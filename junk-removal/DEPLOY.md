# Putting this site on a live server

The whole site is plain static HTML. There is no database, no build step on the
server, no Node, no framework. You copy the files up and it works.

**There are no moving parts at all.** The quote form is a JotForm embed, so
submissions go to JotForm rather than through the server. That means:

- **No PHP required.** Any host that serves files will do — your cPanel, but
  equally Cloudflare Pages or Netlify, both free.
- **No mail() to fail.** The previous PHP handler mailed submissions and, when
  that failed, showed the customer a thank-you page while the lead vanished.
  JotForm stores every submission on their side, so nothing is lost silently.

---

## What to upload, and what to leave behind

`sh deploy/make-dist.sh` assembles a `dist/` folder containing exactly what
belongs on a server. Upload the *contents* of `dist/`, not the repo. If you
prefer to upload by hand, this is what the script leaves out, and why:

| Leave out | Why |
|---|---|
| `_pages/` | Source fragments. The finished pages are already built. |
| `_build.py` | The generator. Runs on your machine, not the server. |
| `images/_make-icons.py` | Same. |
| `deploy/` | Container config for Railway only. |
| `Dockerfile`, `.dockerignore`, `railway.json` | Container deploys only. |
| `.github/` | GitHub Actions config. |
| `README.md`, `DEPLOY.md`, `MIGRATE.md` | Documentation. |

Everything else goes up **as-is, keeping the folder structure** — in particular
`blog/`, `css/`, `js/` and `images/` must stay as folders. The site
uses relative paths throughout, which is deliberate: it means the whole thing
works unchanged whether it sits at a domain root or in a subfolder.

**`.htaccess` is easy to miss.** It starts with a dot, so most FTP clients and
file managers hide it by default. Without it you lose clean URLs, the custom 404
page, gzip and caching. Turn on "show hidden files" and confirm it arrived.

---

## Option A — Cloudflare Pages, deploying from GitHub (recommended)

Free, fast everywhere, HTTPS included, and it redeploys itself every time you
push. No FTP, no dragging folders, nothing to forget.

**Why this one.** The site is static files, which is exactly what Pages is for.
Its free plan carries unlimited static requests, 500 builds a month and up to
100 custom domains per project, and it strips `.html` from URLs automatically —
which is the same clean-URL shape `.htaccess` gives you on Apache, so every
link on this site works unchanged. Netlify is an equally good alternative with
the same shape of setup; the settings below translate directly.

### 1. Get the code on GitHub

The site currently lives in the `junk-removal/` folder of the lawn repo, on its
own branch. That is fine — Pages can build from a subfolder. Push the branch:

```bash
git push -u origin claude/no-bs-junk-removal-site-vn1784
```

(If you would rather it had its own repository, `MIGRATE.md` walks through that
and keeps the history. It is not required to go live.)

### 2. Create the project

In the Cloudflare dashboard: **Workers & Pages → Create → Pages → Connect to
Git**, pick the repo, then set:

| Setting | Value |
|---|---|
| Production branch | `claude/no-bs-junk-removal-site-vn1784` (or `main` after a migration) |
| Root directory | `junk-removal` |
| Build command | `sh deploy/make-dist.sh` |
| Build output directory | `dist` |

The build command runs `_build.py` and assembles `dist/` — the pages, CSS, JS
and images, and nothing else. Without it you would be publishing the generator
and the page sources too. Python 3 is already present in the build image, and
the site needs nothing else installed.

### 3. Check the preview URL

Every deploy gets a `*.pages.dev` address. Open it and run the checklist at the
bottom of this file **before** pointing the domain at it. Clean URLs, the blog,
the 404 page and the quote form are the four that matter.

### 4. Add the domain

**Custom domains → Set up a domain.** If the domain is registered at Cloudflare,
DNS is filled in for you; otherwise point the nameservers at Cloudflare first.
Add both the apex (`no-bs-junkremoval.com`) and `www`, and let Cloudflare
redirect one to the other so only one version is canonical.

HTTPS is automatic. There is no certificate to buy or renew.

### 5. From then on

Push to the branch and the site updates itself in about a minute. Every deploy
is kept, so a bad change can be rolled back from the dashboard in one click.

---

## Option B — cPanel or any shared Apache host

This is almost certainly the right option; it is the same kind of hosting
no-bs-yardwork.com already runs on.

### 1. Point the domain at a folder

In cPanel, **Domains → Create A New Domain**. Enter `no-bs-junkremoval.com` and
note the **Document Root** it gives you — usually something like
`/home/youruser/no-bs-junkremoval.com`.

> Write that path down and check it. Uploading to the wrong document root is
> how people overwrite their existing site. If the path says `public_html` with
> nothing after it, that is the **yardwork** site — stop and re-check.

### 2. Upload

Either **File Manager → Upload** with a zip and then Extract, or FTP with
FileZilla. Drop the contents of this folder (minus the table above) into the
document root.

### 3. Check the requirements

The `.htaccess` uses `mod_rewrite`, `mod_headers`, `mod_expires` and
`mod_deflate`. All four are standard on cPanel hosting and normally already on.
If clean URLs do not work after upload, `mod_rewrite` is the one to ask your
host about.

### 4. Turn on HTTPS

cPanel → **SSL/TLS Status** → run AutoSSL for the new domain. Free, and takes a
few minutes. Do not skip it — browsers now flag plain HTTP sites, and the site
links to itself over `https://` throughout.

### 5. After DNS resolves, force the canonical host

`.htaccess` has three commented lines near the top that redirect every visitor
to `https://www.no-bs-junkremoval.com`. **Leave them commented until the domain
actually resolves** — enabling them early sends every visitor to a domain that
does not answer, which takes the site down by every route at once.

