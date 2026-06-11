#!/usr/bin/env python3
"""
_blog-autopilot.py
------------------
Fully automated blog post generator + publisher for No-BS Yardwork.
Called by the Claude Code scheduled agent each day.

What it does (Claude agent handles steps 1-5, this script handles 6-9):
  1. [Claude agent] Research seasonal SEO keywords via web search
  2. [Claude agent] Scan competitor sites for topic gaps
  3. [Claude agent] Pick best topic based on season + content rotation
  4. [Claude agent] Write 700-950 word HTML blog post
  5. [Claude agent] Save HTML file to this directory
  6. [This script]  Fetch Pexels image (or use fallback)
  7. [This script]  FTP upload HTML + image
  8. [This script]  Update posts.json on server
  9. [This script]  Update _blog-state.json locally

Usage (called by Claude agent after writing the post):
  python _blog-autopilot.py \
    --file blog-slug-here.html \
    --title "Post Title Here" \
    --date 2026-04-18 \
    --image images/blog-slug-here.webp \
    --category "Lawn Care" \
    --excerpt "160-char excerpt." \
    --readtime 7 \
    --slug blog-slug-here \
    [--fetch-image "lawn care aeration winnipeg spring"]
"""

import argparse
import ftplib
import json
import os
import sys
import io
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
ENV_FILE   = SCRIPT_DIR / "_blog-ftp.env"
STATE_FILE = SCRIPT_DIR / "_blog-state.json"

# ── Content type rotation ──────────────────────────────────────────────────────
CONTENT_TYPES = ["cost-guide", "how-to", "tips-and-tricks", "comparison", "timing-guide"]

def next_content_type(last: str) -> str:
    try:
        idx = CONTENT_TYPES.index(last)
    except ValueError:
        idx = -1
    return CONTENT_TYPES[(idx + 1) % len(CONTENT_TYPES)]

# ── State helpers ──────────────────────────────────────────────────────────────

def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {"last_content_type": "how-to", "published_slugs": []}

def save_state(state: dict):
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")

# ── Season detection ───────────────────────────────────────────────────────────

def current_season() -> str:
    month = datetime.now().month
    if month in (3, 4, 5):   return "spring"
    if month in (6, 7, 8):   return "summer"
    if month in (9, 10):     return "fall"
    return "winter"

# ── Env loader ─────────────────────────────────────────────────────────────────

def load_env() -> dict:
    env = {}
    if not ENV_FILE.exists():
        print(f"ERROR: {ENV_FILE} not found.")
        sys.exit(1)
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env

# ── Pexels image fetch ─────────────────────────────────────────────────────────

BROWSER_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NoBS-Yardwork-Blog/1.0"

