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
      dashed green box. They are all in one commented block at the top of
      `_pages/pricing.html`, plus three teasers in `_pages/index.html`.
- [ ] **Uncomment the canonical-host rule** in `.htaccess` — *only after* DNS
      resolves. Doing it early makes the site unreachable.
- [ ] **Take the photos.** Every missing shot is marked on-page with a green
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
| `junk-furniture.webp` | Sectional coming out a front door, floor protection down, frame padded |
| `junk-furniture-before.webp` / `-after.webp` | Cluttered living room, then the same frame swept |
| `junk-mattress.webp` | Sealed mattress bag being carried out — the detail that sells the service |
| `junk-ewaste.webp` | Trailer of stacked TVs and monitors, ideally at the recycler |
| `junk-reno-debris.webp` | Trailer backed up to a reno in progress, trades still working |
| `junk-shed-before.webp` / `-after.webp` | Leaning shed, then clean bare ground. Best pair on the site |
| `junk-yard-waste.webp` | Trailer heaped with branches after a hedge removal or storm |
| `junk-estate-before.webp` / `-after.webp` | Full room then empty — use a garage or basement, not a bedroom |
| `junk-scrap-metal.webp` | Full metal load, ideally on the scale at the yard |
| `junk-piano.webp` | Upright coming down a staircase on dollies with straps |

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
python3 _build.py      # regenerates all 23 .html files + sitemap.xml
```

- **Page content** → `_pages/<name>.html` (plain HTML fragments)
- **Header, footer, nav, schema, page titles** → `_build.py`
- **Styling** → `css/junk.css`

The generated `.html` files are committed, so the site works for anyone who never
runs the script.

**Prefer no build step?** Run `_build.py` once, delete it along with `_pages/`,
and hand-edit the `.html` files from then on. Nothing else depends on it.

### Previewing it yourself

**Quickest — open one file.** Download the repo (GitHub → green **Code** button →
**Download ZIP**), unzip, and double-click `index.html`. It opens in your browser
and every link works. Nothing to install.

The only thing that misbehaves this way is the extensionless URLs — clicking
around uses the `.html` filenames, which is exactly what happens on the real
server before `.htaccess` rewrites them. Cosmetic only.

**Closer to the real thing — run a local server.** From inside the folder:

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000> . Python is already on macOS and most Linux;
on Windows install it from python.org, or use `npx serve` if you have Node.

**On the live server**, once the addon domain is pointed at this folder, it is
just the domain in a browser. To check a change before it is public, upload to a
staging subfolder rather than the document root.

### Deploying to Railway (always-on staging URL)

`Dockerfile` + `deploy/` give you a live URL that redeploys on every push.

It runs **php:apache**, not a static file server, on purpose: production is
cPanel + Apache + PHP, so this image runs the *same* `.htaccess` and the *same*
`form-process.php`. Extensionless URLs, the 404 page, gzip, cache headers and
the quote form all behave exactly as they will on the real host.

Setup:

1. Railway → **New Project → Deploy from GitHub repo** → pick this repo.
2. **Settings → Root Directory → `junk-removal`.** Miss this and Railway tries
   to build the yardwork site instead.
3. Railway auto-detects the Dockerfile. No build command, no start command, no
   environment variables needed — `$PORT` is handled in `deploy/entrypoint.sh`.
4. **Settings → Networking → Generate Domain** for the `*.up.railway.app` URL.

Verified locally with `docker build` + `docker run`: all extensionless URLs
return 200, `/pricing.html` 301s to `/pricing`, the custom 404 renders, gzip and
cache headers are applied, build tooling under `_pages/`, `_build.py`, `deploy/`
and `Dockerfile` returns 403, and the quote form POSTs through to `thanks.html`
with validation, the honeypot and the header-injection guard all behaving.

### Sharing the staging link

**The Railway URL is public.** Anyone you send it to can open it — no login, no
allowlist. Share it freely with crew, family or a designer.

**`noindex` does not change that.** `deploy/railway.conf` sets
`X-Robots-Tag: noindex, nofollow, noarchive` on every response, which tells
*search engines* not to list the page. It has no effect on people with the link.
It is there because without it Google can index a staging copy carrying
placeholder prices, which then competes with the real no-bs-junkremoval.com
later — a duplicate-content mess that is tedious to unwind. The header lives in
the container config, not in `.htaccess`, so it can never follow the site to
production. Leave it on until the real domain is live.

**Link previews work.** Every page hard-codes `https://www.no-bs-junkremoval.com`
in its `canonical`, `og:url` and `og:image` — correct for production, but that
domain does not resolve yet, so a staging link pasted into Messenger, Slack or a
text message would show a preview card with no image and a dead click-through.
`deploy/entrypoint.sh` rewrites that host to the actual staging domain at serve
time, using Railway's own `RAILWAY_PUBLIC_DOMAIN` variable. Nothing to configure
— it happens as soon as you generate the domain. Set `PUBLIC_URL` yourself if
you host it somewhere other than Railway.

