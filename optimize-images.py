#!/usr/bin/env python3
"""
optimize-images.py — No-BS Yardwork Image Optimizer
Usage: python optimize-images.py
Requires: pip install Pillow

1. Scans HTML files + custom.css for referenced images
2. Re-encodes referenced WebP files >100KB (85% quality, 90% for LCP hero)
3. Lists PNG files safe to delete (no HTML references, WebP counterpart exists)
4. Lists junk files (copies, PSD, ini, etc.)
"""

import os
import re
import sys
import shutil
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow not installed. Run: pip install Pillow")
    sys.exit(1)

ROOT = Path(__file__).parent
IMAGES_DIR = ROOT / "images"
LCP_IMAGE = "lawn7.webp"
SKIP_BELOW_KB = 100


def get_referenced_images():
    referenced = set()

    # Scan all HTML files in root
    for html_file in ROOT.glob("*.html"):
        content = html_file.read_text(encoding="utf-8", errors="ignore")
        for m in re.finditer(r'(?:src|href|content|url)\s*[=(]["\']?images/([^"\'\s)>?#]+)', content):
            referenced.add(m.group(1))

    # Scan custom.css for background-image references
    css_path = ROOT / "css" / "custom.css"
    if css_path.exists():
        css = css_path.read_text(encoding="utf-8", errors="ignore")
        for m in re.finditer(r'url\([\'"]?\.\.\/images\/([^\'")\s]+)[\'"]?\)', css):
            referenced.add(m.group(1))

    return referenced


def compress_webp(referenced):
    print("=== COMPRESSING REFERENCED WebP FILES ===")
    total_saved = 0
    compressed = 0
    skipped = 0

    webp_files = sorted(IMAGES_DIR.glob("*.webp"))

    for fp in webp_files:
        if fp.name not in referenced:
            continue

        size = fp.stat().st_size
        if size < SKIP_BELOW_KB * 1024:
            print(f"SKIP  ({size//1024:>5}KB) {fp.name}")
            skipped += 1
            continue

        quality = 90 if fp.name == LCP_IMAGE else 85
        tmp = fp.with_suffix(".tmp.webp")

        try:
            with Image.open(fp) as img:
                # Convert to RGB/RGBA to strip EXIF metadata (smaller file, no charset issues)
                if img.mode in ("RGBA", "LA", "P"):
                    img = img.convert("RGBA")
                else:
                    img = img.convert("RGB")
                img.save(tmp, "WEBP", quality=quality, method=6)

            new_size = tmp.stat().st_size
            saved = size - new_size
            pct = (saved / size * 100) if size > 0 else 0

            if new_size >= size:
                print(f"SKIP  (already optimal: {size//1024}KB, re-encoded={new_size//1024}KB) {fp.name}")
                tmp.unlink()
                skipped += 1
                continue

            print(f"COMPRESS ({size//1024:>5}KB → {new_size//1024:>5}KB, -{pct:.1f}%, q={quality}) {fp.name}")

            shutil.move(str(tmp), str(fp))
            total_saved += saved
            compressed += 1

        except Exception as e:
            print(f"ERROR: {fp.name}: {e}")
            if tmp.exists():
                tmp.unlink()

    print(f"\nCompressed {compressed} files. Skipped {skipped} (under {SKIP_BELOW_KB}KB).")
    print(f"Total savings: {total_saved / 1024 / 1024:.2f}MB")


def list_deletable_pngs(referenced):
    print("\n=== PNG FILES SAFE TO DELETE ===")
    total_size = 0

    for fp in sorted(IMAGES_DIR.glob("*.png")):
        if fp.name in referenced:
            continue  # PNG is directly referenced — don't delete

        webp_name = fp.stem + ".webp"
        webp_path = IMAGES_DIR / webp_name
        webp_exists = webp_path.exists()
        webp_referenced = webp_name in referenced

        size = fp.stat().st_size
        total_size += size

        if webp_exists and webp_referenced:
            reason = "(WebP counterpart referenced in HTML)"
        elif webp_exists:
            reason = "(WebP exists but also unreferenced)"
        else:
            reason = "(no WebP counterpart, fully unreferenced)"

        print(f"DELETE: images/{fp.name} ({size/1024/1024:.1f}MB) {reason}")

    print(f"\nTotal PNG deletion savings: {total_size/1024/1024:.1f}MB")


def list_junk_files(referenced):
    print("\n=== JUNK / LARGE UNREFERENCED FILES ===")
    for fp in sorted(IMAGES_DIR.iterdir()):
        if not fp.is_file():
            continue
        ext = fp.suffix.lower()
        name = fp.name
        size = fp.stat().st_size

        is_junk = (
            ext in (".psd", ".ini", ".mp4")
            or " - Copy" in name
            or " copy" in name.lower()
            or name == "desktop.ini"
        )
        is_large_unreferenced_svg = (
            ext == ".svg"
            and name not in referenced
            and size > 50 * 1024
        )

        if is_junk:
            print(f"JUNK:   images/{name} ({size//1024}KB)")
        elif is_large_unreferenced_svg:
            print(f"LARGE UNREFERENCED SVG: images/{name} ({size//1024}KB)")


def main():
    print("=== No-BS Yardwork Image Optimizer ===\n")
    print("Scanning HTML files and CSS for referenced images...")
    referenced = get_referenced_images()
    print(f"Found {len(referenced)} unique referenced images.\n")

    compress_webp(referenced)
    list_deletable_pngs(referenced)
    list_junk_files(referenced)

    print("\n=== DONE ===")


if __name__ == "__main__":
    main()
