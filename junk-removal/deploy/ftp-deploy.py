#!/usr/bin/env python3
"""
ftp-deploy.py — put the built site on the cPanel server at Namecheap.

    python3 deploy/ftp-deploy.py --dry-run     # show what would change
    python3 deploy/ftp-deploy.py               # build + upload what changed
    python3 deploy/ftp-deploy.py --all         # re-upload everything
    python3 deploy/ftp-deploy.py --prune       # also delete stale remote files

It runs deploy/make-dist.sh first, so what lands on the server is always a
fresh build of the current working tree — never a stale dist/.

Three things worth knowing:

* **FTPS, not FTP.** Plain FTP sends the password and every file in the clear.
  Pure-FTPd on this host speaks explicit TLS on port 21, so the script insists
  on it and refuses rather than silently falling back to cleartext.
* **Only what changed goes up.** deploy/.deploy-state.json records a hash per
  file from the last successful run; unchanged files are skipped. Delete that
  file (or pass --all) to force a full upload.
* **Not everything on the server is ours.** KEEP below lists the paths cPanel
  and the SSL renewal own. They are never pruned, whatever --prune finds.

Credentials live in deploy/.env (gitignored). See DEPLOY.md.
"""

import argparse
import ftplib
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DIST = ROOT / "dist"
ENV_FILE = HERE / ".env"
STATE_FILE = HERE / ".deploy-state.json"

# Server-owned paths. .well-known carries the Let's Encrypt/AutoSSL challenge
# files — deleting it breaks certificate renewal, and the site goes to a
# browser warning weeks later with nothing obvious to blame.
KEEP = {".well-known", "cgi-bin", ".ftpquota", ".trash", "_errorpages"}


def load_env():
    if not ENV_FILE.exists():
        sys.exit(f"ERROR: {ENV_FILE} not found. See DEPLOY.md for what goes in it.")
    env = {}
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    missing = {"FTP_HOST", "FTP_USER", "FTP_PASS"} - env.keys()
    if missing:
        sys.exit(f"ERROR: {ENV_FILE} is missing {', '.join(sorted(missing))}.")
    return env


def connect(env):
    ftp = ftplib.FTP_TLS()
    ftp.connect(env["FTP_HOST"], int(env.get("FTP_PORT", 21)), timeout=30)
    ftp.login(env["FTP_USER"], env["FTP_PASS"])
    ftp.prot_p()          # encrypt the data channel, not just the login
    ftp.set_pasv(True)    # shared hosts refuse active mode
    return ftp


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def local_files():
    """Every file in dist/, as {relative posix path: sha256}."""
    out = {}
    for p in sorted(DIST.rglob("*")):
        if p.is_file() and p.name != ".DS_Store":
            out[p.relative_to(DIST).as_posix()] = digest(p)
    return out


def ensure_dir(ftp, remote_dir, made):
    """mkdir -p, remembering what already exists so each dir is tried once."""
    if remote_dir in ("", ".") or remote_dir in made:
        return
    parent = os.path.dirname(remote_dir)
    ensure_dir(ftp, parent, made)
    try:
        ftp.mkd(remote_dir)
    except ftplib.error_perm as e:
        if not str(e).startswith("550"):   # 550 = already there
            raise
    made.add(remote_dir)


def remote_tree(ftp, path=""):
    """Every remote file path under `path`, skipping the server's own dirs."""
    found = []
    try:
        entries = list(ftp.mlsd(path or "."))
    except ftplib.error_perm:
        return found
    for name, facts in entries:
        if name in (".", ".."):
            continue
        rel = f"{path}/{name}" if path else name
        if rel.split("/")[0] in KEEP:
            continue
        if facts.get("type") == "dir":
            found.extend(remote_tree(ftp, rel))
        elif facts.get("type") == "file":
            found.append(rel)
    return found


def main():
    ap = argparse.ArgumentParser(description="Upload the built site over FTPS.")
    ap.add_argument("--dry-run", action="store_true", help="list changes, upload nothing")
    ap.add_argument("--all", action="store_true", help="ignore the state file, upload everything")
    ap.add_argument("--prune", action="store_true", help="delete remote files no longer in dist/")
    ap.add_argument("--no-build", action="store_true", help="use the existing dist/ as-is")
    args = ap.parse_args()

    if not args.no_build:
        subprocess.run(["sh", "deploy/make-dist.sh"], cwd=ROOT, check=True)
    if not DIST.is_dir():
        sys.exit("ERROR: dist/ does not exist. Run: sh deploy/make-dist.sh")

    files = local_files()
    state = {} if args.all else json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {}
    changed = [f for f, h in files.items() if state.get(f) != h]

    print(f"{len(files)} files in dist/, {len(changed)} to upload")
    if args.dry_run:
        for f in changed:
            print("  would upload", f)

    env = load_env()
    ftp = connect(env)
    print(f"connected to {env['FTP_HOST']} as {env['FTP_USER']} (FTPS, {ftp.pwd()})")

    try:
        stale = []
        if args.prune:
            stale = sorted(set(remote_tree(ftp)) - set(files))
            for f in stale:
                print(("  would delete " if args.dry_run else "  deleting ") + f)
                if not args.dry_run:
                    ftp.delete(f)

        if args.dry_run:
            print("dry run — nothing changed on the server")
            return

        made = set()
        done = 0
        for rel in changed:
            ensure_dir(ftp, os.path.dirname(rel), made)
            with open(DIST / rel, "rb") as fh:
                ftp.storbinary(f"STOR {rel}", fh)
            state[rel] = files[rel]
            done += 1
            print(f"  [{done}/{len(changed)}] {rel}")

        # Drop entries for files that no longer exist locally, so the state
        # file does not grow forever with pages that were renamed away.
        state = {f: h for f, h in state.items() if f in files}
        STATE_FILE.write_text(json.dumps(state, indent=1, sort_keys=True))
        print(f"done: {done} uploaded, {len(files) - done} unchanged, {len(stale)} deleted")
    finally:
        try:
            ftp.quit()
        except Exception:
            ftp.close()


if __name__ == "__main__":
    main()
