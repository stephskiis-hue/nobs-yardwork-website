#!/usr/bin/env python3
"""
refresh.py — re-download the self-hosted Plus Jakarta Sans files.

    python3 fonts/refresh.py

The site used to link fonts.googleapis.com. It does not any more: on a phone
that cost two extra handshakes before a single word could paint. These are the
same files Google serves, fetched once and served from our own domain.

Google publishes them as VARIABLE fonts, so one file per subset and style
covers every weight the site uses (400 body, 600/700/800 headings). That is why
there are four files and not ten.

Run this only if the font needs updating. The @font-face rules live at the top
of css/junk.css; if the file names change here, change them there too.

Licence: SIL Open Font License 1.1 — self-hosting is explicitly permitted.
"""
import re
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
CSS = ("https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans"
       ":ital,wght@0,400;0,600;0,700;0,800;1,400&display=swap")
# Google serves woff2 only to browsers it recognises; a bare urllib UA gets ttf.
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
SUBSETS = ("latin", "latin-ext")


def fetch(url, ua=UA):
    return urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": ua}), timeout=30).read()


def main():
    css = fetch(CSS).decode()
    seen = set()
    for subset, body in re.findall(r"/\* (\S+) \*/\s*@font-face \{(.*?)\}", css, re.S):
        if subset not in SUBSETS:
            continue
        style = re.search(r"font-style: (\w+)", body).group(1)
        url = re.search(r"url\((https://[^)]+)\)", body).group(1)
        name = f"plus-jakarta-sans-{subset}-{style}.woff2"
        if name in seen:
            continue
        seen.add(name)
        (HERE / name).write_bytes(fetch(url))
        print(f"  {name}")
    print(f"{len(seen)} files refreshed in {HERE}")


if __name__ == "__main__":
    main()
