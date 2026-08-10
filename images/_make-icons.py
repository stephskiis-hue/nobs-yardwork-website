#!/usr/bin/env python3
"""
Generates the 12 "What We Take" line icons.

Stroke-based and drawn in `currentColor`, so a single file works on any
background and takes its colour from the CSS `color` property — that is how
`.take-grid` tints them with --division-color without a second asset set.

Run from this directory:  python3 _make-icons.py
"""

from pathlib import Path

HEAD = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" '
    'viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.5" '
    'stroke-linecap="round" stroke-linejoin="round" role="img" '
    'aria-hidden="true">'
)

ICONS = {
    # Couch: back, seat, two arms, two legs.
    "furniture": """
      <path d="M8 22v-6a3 3 0 0 1 3-3h26a3 3 0 0 1 3 3v6"/>
      <path d="M8 22a3 3 0 0 1 3 3v4h26v-4a3 3 0 0 1 3-3"/>
      <path d="M5 22h3v10H5zM40 22h3v10h-3z"/>
      <path d="M11 32v4M37 32v4"/>
    """,
    # Fridge: tall body, freezer divider, two handles.
    "appliance": """
      <rect x="13" y="6" width="22" height="36" rx="3"/>
      <path d="M13 19h22"/>
      <path d="M19 12v4M19 24v6"/>
    """,
    # Mattress: rounded slab with quilting buttons.
    "mattress": """
      <rect x="5" y="16" width="38" height="18" rx="4"/>
      <path d="M5 25h38"/>
      <path d="M14 20.5v0M24 20.5v0M34 20.5v0M14 29.5v0M24 29.5v0M34 29.5v0"/>
    """,
    # Monitor / TV on a stand.
    "ewaste": """
      <rect x="6" y="9" width="36" height="24" rx="3"/>
      <path d="M18 40h12M24 33v7"/>
      <path d="M13 16h8"/>
    """,
    # Debris pile: broken planks stacked at angles.
    "reno-debris": """
      <path d="M6 38h36"/>
      <path d="M10 38l6-14 8 3-4 11"/>
      <path d="M24 38l10-16 6 4-4 12"/>
      <path d="M16 24l8 3"/>
    """,
    # Hot tub: tub shell, waterline, rising bubbles.
    "hot-tub": """
      <path d="M6 24h36v10a5 5 0 0 1-5 5H11a5 5 0 0 1-5-5z"/>
      <path d="M6 29h36"/>
      <path d="M16 19c0-3 3-3 3-6M24 17c0-3 3-3 3-6M32 19c0-3 3-3 3-6"/>
    """,
    # Shed: pitched roof, door.
    "shed-deck": """
      <path d="M6 22L24 8l18 14"/>
      <path d="M10 22v18h28V22"/>
      <path d="M20 40V29h8v11"/>
    """,
    # Concrete: stacked broken slabs.
    "concrete": """
      <path d="M5 38h38"/>
      <path d="M8 38v-8h14v8"/>
      <path d="M22 38v-11h16v11"/>
      <path d="M12 30v-6h14v6"/>
    """,
    # Branch with leaves.
    "yard-waste": """
      <path d="M24 42V14"/>
      <path d="M24 26c-8 0-12-4-12-10 6 0 12 3 12 10z"/>
      <path d="M24 20c8 0 12-4 12-10-6 0-12 3-12 10z"/>
      <path d="M24 34c-6 0-9-3-9-7 5 0 9 2 9 7z"/>
    """,
    # House with a packed box beside it.
    "estate": """
      <path d="M5 21L18 10l13 11"/>
      <path d="M8 21v17h20V21"/>
      <path d="M32 26h11v12H32z"/>
      <path d="M32 31h11M37.5 26v5"/>
    """,
    # Stacked pipe / bar ends.
    "scrap-metal": """
      <circle cx="14" cy="31" r="7"/>
      <circle cx="30" cy="31" r="7"/>
      <circle cx="22" cy="17" r="7"/>
    """,
    # Piano keyboard.
    "piano": """
      <rect x="5" y="14" width="38" height="20" rx="2"/>
      <path d="M14 14v13M23 14v13M32 14v13"/>
      <path d="M5 27h38"/>
    """,
}

out = Path(__file__).parent
for name, body in ICONS.items():
    inner = " ".join(line.strip() for line in body.strip().splitlines())
    (out / f"icon-take-{name}.svg").write_text(f"{HEAD}{inner}</svg>\n", encoding="utf-8")

print(f"wrote {len(ICONS)} icons")
