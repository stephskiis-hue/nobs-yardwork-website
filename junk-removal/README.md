# No BS Junk Removal — Winnipeg

Static site for the junk removal division of **No-BS Yardwork**.
Target domain: `nobs-junk.com` — chosen, not yet registered. Until `SITE` in
`_build.py` is changed, the build still generates against `no-bs-junkremoval.com`.

Hand-coded static HTML, same stack as no-bs-yardwork.com: no framework, no
runtime dependencies, deploys by FTP to cPanel/Apache.

> **Not in its own repo yet.** See [MIGRATE.md](MIGRATE.md) for the one command
> that moves it, and why it started here.

---

## Before this goes live

These are the things only you can do. Nothing on this list is code.

- [ ] **Register `nobs-junk.com`** (it was available in September 2026), then
      change `SITE` at the top of `_build.py` and rebuild. Every canonical,
      sitemap entry and share link is generated from that one line.
- [ ] **Add the addon domain** in cPanel and note its document root
- [x] **Set the prices.** Done: $139 minimum up to $689 for a full trailer, plus
      per-tonne rates for heavy material. A price appears in three places; the
      comment at the top of `_pages/pricing.html` lists them.
- [ ] **Uncomment the canonical-host rule** in `.htaccess` — *only after* DNS
      resolves. Doing it early makes the site unreachable.
- [ ] **Replace the stock photos** with real job photos. Seven service pages use
      Unsplash stock today; the shot list is below.
- [ ] **Add your liability coverage amount** to the box on `_pages/about.html`
- [ ] **Test the quote form** once, for real. It is a JotForm embed
      (`262378273577268`, "Clone of Request for Quote"), so submissions land in
      your JotForm account — there is no server-side mail to fail.
- [ ] **Finish verifying the Google Business Profile.** It exists but is not
      verified, and an unverified listing does not appear in the map pack, which
      is where most of these customers click. Then make the site's street address
      match it exactly — `_build.py` currently has "Lakewood Blvd" with no number.
- [ ] **Search Console** property + submit `sitemap.xml`
- [ ] **Check the Tag Manager container** (`GTM-M3MHCKF5`). The site loads Tag
      Manager *and* Google Analytics (`G-VN2QZ4KXXH`) separately, which likely
      counts every visit twice. If the container holds only Analytics, remove Tag
      Manager; if it holds an Ads tag or a Meta pixel, keep it and remove the
      separate Analytics tag instead.
- [ ] **Create a separate GA4 property** for the junk division. The current ID
      belongs to the yardwork site, so the two businesses' leads are mixed.

---

## Photos still needed

**This changed.** Seven Unsplash-licensed stock photos now sit on the service
pages — see [`images/CREDITS.md`](images/CREDITS.md) for what each one shows and
the licence terms. The old labelled placeholder blocks are gone.

