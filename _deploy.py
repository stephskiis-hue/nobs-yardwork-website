#!/usr/bin/env python3
"""
_deploy.py
----------
Generic deploy tool for the No-BS Yardwork website.

Uploads any file(s) you name straight to the live server over FTP — the same
way the blog autopilot publishes posts. Use this to push edits to any page
(index.html, projects.html, about.html, css/custom.css, images/..., etc.)
so they go live immediately.

Why this exists:
  GitHub does NOT auto-deploy this site. The live site at no-bs-yardwork.com
  is updated by uploading files over FTP. Pushing to GitHub only updates the
  Git repo, not the server. This script is the bridge that actually publishes.

Usage:
  python3 _deploy.py projects.html
  python3 _deploy.py index.html about.html css/custom.css
  python3 _deploy.py images/blog-foo.webp        # subfolders are preserved
  python3 _deploy.py --all-changed               # deploy everything git sees as modified
  python3 _deploy.py --dry-run projects.html     # show what WOULD upload, send nothing

Credentials:
  Reads _blog-ftp.env in this directory (same file the blog robot uses):
      FTP_HOST=...
      FTP_PORT=21
      FTP_USER=...
      FTP_PASS=...
      FTP_PATH=/public_html        # remote web root
      SITE_URL=https://no-bs-yardwork.com
  Falls back to OS environment variables of the same names if the file is
  absent (useful if you ever wire FTP secrets into a hosted environment).

Notes:
  - A file's path relative to this folder is preserved on the server, so
    "css/custom.css" lands in "<FTP_PATH>/css/custom.css".
  - Missing remote subdirectories are created automatically.
  - This must run somewhere that has the FTP credentials AND is allowed to
    make outbound FTP connections (your local machine). It will NOT work from
    the claude.ai web sandbox, which blocks raw FTP.
"""

import argparse
import ftplib
import os
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ENV_FILE = SCRIPT_DIR / "_blog-ftp.env"

REQUIRED_KEYS = ["FTP_HOST", "FTP_USER", "FTP_PASS", "FTP_PATH"]


# ── Credentials ─────────────────────────────────────────────────────────────────

def load_env() -> dict:
    """Load FTP credentials from _blog-ftp.env, falling back to OS env vars."""
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                # Strip inline comments and surrounding quotes
                v = v.split("#", 1)[0].strip().strip('"').strip("'")
                env[k.strip()] = v

    # Fall back to OS environment for any key not found in the file
    for key in REQUIRED_KEYS + ["FTP_PORT", "SITE_URL"]:
        if key not in env and os.environ.get(key):
            env[key] = os.environ[key]

    missing = [k for k in REQUIRED_KEYS if not env.get(k)]
    if missing:
        print(f"ERROR: missing credential(s): {', '.join(missing)}")
        print(f"       Add them to {ENV_FILE.name} or set them as environment variables.")
        if not ENV_FILE.exists():
            print(f"       ({ENV_FILE.name} was not found in {SCRIPT_DIR})")
        sys.exit(1)

    env.setdefault("FTP_PORT", "21")
    env.setdefault("SITE_URL", "https://no-bs-yardwork.com")
    return env


# ── File selection ──────────────────────────────────────────────────────────────

def git_changed_files() -> list[str]:
    """Return tracked files git reports as modified/added (for --all-changed)."""
    try:
        out = subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=SCRIPT_DIR, text=True
        )
    except Exception as e:
        print(f"ERROR: could not run git status: {e}")
        sys.exit(1)

    files = []
    for line in out.splitlines():
        if not line.strip():
            continue
        path = line[3:].strip()
        # Handle renames "old -> new"
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        # Only deploy real, web-servable files (skip the tooling/state files)
        if path.startswith("_") or path == ".gitignore":
            continue
        if (SCRIPT_DIR / path).is_file():
            files.append(path)
    return files


# ── FTP ─────────────────────────────────────────────────────────────────────────

def ftp_connect(env: dict) -> ftplib.FTP:
    ftp = ftplib.FTP()
    try:
        ftp.connect(env["FTP_HOST"], int(env["FTP_PORT"]), timeout=30)
        ftp.login(env["FTP_USER"], env["FTP_PASS"])
        ftp.set_pasv(True)  # passive mode — required by most shared hosts
        print(f"FTP connected to {env['FTP_HOST']}")
        return ftp
    except ftplib.all_errors as e:
        print(f"ERROR: FTP connection failed: {e}")
        sys.exit(1)


def ftp_ensure_dir(ftp: ftplib.FTP, remote_dir: str):
    """Change to remote_dir, creating any missing path segments along the way."""
    # Always start from an absolute base
    ftp.cwd("/")
    for part in remote_dir.strip("/").split("/"):
        if not part:
            continue
        try:
            ftp.cwd(part)
        except ftplib.error_perm:
            ftp.mkd(part)
            ftp.cwd(part)


def deploy_file(ftp: ftplib.FTP, rel_path: str, ftp_root: str) -> bool:
    local = SCRIPT_DIR / rel_path
    if not local.is_file():
        print(f"  SKIP {rel_path} (not found locally)")
        return False

    rel = Path(rel_path)
    remote_dir = ftp_root.rstrip("/")
    if rel.parent != Path("."):
        remote_dir = f"{remote_dir}/{rel.parent.as_posix()}"

    ftp_ensure_dir(ftp, remote_dir)
    with open(local, "rb") as f:
        ftp.storbinary(f"STOR {rel.name}", f)
    print(f"  UP  {rel_path}  ->  {remote_dir}/{rel.name}")
    return True


# ── Main ────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Deploy file(s) to the No-BS Yardwork server over FTP")
    parser.add_argument("files", nargs="*", help="File(s) to upload, relative to this folder")
    parser.add_argument("--all-changed", action="store_true", help="Deploy every file git reports as modified")
    parser.add_argument("--dry-run", action="store_true", help="Show what would upload without connecting")
    args = parser.parse_args()

    files = list(args.files)
    if args.all_changed:
        files = git_changed_files()
        if not files:
            print("Nothing to deploy — git reports no modified web files.")
            return
        print("Files git sees as changed:")
        for f in files:
            print(f"  - {f}")

    if not files:
        parser.error("no files given (pass filenames or use --all-changed)")

    env = load_env()

    if args.dry_run:
        print("\nDRY RUN — would upload these to "
              f"{env['FTP_HOST']}:{env['FTP_PATH']} :")
        for f in files:
            exists = "" if (SCRIPT_DIR / f).is_file() else "  (MISSING LOCALLY)"
            print(f"  {f}{exists}")
        return

    ftp = ftp_connect(env)
    uploaded = 0
    for f in files:
        if deploy_file(ftp, f, env["FTP_PATH"]):
            uploaded += 1
    ftp.quit()

    print(f"\nDone. {uploaded} file(s) live.")
    site = env["SITE_URL"].rstrip("/")
    for f in files:
        if (SCRIPT_DIR / f).is_file():
            url_path = f[:-len("index.html")] if f.endswith("index.html") else f
            print(f"  {site}/{url_path}")


if __name__ == "__main__":
    main()
