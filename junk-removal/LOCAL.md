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

`_build.py`, `_categories.py` and `_serve.py` use only the Python standard
library. No `pip install`, no virtualenv, no Node, no build tools. Python 3
already ships on macOS and Linux; on Windows get it from python.org and tick
"Add Python to PATH".

Check it works:

```bash
python3 --version     # Windows: python --version
```

## See the site

```bash
python3 _serve.py
```

Then open <http://localhost:8000>. Stop it with Ctrl-C.

**Do not double-click `index.html`, and do not use `python3 -m http.server`.**
Both show the first page fine, then every link 404s. The site's links are
extensionless — `/pricing`, not `/pricing.html` — because that is the real
address, and the live server's `.htaccess` maps one to the other. Opening files
directly has no such rule, and neither does Python's plain server. `_serve.py`
is that plain server plus the one rule.

---

## The one thing that will waste your time

**Do not edit the `.html` files in the top level of the folder.**

`index.html`, `pricing.html`, `about.html` and the other 31 are **generated**.
They are the *output* of `_build.py`. Edit one, run the build, and your change
is gone — no warning, no error, just gone.

This is not an accident. The lawn site has its header and footer copy-pasted
into 47 separate files, so changing one nav link means 47 identical edits and
one of them always gets missed. Here the shared parts live in one place.

Edit the **sources** instead:

| To change | Edit | Then |
|---|---|---|
| Words on a page | `_pages/<page>.html` | `python3 _build.py` |
| What we take: any category or item | `_categories.py` | `python3 _build.py` |
| A blog post | `_pages/blog/<slug>.html` | `python3 _build.py` |
| Nav menu, footer links | `NAV` / `FOOTER_LINKS` in `_build.py` | `python3 _build.py` |
| Page titles, meta descriptions | the `PAGES` list in `_build.py` | `python3 _build.py` |
| Phone, email, form ID, domain | the constants at the top of `_build.py` | `python3 _build.py` |
| Colours, spacing, layout | `css/junk.css` | nothing — CSS is not generated |
| A photo | drop the new file in `images/` at the same filename | nothing |

So the loop is: **edit a source file → `python3 _build.py` → refresh the browser.**

```bash
python3 _build.py
```

```
built 34 pages + sitemap.xml + feed.xml + llms.txt (8 posts, 52 FAQs)
```

If it prints an error instead, it is telling you something real, and it names
the page. It refuses to write out a broken site. The things it checks:

- a page whose fragment is missing
- an FAQ block that does not match its structured data
- a title over 60 characters, or a description outside 120–158 characters —
  past those, Google cuts them off in search results
- an item listed twice in `_categories.py`, or a category with too few items

---

## Common jobs

### Add something you take

Open `_categories.py`, find the right category, and add a line:

```python
I("Air hockey table",
  "Long, flat and heavier than it looks, with a blower motor inside. The legs "
  "come off before it moves.",
  aka=["Foosball table"]),
```

The **note** should be something true and specific: what makes it awkward, what
it weighs, where it goes in Winnipeg. `aka` is any other word people search for
the same thing. Rebuild, and it appears on its category page, in the A–Z, on the
homepage list and in the structured data, all at once.

The top of `_categories.py` explains the rules in full, including where the
things you *cannot* take go.

### Change a price

A price appears in **three places**, and they have to match, or the pricing
page, the homepage and the structured data Google reads will disagree:

1. the rate table in `_pages/pricing.html`
2. the three teaser rows in `_pages/index.html`
3. `priceRange` in `_build.py`

The comment at the top of `_pages/pricing.html` lists them. Change all three,
then rebuild.

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
git commit -m "Add air hockey tables to what we take"
git push
```

A shallow clone (`--depth 1`) can push fine. If git ever complains about the
shallow history, run `git fetch --unshallow` once.

## Putting it live

See [`DEPLOY.md`](DEPLOY.md). Short version: upload everything except
`_pages/`, the three `.py` files, `deploy/`, `.github/` and the `.md` files to
your document root, and make sure the hidden `.htaccess` goes up with it.

If a `.py` file does get uploaded by accident, `.htaccess` refuses to serve it.

## If you would rather not have a build step

Run the build one final time, then:

```bash
rm -rf _pages _build.py _categories.py
```

From then on you hand-edit the 34 `.html` files directly and there is no tooling
at all. The cost is permanent: every nav or footer change means editing all 34
files by hand, and adding one item you take means updating the hub, the A–Z,
its category page and the homepage separately. Worth it only if you are certain
you will never touch any of that again.
