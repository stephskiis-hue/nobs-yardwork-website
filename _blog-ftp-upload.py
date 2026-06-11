#!/usr/bin/env python3
"""
_blog-ftp-upload.py
-------------------
Uploads a new blog post HTML file to the No-BS Yardwork server via FTP,
fetches and updates posts.json, and optionally downloads a Pexels image.

Usage:
  python _blog-ftp-upload.py \
    --file blog-my-post.html \
    --title "My Post Title" \
    --date 2026-04-18 \
    --image images/blog-my-post.webp \
    --category "Lawn Care" \
    --excerpt "Short description up to 160 chars." \
    --readtime 6 \
    [--fetch-image "lawn care winnipeg spring"]

Reads credentials from _blog-ftp.env in the same directory.
"""

import argparse
import ftplib
import json
import os
import sys
import urllib.request
import urllib.error
import time
from pathlib import Path

# ── Load credentials ──────────────────────────────────────────────────────────

def load_env(path="_blog-ftp.env"):
    env = {}
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip()
    except FileNotFoundError:
        print(f"ERROR: {path} not found. Copy _blog-ftp.env.example and fill in your credentials.")
        sys.exit(1)
    return env

# ── FTP helpers ───────────────────────────────────────────────────────────────

def ftp_connect(env):
    """Connect using passive mode (matches FileZilla behaviour on Moniker)."""
    ftp = ftplib.FTP()
    ftp.set_debuglevel(0)
    try:
        ftp.connect(env["FTP_HOST"], int(env.get("FTP_PORT", 21)), timeout=30)
        ftp.login(env["FTP_USER"], env["FTP_PASS"])
        ftp.set_pasv(True)          # passive mode — required by most shared hosts
        print(f"✅ FTP connected to {env['FTP_HOST']}")
        return ftp
    except ftplib.all_errors as e:
        print(f"ERROR: FTP connection failed: {e}")
        sys.exit(1)

def ftp_upload_file(ftp, local_path, remote_dir, remote_name=None):
    """Upload a single file. Changes to remote_dir first."""
    remote_name = remote_name or Path(local_path).name
    try:
        ftp.cwd(remote_dir)
    except ftplib.error_perm:
        print(f"ERROR: Remote directory '{remote_dir}' not found.")
        sys.exit(1)
    with open(local_path, "rb") as f:
        ftp.storbinary(f"STOR {remote_name}", f)
    print(f"  ↑ Uploaded {remote_name} → {remote_dir}/{remote_name}")

def ftp_upload_bytes(ftp, data: bytes, remote_dir, remote_name):
    """Upload bytes directly (for in-memory content like posts.json)."""
    import io
    ftp.cwd(remote_dir)
    ftp.storbinary(f"STOR {remote_name}", io.BytesIO(data))
    print(f"  ↑ Uploaded {remote_name} → {remote_dir}/{remote_name}")

# ── posts.json update ─────────────────────────────────────────────────────────

def update_posts_json(ftp, env, new_entry):
    """Fetch current posts.json from live site, prepend new entry, re-upload."""
    url = env["SITE_URL"].rstrip("/") + "/posts.php"
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            posts = json.loads(r.read().decode())
        print(f"  ↓ Fetched posts.json ({len(posts)} existing posts)")
    except Exception as e:
        print(f"  ⚠ Could not fetch posts.json from live site ({e}), starting fresh list")
        posts = []

    # Remove any existing entry with same URL to avoid duplicates
    posts = [p for p in posts if p.get("url") != new_entry["url"]]
    posts.insert(0, new_entry)

    data = json.dumps(posts, indent=2, ensure_ascii=False).encode("utf-8")
    ftp_upload_bytes(ftp, data, env["FTP_PATH"], "posts.json")

    # Also write locally so blog.html inline fallback can be updated separately
    with open("posts.json", "wb") as f:
        f.write(data)
    print(f"  ✏  Local posts.json updated ({len(posts)} posts total)")

# ── Pexels image fetch ────────────────────────────────────────────────────────