def fetch_pexels_image(keywords: str, slug: str, env: dict):
    api_key = env.get("PEXELS_API_KEY", "")
    if not api_key or api_key.startswith("YOUR_KEY"):
        print("  WARN PEXELS_API_KEY not set -- skipping image fetch")
        return None
    try:
        from PIL import Image as PILImage
    except ImportError:
        print("  WARN Pillow not installed -- skipping image fetch")
        return None

    # Filename: slugs already start with 'blog-'; don't double-prefix.
    base = slug if slug.startswith("blog-") else f"blog-{slug}"

    query = urllib.parse.quote(keywords)
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=15&orientation=landscape"
    req = urllib.request.Request(
        url,
        headers={"Authorization": api_key, "User-Agent": BROWSER_UA},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", errors="replace")[:200]
        except Exception:
            pass
        print(f"  WARN Pexels API {e.code} {e.reason} {body}")
        return None
    except Exception as e:
        print(f"  WARN Pexels API error: {e}")
        return None

    photos = data.get("photos", [])
    if not photos:
        print(f"  WARN No Pexels results for '{keywords}'")
        return None

    # Prefer a clearly-landscape photo (width > height); fall back to first.
    photo = next(
        (p for p in photos if p.get("width", 0) > p.get("height", 1)),
        photos[0],
    )
    img_url = photo["src"].get("large2x") or photo["src"]["large"]
    print(f"  PHOTO Pexels -- {photo['photographer']}: {img_url}")

    try:
        img_req = urllib.request.Request(img_url, headers={"User-Agent": BROWSER_UA})
        with urllib.request.urlopen(img_req, timeout=30) as r:
            raw = r.read()
    except Exception as e:
        print(f"  WARN Image download failed: {e}")
        return None

    local_path = SCRIPT_DIR / "images" / f"{base}.webp"
    try:
        img = PILImage.open(io.BytesIO(raw)).convert("RGB")
        if img.width > 1200:
            ratio = 1200 / img.width
            img = img.resize((1200, int(img.height * ratio)), PILImage.LANCZOS)
        img.save(str(local_path), "WEBP", quality=85)
        print(f"  SAVED {local_path.name} ({img.width}x{img.height})")
        return f"images/{base}.webp"
    except Exception as e:
        print(f"  WARN Image conversion failed: {e}")
        return None

# ── FTP helpers ────────────────────────────────────────────────────────────────

def ftp_connect(env: dict) -> ftplib.FTP:
    ftp = ftplib.FTP()
    try:
        ftp.connect(env["FTP_HOST"], int(env.get("FTP_PORT", 21)), timeout=30)
        ftp.login(env["FTP_USER"], env["FTP_PASS"])
        ftp.set_pasv(True)
        print(f"FTP connected to {env['FTP_HOST']}")
        return ftp
    except ftplib.all_errors as e:
        print(f"ERROR: FTP connection failed: {e}")
        sys.exit(1)

def ftp_upload_file(ftp: ftplib.FTP, local_path: str, remote_dir: str, remote_name: str = None):
    remote_name = remote_name or Path(local_path).name
    try:
        ftp.cwd(remote_dir)
    except ftplib.error_perm as e:
        print(f"ERROR: Remote dir '{remote_dir}' not found: {e}")
        sys.exit(1)
    with open(local_path, "rb") as f:
        ftp.storbinary(f"STOR {remote_name}", f)
    print(f"  UP {remote_name} -> {remote_dir}/")

def ftp_upload_bytes(ftp: ftplib.FTP, data: bytes, remote_dir: str, remote_name: str):
    ftp.cwd(remote_dir)
    ftp.storbinary(f"STOR {remote_name}", io.BytesIO(data))
    print(f"  UP {remote_name} -> {remote_dir}/")

def update_posts(new_entry: dict) -> list:
    """
    Load local posts.json, prepend the new entry, sort newest-first,
    save back to posts.json. Returns the updated list.
    Note: hosting blocks .json and .php serving, so blog.html
    uses an inline POSTS array — we patch that directly via patch_blog_html().
    """
    local_json = SCRIPT_DIR / "posts.json"
    if local_json.exists():
        posts = json.loads(local_json.read_text(encoding="utf-8"))
    else:
        posts = []

    posts = [p for p in posts if p.get("url") != new_entry["url"]]
    posts.insert(0, new_entry)
    posts.sort(key=lambda p: p.get("date", ""), reverse=True)

    local_json.write_bytes(json.dumps(posts, indent=2, ensure_ascii=False).encode("utf-8"))
    print(f"  LOCAL posts.json updated ({len(posts)} posts total)")
    return posts


def patch_blog_html(ftp: ftplib.FTP, env: dict, posts: list):
    """
    Replace the var POSTS = [...] inline array in blog.html with the
    current posts list, then re-upload blog.html to the server.
    This is the primary data delivery mechanism since the host blocks
    direct .json/.php fetching.
    """
    import re
    blog_path = SCRIPT_DIR / "blog.html"
    html = blog_path.read_text(encoding="utf-8")

    # Build the JS-safe posts array (single-quoted strings, escaped apostrophes)
    def js_str(s):
        return s.replace("\\", "\\\\").replace("'", "\\'")

    lines = ["[\n"]
    for i, p in enumerate(posts):
        comma = "" if i == len(posts) - 1 else ","
        lines.append(
            f"        {{\n"
            f"          title:    '{js_str(p['title'])}',\n"
            f"          date:     '{p['date']}',\n"
            f"          image:    '{p['image']}',\n"
            f"          excerpt:  '{js_str(p['excerpt'])}',\n"
            f"          url:      '{p['url']}',\n"
            f"          category: '{p['category']}',\n"
            f"          readTime: {p['readTime']}\n"
            f"        }}{comma}\n"
        )
    lines.append("      ]")
    new_array = "".join(lines)

    new_html, count = re.subn(
        r"var POSTS\s*=\s*\[.*?\];",
        f"var POSTS = {new_array};",
        html,
        flags=re.DOTALL,
    )
    if count == 0:
        print("  WARN Could not find var POSTS in blog.html — skipping patch")
        return

    blog_path.write_text(new_html, encoding="utf-8")
    ftp_upload_file(ftp, str(blog_path), env["FTP_PATH"], "blog.html")
    print(f"  UP blog.html patched with {len(posts)} posts and re-uploaded")

# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file",        required=True)
    parser.add_argument("--title",       required=True)
    parser.add_argument("--date",        required=True)
    parser.add_argument("--image",       required=True, help="Fallback image path if Pexels fails")
    parser.add_argument("--category",    required=True)
    parser.add_argument("--excerpt",     required=True)
    parser.add_argument("--readtime",    required=True, type=int)
    parser.add_argument("--slug",        required=True, help="Slug without .html, e.g. blog-lawn-care-tips")
    parser.add_argument("--fetch-image", default=None,  help="Pexels search keywords")
    args = parser.parse_args()

    env   = load_env()
    state = load_state()

    print(f"\nSeason:   {current_season()}")
    print(f"Post:     {args.title}")
    print(f"Category: {args.category}")

    # ── Fetch Pexels image ────────────────────────────────────────────────────
    image_path = args.image
    if args.fetch_image:
        fetched = fetch_pexels_image(args.fetch_image, args.slug, env)
        if fetched:
            image_path = fetched

    # ── FTP ───────────────────────────────────────────────────────────────────
    ftp = ftp_connect(env)

    # Always upload the hero image if it exists locally (Pexels-fetched or fallback)
    local_img = SCRIPT_DIR / image_path
    if local_img.exists():
        ftp_upload_file(ftp, str(local_img), env["FTP_PATH"] + "/images", Path(image_path).name)
    else:
        print(f"  WARN hero image missing at {local_img} -- skipping image upload")

    # Upload HTML
    html_path = SCRIPT_DIR / args.file
    if not html_path.exists():
        print(f"ERROR: HTML file '{args.file}' not found.")
        ftp.quit()
        sys.exit(1)
    ftp_upload_file(ftp, str(html_path), env["FTP_PATH"], args.file)

    # Update posts.json (local) + patch blog.html inline array + re-upload blog.html
    new_entry = {
        "title":    args.title,
        "date":     args.date,
        "image":    image_path,
        "excerpt":  args.excerpt[:200],
        "url":      args.slug,
        "category": args.category,
        "readTime": args.readtime,
    }
    posts = update_posts(new_entry)
    patch_blog_html(ftp, env, posts)
    ftp.quit()

    # ── Update state ──────────────────────────────────────────────────────────
    state["last_content_type"] = next_content_type(state.get("last_content_type", "how-to"))
    slugs = state.get("published_slugs", [])
    if args.slug not in slugs:
        slugs.append(args.slug)
    state["published_slugs"] = slugs
    save_state(state)

    print(f"\nDone! Post live at: {env['SITE_URL']}/{args.slug}")
    print(f"Next content type: {state['last_content_type']}")
    print(f"Total posts published: {len(slugs)}")

if __name__ == "__main__":
    main()