Stock is a stopgap, not the goal. Real photos of your own crew and equipment
beat it on trust and on local SEO, because Google favours original imagery. Drop
a replacement in at the same filename and it swaps everywhere with no other
change. The shot list below is still the brief worth shooting to.

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
python3 _build.py      # 34 .html files + sitemap.xml + feed.xml + llms.txt
python3 _serve.py      # preview at http://localhost:8000
```

- **Page content** → `_pages/<name>.html` (plain HTML fragments)
- **What we take** → `_categories.py`: every category, every item, and the
  things we can't take. The hub, the A–Z index, each category page's item list,
  the homepage list and the structured data are all generated from it.
- **Blog posts** → `_pages/blog/<slug>.html` plus an entry in `POSTS`
- **Header, footer, nav, schema, page titles** → `_build.py`
- **Styling** → `css/junk.css`

The generated `.html` files are committed, so the site works for anyone who never
runs the script.

**Prefer no build step?** Run `_build.py` once, delete it along with `_pages/`,
and hand-edit the `.html` files from then on. Nothing else depends on it.

### The blog

Eight posts live at `/blog`, covering pricing, bin-vs-crew, heavy material, hot
tubs, estate cleanouts, recycling, winter work and job prep. Each one links back
into the relevant service pages, which is most of the point of having them.

Adding a post is two files and one command — the full walkthrough is in
[`DEPLOY.md`](DEPLOY.md#adding-a-blog-post-later). The important part is that a
post is **defined once**, in the `POSTS` list. The index card, breadcrumb,
`BlogPosting` structured data, sitemap entry with `lastmod`, RSS item and the
related-posts strip are all derived from that entry. There is no second place to
update, so the index and the feed cannot drift away from the posts.

Posts sit in a real `blog/` subdirectory, so they reach shared assets through
`../`. That prefix comes from the `{BASE}` token — see `render_nav()` for why the
site stays on relative paths rather than switching to root-relative ones.

**Author attribution** is set to the business (`BLOG_AUTHOR` in `_build.py`)
rather than to Stephano or Ben by name, because these are company positions and
putting first-person opinions under a real person's byline is your call to make,
not the generator's. Change `BLOG_AUTHOR` and the `author` block in
`blog_posting_schema()` to a `Person` if you would rather they were signed.

### Previewing it yourself

From inside the folder:

```bash
python3 _serve.py
```

Then open <http://localhost:8000>. Python is already on macOS and most Linux; on
Windows install it from python.org.

**Double-clicking `index.html` no longer works, and neither does
`python3 -m http.server`.** Internal links are extensionless (`/pricing`, not
`/pricing.html`) because that is the canonical address, and linking to the
`.html` form cost a 301 redirect on every click. On the real server `.htaccess`
maps `/pricing` to `pricing.html`. Opening the files directly, or using Python's
plain server, has no such rule, so every link 404s. `_serve.py` is Python's
built-in server plus that one rule, and nothing more.

**On the live server**, once the addon domain is pointed at this folder, it is
just the domain in a browser. To check a change before it is public, upload to a
staging subfolder rather than the document root.

### Deploying to Railway (always-on staging URL)

`Dockerfile` + `deploy/` give you a live URL that redeploys on every push.

It runs **php:apache**, not a static file server, on purpose: production is
cPanel + Apache, so this image runs the *same* `.htaccess` the real host will.
Extensionless URLs, the 404 page, gzip and cache headers all behave exactly as
they will in production.

Setup:

1. Railway → **New Project → Deploy from GitHub repo** → pick this repo.
2. **Settings → Source → Branch** → `claude/no-bs-junk-removal-site-vn1784`
   (or `main` once this is merged).
3. Root Directory does not need setting. There is a `Dockerfile` at the repo
   root that copies `junk-removal/` into the web root, so Railway serves the
   junk removal site either way. Setting Root Directory to `junk-removal` also
   works — it just uses `junk-removal/Dockerfile` instead, which builds the
   same image.
4. Railway auto-detects the Dockerfile. No build command, no start command, no
   environment variables needed — `$PORT` is handled in `deploy/entrypoint.sh`.
5. **Settings → Networking → Generate Domain** for the `*.up.railway.app` URL.

Verified locally with `docker build` + `docker run`: all extensionless URLs
return 200, `/pricing.html` 301s to `/pricing`, the custom 404 renders, gzip and
cache headers are applied, build tooling under `_pages/`, `_build.py`, `deploy/`
and `Dockerfile` returns 403, and the quote form POSTs through to `thanks.html`
with validation, the honeypot and the header-injection guard all behaving.

### If a deploy crashes on boot

`deploy/entrypoint.sh` validates the Apache config and prints what it did before
handing off, so **Deploy Logs name the cause** rather than reporting a bare exit
code. Read them first; the last line before the failure is the reason.

One failure has already been seen and is now handled automatically:

> `AH00534: apache2: Configuration error: More than one MPM loaded.`

Apache refuses to start with two Multi-Processing Modules loaded. A clean
`php:8.2-apache` ships only `mpm_prefork`, and nothing in this repo asks for a
second one — Railway's **build cache** served a base image that already had
`mpm_event` enabled alongside it, so every boot died before Apache came up and
the URL returned `502 Application failed to respond`.

The repair lives in the entrypoint, not the Dockerfile, and deliberately so: a
cached build layer is what introduced the problem, so a fix baked into another
build layer can be cached straight past it. At container start the entrypoint
removes every MPM symlink and re-links `mpm_prefork` (required by `mod_php`,
which is not thread-safe). Whatever the image contains, Apache boots with one
MPM. The startup log records it:

```
  MPM loaded: mpm_event.load mpm_prefork.load
    -> corrected to mpm_prefork only
```

If a deploy still fails after this, the safe first move is **Redeploy without
cache** in Railway, which discards the poisoned base layer.

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

The brand palette comes from the tokens `custom.css` declares, so this site and
the lawn site stay in step and re-syncing the parent's palette updates this one
for free:

| Token | Value | Used for |
|---|---|---|
| `--primary-color` | `#0B3D2C` | dark green — header, footer, dark bands, headings |
| `--accent-color` | `#2A7D2E` | brand green — buttons, icons, highlights |
| `--secondary-color` | `#F0FFF0` | honeydew — alternating section bands |
| `--divider-color` | `#E7ECEA` | card borders, table rules |
| `--text-color` | `#555555` | body copy |
| `--white-color` | `#FFFFFF` | page ground |

`junk.css` adds three tokens of its own, each for a job the palette above cannot
do legibly. The ratios are measured:

| Token | Value | Used for |
|---|---|---|
| `--accent-on-dark` | `#6FCF7C` | green **text** on the dark green. The brand accent measures 2.37:1 there and fails WCAG; this is 6.34:1 |
| `--warning-color` | `#9B2C2C` | "we can't take this" — 7.53:1 on white |
| `--warning-tint` | `#FDECEC` | behind the warning label — the red is 6.59:1 on it |

White page, green furniture — the same arrangement as no-bs-yardwork.com. If you
need a new colour, add it as a token first; don't hard-code a hex in a component
rule. The green button on white measures 5.16:1, which passes WCAG AA.

**Use `--accent-color` for green on light backgrounds and `--accent-on-dark` for
green text on dark ones.** Using the first on the second is exactly how the
homepage headline came to fail contrast.

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

The quote form is a JotForm embed (no JavaScript
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

34 pages are built: the 12 category pages, the What We Take hub, the A–Z index
of every item, the what-we-can't-take page, commercial, winter, about,
where-your-junk-goes, reviews, quote, pricing, 404, thanks, and the blog index
with eight posts. Still to come:

- **Neighbourhood pages.** Worth doing properly or not at all: 25 near-identical
  pages with the place name swapped is thin content that Google ignores and
  customers see through. Each needs a real local job, a real photo and a real
  local detail, so these wait on job photos.
