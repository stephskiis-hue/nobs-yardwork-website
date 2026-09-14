# Editing this site on your own machine

## Get the code

```bash
git clone --branch junk-site-main --single-branch --depth 1 \
  https://github.com/stephskiis-hue/nobs-yardwork-website.git no-bs-junk
cd no-bs-junk
```

`junk-site-main` is the branch where this site sits at the top level, with no
`junk-removal/` folder wrapped around it. `--depth 1` matters: the full history
is about **164 MB**, because the lawn repo carries a WordPress install you have
no use for. This gets you a few MB instead.

## What you need

**Python 3. That is the entire list.**

`_build.py` imports only `html`, `json`, `re`, `datetime`, `email.utils` and
`pathlib` — all standard library. No `pip install`, no virtualenv, no Node, no
build tools. Python 3 already ships on macOS and Linux; on Windows get it from
python.org and tick "Add Python to PATH".

Check it works:

```bash
python3 --version     # Windows: python --version
```

## See the site

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000>. Stop it with Ctrl-C.

You can also just double-click `index.html`. Everything works except the clean
URLs — links go to `/pricing.html` instead of `/pricing`. That is cosmetic; the
real server rewrites them.

---

## The one thing that will waste your time

**Do not edit the `.html` files in the top level of the folder.**

`index.html`, `pricing.html`, `about.html` and the other 29 are **generated**.
They are the *output* of `_build.py`. Edit one, run the build, and your change
is gone — no warning, no error, just gone.

This is not an accident. The lawn site has its header and footer copy-pasted
into 47 separate files, so changing one nav link means 47 identical edits and
one of them always gets missed. Here the shared parts live in one place.

Edit the **sources** instead:

| To change | Edit | Then |
|---|---|---|
| Words on a page | `_pages/<page>.html` | `python3 _build.py` |
| A blog post | `_pages/blog/<slug>.html` | `python3 _build.py` |
| Nav menu, footer links | `NAV` / `FOOTER_LINKS` in `_build.py` | `python3 _build.py` |
| Page titles, meta descriptions | the `PAGES` list in `_build.py` | `python3 _build.py` |
| Phone, email, form ID | the constants at the top of `_build.py` | `python3 _build.py` |
| Colours, spacing, layout | `css/junk.css` | nothing — CSS is not generated |
| A photo | drop the new file in `images/` at the same filename | nothing |

So the loop is: **edit a source file → `python3 _build.py` → refresh the browser.**

```bash
python3 _build.py
```

```
built 32 pages + sitemap.xml + feed.xml + llms.txt (8 posts, 52 FAQs)
```

If it prints an error instead, it is telling you something real — a missing
fragment, or an FAQ block that does not match its schema. It refuses to build a
broken site rather than writing one out.

---

## Common jobs

### Set the real prices

Every price is a `$XXX` placeholder that renders as a dashed green box, so none
can go live by accident. They are all in one commented block at the top of
`_pages/pricing.html`, plus three teasers in `_pages/index.html`.

Replace each `$XXX` with your number **and delete the surrounding
`<span class="price-tbd">` and `</span>`**, then rebuild. This is the last real
blocker before launch.

### Change the quote form

The form on `/quote` is a JotForm embed. The form ID is set once, as
`JOTFORM_ID` in `_build.py`. Point it at a different form by changing that line
and rebuilding — do not edit the ID inside `_pages/quote.html`.

### Add a blog post

Two files and one command — full walkthrough in
[`DEPLOY.md`](DEPLOY.md#adding-a-blog-post-later). Write the body as
`_pages/blog/your-slug.html`, add a `BP(...)` entry to the `POSTS` list in
`_build.py`, rebuild. The index card, breadcrumb, structured data, sitemap
entry, RSS item and related-posts strip all come from that one entry.

### Swap a stock photo for a real one

Save your photo over the existing filename in `images/` — e.g. replace
`images/furniture-removal.webp` — and it changes everywhere. No rebuild needed,
no HTML to touch. Keep it roughly 3:2 and around 1000px wide.

Worth doing: your own job photos beat stock on trust and on local search,
because Google favours original imagery. See
[`images/CREDITS.md`](images/CREDITS.md) for what is stock today.

---

## Saving your changes

If you just want the files, you are done — edit and upload.

To keep your history and push back to GitHub:

```bash
git add -A
git commit -m "Set real prices"
git push
```

A shallow clone (`--depth 1`) can push fine. If git ever complains about the
shallow history, run `git fetch --unshallow` once.

## Putting it live

See [`DEPLOY.md`](DEPLOY.md). Short version: upload everything except
`_pages/`, `_build.py`, `deploy/`, `.github/` and the `.md` files to your
document root, and make sure the hidden `.htaccess` goes up with it.

## If you would rather not have a build step

Run the build one final time, then:

```bash
rm -rf _pages _build.py
```

From then on you hand-edit the 32 `.html` files directly and there is no tooling
at all. The cost is permanent: every future nav or footer change means editing
all 32 files by hand. Worth it only if you are certain you will never touch the
shared parts again.