The committed HTML is untouched by this; it only changes what the container
sends.

**Every page carries a preview banner** — a green *PREVIEW SITE* strip under the
header explaining that the business is not live and the prices are placeholders.
It is injected at serve time by `railway.conf`, so it exists only on the staging
container and can never reach production. To remove it, delete the `Substitute`
line in `deploy/railway.conf`.

Both substitutions are scoped with `<FilesMatch "\.html$">` and
`SetOutputFilter` rather than `AddOutputFilterByType text/html`. The latter does
not reliably attach to an `ErrorDocument`, which meant the 404 page was silently
skipping both the banner and the host rewrite. Scoping to `.html` also keeps the
filter away from CSS, JS and images — verified byte-identical through the
container.

Two things to leave alone while you are on Railway:

- **Keep the canonical-host rule in `.htaccess` commented out.** Uncommenting it
  redirects the Railway URL to a domain that does not resolve yet.
- **The `.github/workflows/deploy.yml` FTP workflow is unrelated** and stays
  disabled. Railway and cPanel are separate paths; nothing here touches the live
  yardwork site.

Locally, the same image runs with:

```bash
docker build -t nobs-junk .
docker run --rm -p 8080:8080 nobs-junk    # then open http://localhost:8080
```

### Design system

`css/custom.css` is a **byte-identical copy** from no-bs-yardwork.com so it can be
re-synced from the parent later. Do not edit it — every junk-specific rule belongs
in `css/junk.css`, which loads after it.

**`junk.css` defines no colours of its own.** Every value comes from the tokens
`custom.css` already declares, so this site and the lawn site stay in step and
re-syncing the parent's palette updates this one for free:

| Token | Value | Used for |
|---|---|---|
| `--primary-color` | `#0B3D2C` | dark green — header, footer, dark bands, headings |
| `--accent-color` | `#2A7D2E` | brand green — buttons, icons, highlights |
| `--secondary-color` | `#F0FFF0` | honeydew — alternating section bands |
| `--divider-color` | `#E7ECEA` | card borders, table rules |
| `--text-color` | `#555555` | body copy |
| `--white-color` | `#FFFFFF` | page ground |

White page, green furniture — the same arrangement as no-bs-yardwork.com. If you
need a new colour, add it as a token first; don't hard-code a hex in a component
rule. The green button on white measures 5.16:1, which passes WCAG AA.

Two class-naming traps worth knowing, both already hit and fixed:

- **Don't name a section band `.bg-dark`.** Bootstrap defines `.bg-dark` with
  `!important` (`#212529`) and wins, painting the band charcoal. The dark green
  bands use `.bg-forest`.
- **Don't put an icon path in a CSS custom property set on the element.** A
  `url()` inside a custom property resolves relative to the *stylesheet* that
  substitutes it, not the document, so `images/x.svg` became `css/images/x.svg`
  and 404'd. The What We Take icon masks are declared in `junk.css` with
  `../images/` paths.

---

## Deviations from the parent site (all deliberate)

| | Why |
|---|---|
| No `.preloader` | On the parent it is a full-screen overlay removed only by jQuery. If a script fails, the site is a green screen. Not worth the risk. |
| No `text-anime-style-2` on headings | The GSAP SplitText treatment adds an invisible-text failure mode and delays the largest contentful paint. Plain headings are faster and safer. |
| `css/all.min.css`, not `css/all.css` | The parent's `index.html` requests `all.css`, which does not exist on the server. |
| No `aggregateRating` in the structured data | The 4.9/23 rating belongs to the landscaping business. Claiming it here would be a Google structured-data violation. It goes in once this division earns its own. |
| Reviews labelled "From No-BS Yardwork" | They are genuine, but they are not junk removal reviews. Labelling them is the whole point of the brand name. |
| Solid dark-green sticky header, not the parent's transparent one | The parent's header is transparent until you scroll, which relies on a dark hero image sitting behind it. With the hero photo slot still empty that would leave white nav text on white. Same `#0B3D2C` as the parent's scrolled state. |

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
    backgroundColor: "#2A7D2E",
    fontColor: "#FFFFFF",
    type: "1", height: 500, width: 700, openOnLoad: false
  });
</script>
<a class="btn-default lightbox-260105131967250">Request a quote</a>
```

---

## Not built yet

The blueprint specifies ~45 pages. 23 are built: all 12 "What We Take"
categories now have their own page, plus commercial, winter, about, where-your-
junk-goes, reviews, quote, pricing, the hub, 404 and thanks. Still to come:

- Service-area pages. Worth doing properly or not at all: the blueprint's own
  warning is that 25 near-identical pages with the place name swapped is thin
  content that Google ignores and customers see through. Each needs a real local
  job, a real photo and a real local detail.
- Blog
