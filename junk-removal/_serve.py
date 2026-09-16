#!/usr/bin/env python3
"""
_serve.py — preview the site on your own machine, the way the real server shows it.

    python3 _serve.py          # then open http://localhost:8000
    python3 _serve.py 8080     # or pick a port

WHY NOT `python3 -m http.server`
--------------------------------
Every internal link on this site is extensionless — /pricing, not
/pricing.html — because that is the canonical address, and linking to the
.html form cost a redirect on every click. On the real server, .htaccess maps
/pricing to pricing.html. Python's built-in server does no such mapping, so
every link 404s. Double-clicking index.html breaks the same way.

This is that built-in server plus the one rule it is missing: if /x is not a
file, try /x.html. Standard library only, like _build.py.

It is a preview, not a production server. It does not apply the cache, gzip or
security headers from .htaccess, and it only listens on this machine. For a
byte-for-byte check of the real Apache behaviour, use the Docker image
described in README.md.
"""

import http.server
import os
import sys
from functools import partial
from pathlib import Path

ROOT = Path(__file__).parent


class CleanURLHandler(http.server.SimpleHTTPRequestHandler):
    # Older Pythons do not know these types. The icon masks are SVGs used as
    # CSS mask-image, which some browsers refuse without the right MIME type.
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".webp": "image/webp",
        ".svg": "image/svg+xml",
        ".woff2": "font/woff2",
    }

    def translate_path(self, path):
        fs_path = super().translate_path(path)
        if os.path.isdir(fs_path):
            return fs_path  # the base class serves the directory's index.html
        if not os.path.exists(fs_path) and os.path.exists(fs_path + ".html"):
            return fs_path + ".html"  # /pricing -> pricing.html, as .htaccess does
        return fs_path

    def send_error(self, code, message=None, explain=None):
        # Show the site's own 404 page, as the real server does.
        page = ROOT / "404.html"
        if code == 404 and page.exists():
            body = page.read_bytes()
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)
            return
        super().send_error(code, message, explain)


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    handler = partial(CleanURLHandler, directory=str(ROOT))
    # 127.0.0.1, not 0.0.0.0: a preview should not be reachable from the network.
    with http.server.ThreadingHTTPServer(("127.0.0.1", port), handler) as httpd:
        print(f"Previewing at http://localhost:{port}   (Ctrl-C to stop)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")


if __name__ == "__main__":
    main()
