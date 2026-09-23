#!/usr/bin/env python3
"""
make-og-card.py — render images/og-card.png, the link-preview image.

    python3 images/make-og-card.py

Social networks crop a shared link's image to roughly 1.91:1 and show it at
about 500px wide in a feed. That rules out the site's photos (a 4:5 hero gets
its crew cropped out) and it rules out fine print. So the card is the badge
logo, which already carries the name and the trade, plus the two things a
stranger needs: where we work and the number to call.

Rendering is done by headless Chrome rather than an image library, because
this machine has no Pillow or ImageMagick and Chrome is already here. The
layout below is ordinary HTML — edit it, re-run, look at the PNG.
"""
import subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Sampled from the badge's own corners, so the artwork sits on its own colour
# instead of on a near-miss that shows as a visible square.
BG = "#043F1E"

HTML = """<!doctype html><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700;800&display=swap" rel="stylesheet">
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{width:1200px;height:630px;background:%(bg)s;font-family:"Plus Jakarta Sans",sans-serif;
       display:flex;align-items:center;gap:36px;padding:0 60px 0 36px;overflow:hidden}
  /* The badge carries its own striped background, which reads as a pasted-on
     square against the flat card. An inset shadow in the card colour feathers
     all four edges without touching the artwork in the middle. */
  .badge{position:relative;flex:none;width:540px;height:540px}
  .badge img{width:540px;height:540px;display:block}
  .badge::after{content:"";position:absolute;inset:0;box-shadow:inset 0 0 38px 8px %(bg)s}
  .copy{display:flex;flex-direction:column;gap:24px}
  h1{font-size:52px;line-height:1.08;font-weight:800;color:#fff;letter-spacing:-.02em}
  h1 span{color:#8FE04D;display:block}
  .meta{font-size:23px;font-weight:700;color:rgba(255,255,255,.85);
        letter-spacing:.05em;text-transform:uppercase;line-height:1.5}
  .dot{color:#8FE04D;padding:0 8px}
  .rule{width:120px;height:7px;background:#8FE04D;border-radius:4px}
</style>
<body>
  <div class="badge"><img src="%(badge)s" alt=""></div>
  <div class="copy">
    <div class="rule"></div>
    <h1>Junk gone.<span>You point, we lift.</span></h1>
    <div class="meta">Winnipeg<span class="dot">&middot;</span>204.900.0438<br>
      All-in pricing &mdash; labour, hauling, dump fees</div>
  </div>
</body>"""


def main():
    if not Path(CHROME).exists():
        sys.exit(f"Chrome not found at {CHROME} — edit CHROME in this script.")
    badge = HERE / "logo-badge.png"
    if not badge.exists():
        sys.exit(f"{badge} is missing. It is the square badge logo.")
    out = HERE / "og-card.png"
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(HTML % {"bg": BG, "badge": badge.as_uri()})
        page = f.name
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--window-size=1200,630",
                    "--virtual-time-budget=6000", f"--screenshot={out}",
                    f"file://{page}"], check=True, capture_output=True)
    print(f"wrote {out} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