Once `https://www.no-bs-junkremoval.com` loads in a browser, uncomment them.

---

## Option C — a VPS running nginx

The `.htaccess` does nothing on nginx, so its behaviour has to be expressed in
the server block instead. This config is the equivalent:

```nginx
server {
    listen 80;
    server_name no-bs-junkremoval.com www.no-bs-junkremoval.com;
    root /var/www/no-bs-junkremoval;
    index index.html;

    # Strip .html when someone types or links it explicitly (matches .htaccess).
    # `return` inside `if` is one of the few forms that is safe in nginx.
    if ($request_uri ~ ^/(.*)\.html(\?|$)) {
        return 301 /$1;
    }

    # Map a clean URL back to the file on disk, and a directory to its index.
    # $uri.html is what makes /blog/some-post work.
    location / {
        try_files $uri $uri.html $uri/ =404;
    }

    error_page 404 /404.html;

    # The quote form. Drop this block if you are not running PHP; adjust the
    # socket path to match your installed PHP version.
    location ~ \.php$ {
        include        fastcgi_params;
        fastcgi_pass   unix:/run/php/php8.2-fpm.sock;
        fastcgi_param  SCRIPT_FILENAME $document_root$fastcgi_script_name;
    }

    location ~* \.(jpg|jpeg|png|webp|svg|ico|css|js|woff|woff2)$ {
        add_header Cache-Control "public, max-age=31536000";
    }
    location ~* \.html$ {
        add_header Cache-Control "public, max-age=3600";
    }

    # Keep build tooling out of the web root even if it gets uploaded.
    location ~ ^/(_pages|deploy)/          { deny all; }
    location ~ ^/(_build\.py|Dockerfile|railway\.json|.*\.md)$ { deny all; }

    gzip on;
    gzip_min_length 512;
    gzip_types text/plain text/css text/xml application/javascript
               application/json image/svg+xml;
}
```

Then `sudo nginx -t && sudo systemctl reload nginx`, and get a certificate with
`sudo certbot --nginx -d no-bs-junkremoval.com -d www.no-bs-junkremoval.com`.

---

## After it is live — a short checklist

Open the site and confirm each of these. They are the things that actually break.

- [ ] `https://www.no-bs-junkremoval.com` loads with the green header and logo.
- [ ] **Clean URLs**: `/pricing` works, not just `/pricing.html`. If this fails,
      `.htaccess` did not upload or `mod_rewrite` is off.
- [ ] **The blog**: `/blog` shows eight cards, and `/blog/junk-removal-cost-winnipeg`
      opens the post with styling intact.
- [ ] **404**: visit `/does-not-exist` and confirm you get the branded page, not
      the host's default error.
- [ ] **The form**: send yourself a test through `/quote` and confirm it lands
      in your JotForm inbox. Do this once, for real — it is the only thing on
      the site that earns money.
- [ ] **Mobile**: open it on a phone. Check the hamburger menu opens and the
      call bar at the bottom works.
- [ ] `/sitemap.xml` and `/feed.xml` both load.

### Then tell Google it exists

1. **Google Search Console** → add the property → verify (the DNS TXT method is
   easiest with a new domain) → **Sitemaps** → submit `sitemap.xml`.
2. **Google Business Profile** — for a local trade this matters more than
   everything else on this page combined. A junk removal search in Winnipeg
   shows the map pack first.

### Things to fix before launch, not after

- Replace the `$XXX` placeholder prices in `_pages/pricing.html` with real
  numbers and re-run the build.
- Swap in real photos where the README's shot list calls for them.
- Decide whether this division gets its own GA4 property, or keeps sharing the
  yardwork one. The IDs are at the top of `_build.py`. The JotForm is already
  separate — `/quote` uses "Clone of Request for Quote"
  (`262378273577268`), not the lawn site's form.

---

## Adding a blog post later

Two files, then one command.

1. Write the article body as an HTML fragment at
   `_pages/blog/your-post-slug.html`. Copy an existing one to get the
   indentation and the available classes (`.lead-in`, `.callout`,
   `.table-scroll`, `h2`, `h3`, `ul`). Use `{BASE}` in front of internal links
   — `<a href="{BASE}pricing.html">` — because posts live one folder down.

2. Add an entry to the `POSTS` list in `_build.py`:

   ```python
   BP("your-post-slug",
      "Title That Appears In Google | No BS Junk Removal",
      "The headline shown on the page",
      "Short Crumb",
      "The meta description, about 150 characters.",
      "2026-09-01",
      "The teaser shown on the blog index card.",
      6, ["pricing"]),
   ```

3. Run `python3 _build.py` and upload the changed files.

The index card, the breadcrumb, the structured data, the sitemap entry, the RSS
item and the related-posts strip are all generated from that one entry. There is
no second place to update, which is the point.

---

## If something looks wrong

**Clean URLs 404** — `.htaccess` did not upload (it is hidden by default) or
`mod_rewrite` is off.

**Page loads but has no styling** — the `css/` folder did not upload, or it went
up as loose files instead of a folder. The structure has to be preserved.

**Blog posts unstyled but other pages fine** — posts are one directory deeper
and reach assets through `../`. That means `blog/` must sit *beside* `css/`, not
inside it.

**Quote form is blank or very short** — the JotForm iframe did not load.
Check the browser console for a blocked request. The page falls back to a
"call or text us" line beneath the form, so the visitor is never stranded.
Submissions live in your JotForm account, not on the server, so there is
nothing to check on the host.

**Everything redirects to a dead domain** — the canonical-host block in
`.htaccess` was uncommented before DNS resolved. Comment it out again.
