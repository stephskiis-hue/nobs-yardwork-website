# No BS Junk Removal — Winnipeg

Static site for the junk removal division of **No-BS Yardwork**.
Target domain: `no-bs-junkremoval.com`

Hand-coded static HTML, same stack as no-bs-yardwork.com: no framework, no
runtime dependencies, deploys by FTP to cPanel/Apache.

> **Not in its own repo yet.** See [MIGRATE.md](MIGRATE.md) for the one command
> that moves it, and why it started here.

---

## Before this goes live

These are the things only you can do. Nothing on this list is code.

- [ ] **Register `no-bs-junkremoval.com`** (and `.ca`, redirected to it)
- [ ] **Add the addon domain** in cPanel and note its document root
- [ ] **Set the prices.** Every price is a `$XXX` placeholder rendered as a
      dashed orange box. They are all in one commented block at the top of
      `_pages/pricing.html`, plus three teasers in `_pages/index.html`.
- [ ] **Uncomment the canonical-host rule** in `.htaccess` — *only after* DNS
      resolves. Doing it early makes the site unreachable.
- [ ] **Take the photos.** Every missing shot is marked on-page with an orange
      dashed block containing the brief and the filename. See below.
- [ ] **Add your liability coverage amount** to the box on `_pages/about.html`
- [ ] **Test the quote form** end to end and check your spam folder — PHP
      `mail()` on shared hosting is unreliable. If it does not arrive, swap the
      form for the JotForm embed (snippet below).
- [ ] **Create a Google Business Profile** for the junk division. For this kind
      of business it out-earns the website as a lead source; do it before launch.
- [ ] **Search Console** property + submit `sitemap.xml`
- [ ] Decide whether you want a **separate GA4 property** (currently reusing the
      yardwork one, `G-VN2QZ4KXXH`, and GTM container `GTM-M3MHCKF5`)

---

## Photos still needed

No stock photography is used anywhere on this site, and none should be. Where a
real photo does not exist yet, the page shows a labelled placeholder with the
brief rather than a substitute. Drop the file in `images/` and replace the
`<div class="photo-slot">` block.

| File | Shot |
|---|---|
| `junk-hero.webp` | Crew + dump trailer in a real Winnipeg driveway, daylight, nobody posing. The single most important image on the site. |
| `junk-hottub.webp` | Hot tub cut into sections, deck and fence intact in frame |
| `junk-hottub-before.webp` / `-after.webp` | Same angle, tub in place then empty swept pad |
| `junk-appliances.webp` | Trailer with 4–6 appliances strapped in, crew for scale |
| `junk-appliance-stairs.webp` | Appliance dolly on basement stairs with floor protection |
| `junk-concrete-load.webp` | Loaded concrete trailer, ideally with the scale ticket visible |
| `junk-commercial-before.webp` / `-after.webp` | Cluttered lot or back alley, then the same frame cleared |
| `crew-*.webp` | The rest of the crew, for the About page |

For the hero, once `junk-hero.webp` exists, add to the `<section class="junk-hero">`
tag in `_pages/index.html`:

```html
style="background-image: url('images/junk-hero.webp')"
```

---

## Editing the site

The parent site has its header and footer hand-copied into 47 files, so changing
one nav item means 47 edits. This site does not repeat that.

```bash
python3 _build.py      # regenerates all 14 .html files + sitemap.xml
```

- **Page content** → `_pages/<name>.html` (plain HTML fragments)
- **Header, footer, nav, schema, page titles** → `_build.py`
- **Division styling** → `css/junk.css`

The generated `.html` files are committed, so the site works for anyone who never
runs the script. `python3 -m http.server 8000` serves it locally.

**Prefer no build step?** Run `_build.py` once, delete it along with `_pages/`,
and hand-edit the `.html` files from then on. Nothing else depends on it.

### Design system

`css/custom.css` is a **byte-identical copy** from no-bs-yardwork.com so it can be
re-synced from the parent later. Do not edit it — every junk-specific rule belongs
in `css/junk.css`, which loads after it.

The brand green (`--accent-color: #2A7D2E`) and dark green (`--primary-color:
#0B3D2C`) are inherited unchanged; that is the family link. The division layer
adds hi-vis orange `--division-color: #FF6B00`.

One rule worth knowing before you change a colour: **orange never pairs with
white text.** `#FF6B00` on white is 2.85:1 contrast, which fails WCAG AA. Orange
pairs with near-black `--on-division: #141414` (6.45:1) — which is also what
makes it read as safety signage. For orange *text* on a light background, use
`--division-text: #B84A00` (5.2:1).

---

## Deviations from the parent site (all deliberate)

| | Why |
|---|---|
| No `.preloader` | On the parent it is a full-screen overlay removed only by jQuery. If a script fails, the site is a green screen. Not worth the risk. |
| No `text-anime-style-2` on headings | The GSAP SplitText treatment adds an invisible-text failure mode and delays the largest contentful paint. Plain headings are faster and safer. |
| Solid sticky header, not transparent | Survives an empty hero image slot, legible on every page, and `position: sticky` gives an always-visible phone number with no JavaScript. |
| `css/all.min.css`, not `css/all.css` | The parent's `index.html` requests `all.css`, which does not exist on the server. |
| No `aggregateRating` in the structured data | The 4.9/23 rating belongs to the landscaping business. Claiming it here would be a Google structured-data violation. It goes in once this division earns its own. |
| Reviews labelled "From No-BS Yardwork" | They are genuine, but they are not junk removal reviews. Labelling them is the whole point of the brand name. |

---

## Lead capture

The quote form posts to `form-process.php` with a plain POST (no JavaScript
required) and redirects to `thanks.html`.

To route leads through the JotForm the yardwork site already uses, replace the
`<form>` block in `_pages/quote.html` with:

```html
<script src="https://cdn.jotfor.ms/s/static/latest/static/feedback2.js"></script>
<script>
  var JFL = new JotformFeedback({
    formId: "260105131967250",
    base: "https://form.jotform.com/",
    windowTitle: "Request a Junk Removal Quote",
    backgroundColor: "#FF6B00",
    fontColor: "#141414",
    type: "1", height: 500, width: 700, openOnLoad: false
  });
</script>
<a class="btn-default lightbox-260105131967250">Request a quote</a>
```

---

## Not built yet

The blueprint specifies ~45 pages. This is the core launch set (14). Still to come:

- The other 9 "What We Take" child pages (furniture, mattress, e-waste, reno
  debris, shed/deck, yard waste, estate, scrap metal, piano) — the hub page
  covers them with anchors for now
- Service-area pages. Worth doing properly or not at all: the blueprint's own
  warning is that 25 near-identical pages with the place name swapped is thin
  content that Google ignores and customers see through. Each needs a real local
  job, a real photo and a real local detail.
- Blog