def fetch_pexels_image(keywords, slug, env):
    """
    Search Pexels for keywords, download best landscape image,
    convert to webp, save as images/blog-{slug}.webp, return path.
    Returns None if Pexels API key not set or fetch fails.
    """
    api_key = env.get("PEXELS_API_KEY", "")
    if not api_key or api_key.startswith("PASTE"):
        print("  ⚠ PEXELS_API_KEY not set — skipping image fetch, using fallback image")
        return None

    try:
        from PIL import Image
        import io as _io
    except ImportError:
        print("  ⚠ Pillow not installed — skipping image fetch (pip install Pillow)")
        return None

    query = urllib.parse.quote(keywords)
    api_url = f"https://api.pexels.com/v1/search?query={query}&per_page=10&orientation=landscape"

    req = urllib.request.Request(api_url, headers={"Authorization": api_key})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read().decode())
    except Exception as e:
        print(f"  ⚠ Pexels API error: {e}")
        return None

    photos = data.get("photos", [])
    if not photos:
        print(f"  ⚠ No Pexels results for '{keywords}'")
        return None

    # Pick first landscape photo
    photo = photos[0]
    img_url = photo["src"]["large"]
    photo_credit = photo["photographer"]

    print(f"  📷 Pexels photo by {photo_credit}: {img_url}")

    # Download
    try:
        with urllib.request.urlopen(img_url, timeout=30) as r:
            img_data = r.read()
    except Exception as e:
        print(f"  ⚠ Image download failed: {e}")
        return None

    # Convert to webp
    local_path = f"images/blog-{slug}.webp"
    try:
        img = Image.open(_io.BytesIO(img_data))
        img = img.convert("RGB")
        # Resize to max 1200px wide
        if img.width > 1200:
            ratio = 1200 / img.width
            img = img.resize((1200, int(img.height * ratio)), Image.LANCZOS)
        img.save(local_path, "WEBP", quality=85)
        print(f"  🖼  Saved {local_path} ({img.width}×{img.height})")
        return local_path
    except Exception as e:
        print(f"  ⚠ Image conversion failed: {e}")
        return None

# ── Main ──────────────────────────────────────────────────────────────────────

import urllib.parse

def main():
    parser = argparse.ArgumentParser(description="Upload blog post to No-BS Yardwork server")
    parser.add_argument("--file",        required=True,  help="Local HTML filename, e.g. blog-my-post.html")
    parser.add_argument("--title",       required=True,  help="Post title")
    parser.add_argument("--date",        required=True,  help="Publish date YYYY-MM-DD")
    parser.add_argument("--image",       required=True,  help="Image path, e.g. images/blog-my-post.webp")
    parser.add_argument("--category",    required=True,  help="Category: Lawn Care / Cleanups / Fencing / etc.")
    parser.add_argument("--excerpt",     required=True,  help="Short excerpt (max 160 chars)")
    parser.add_argument("--readtime",    required=True,  type=int, help="Estimated read time in minutes")
    parser.add_argument("--fetch-image", default=None,   help="Keywords to search Pexels for a photo")
    args = parser.parse_args()

    env = load_env()

    # ── Optionally fetch image from Pexels ────────────────────────────────────
    slug = Path(args.file).stem  # e.g. "blog-my-post"
    image_path = args.image

    if args.fetch_image:
        fetched = fetch_pexels_image(args.fetch_image, slug, env)
        if fetched:
            image_path = fetched

    # ── Connect FTP ───────────────────────────────────────────────────────────
    ftp = ftp_connect(env)

    # ── Upload image if it was fetched ────────────────────────────────────────
    if image_path != args.image and os.path.exists(image_path):
        ftp_upload_file(ftp, image_path, env["FTP_PATH"] + "/images", Path(image_path).name)

    # ── Upload HTML ───────────────────────────────────────────────────────────
    if not os.path.exists(args.file):
        print(f"ERROR: HTML file '{args.file}' not found in current directory.")
        ftp.quit()
        sys.exit(1)
    ftp_upload_file(ftp, args.file, env["FTP_PATH"], args.file)

    # ── Update posts.json ─────────────────────────────────────────────────────
    new_entry = {
        "title":    args.title,
        "date":     args.date,
        "image":    image_path,
        "excerpt":  args.excerpt[:200],
        "url":      args.file,
        "category": args.category,
        "readTime": args.readtime
    }
    update_posts_json(ftp, env, new_entry)

    ftp.quit()
    print(f"\n🚀 Done! Post live at: {env['SITE_URL']}/{args.file}")

if __name__ == "__main__":
    main()
