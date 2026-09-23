#!/usr/bin/env python3
"""
make-tiles.py — re-encode the category tile photos at the size they display.

    python3 images/make-tiles.py [--width 360] [--quality 0.82]

The tile grid is six across on a desktop and two across on a phone, which works
out to roughly 175-190 CSS pixels wide in both cases. The photos shipped at
500px, so every phone downloaded about 2.7x the pixels it could show. At 360px
they are still 2x for a retina screen.

There is no Pillow or ImageMagick on this machine, so the resizing is done by
headless Chrome: a canvas draws each photo at the target size and re-encodes it
with the browser's own WebP encoder. The page has to be served over HTTP rather
than opened from disk — a file:// image taints the canvas and toDataURL then
refuses to run.

Re-run it after adding or replacing a tile photo. Originals are in git history.
"""
import argparse
import base64
import http.server
import json
import re
import socketserver
import subprocess
import threading
from pathlib import Path

HERE = Path(__file__).resolve().parent
TILES = HERE / "tiles"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

PAGE = """<body><pre id="out"></pre><script>
const files = %(files)s, W = %(w)d, Q = %(q)s, out = {};
let left = files.length;
files.forEach(f => {
  const img = new Image();
  img.onload = () => {
    const H = Math.round(W * img.height / img.width);
    const c = document.createElement('canvas');
    c.width = W; c.height = H;
    c.getContext('2d').drawImage(img, 0, 0, W, H);
    out[f] = c.toDataURL('image/webp', Q);
    if (--left === 0) document.getElementById('out').textContent = JSON.stringify(out);
  };
  img.onerror = () => { out[f] = null; if (--left === 0)
    document.getElementById('out').textContent = JSON.stringify(out); };
  img.src = '/tiles/' + f;
});
</script></body>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--width", type=int, default=360)
    ap.add_argument("--quality", type=float, default=0.82)
    args = ap.parse_args()

    names = sorted(p.name for p in TILES.glob("*.webp"))
    if not names:
        raise SystemExit(f"no tiles in {TILES}")

    page = PAGE % {"files": json.dumps(names), "w": args.width, "q": args.quality}
    (HERE / "_tiles-resize.html").write_text(page)

    handler = lambda *a, **kw: http.server.SimpleHTTPRequestHandler(*a, directory=str(HERE), **kw)
    with socketserver.TCPServer(("127.0.0.1", 0), handler) as httpd:
        port = httpd.server_address[1]
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        dom = subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--virtual-time-budget=20000",
             "--dump-dom", f"http://127.0.0.1:{port}/_tiles-resize.html"],
            capture_output=True, text=True, check=True).stdout
        httpd.shutdown()
    (HERE / "_tiles-resize.html").unlink()

    m = re.search(r'<pre id="out">(\{.*?\})</pre>', dom, re.S)
    if not m:
        raise SystemExit("Chrome returned no data — is the path to Chrome right?")

    before = after = 0
    for name, uri in json.loads(m.group(1)).items():
        p = TILES / name
        before += p.stat().st_size
        if not uri:
            print(f"  SKIP {name} (failed to load)")
            after += p.stat().st_size
            continue
        data = base64.b64decode(uri.split(",", 1)[1])
        p.write_bytes(data)
        after += len(data)
    print(f"{len(names)} tiles: {before // 1024} KB -> {after // 1024} KB "
          f"at {args.width}px wide")


if __name__ == "__main__":
    main()
