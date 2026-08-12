# Putting this site on a live server

The whole site is plain static HTML. There is no database, no build step on the
server, no Node, no framework. You copy the files up and it works.

The only moving part is **`form-process.php`**, which handles the quote form. If
your host has PHP (essentially all shared hosting does), it works with no setup.
If it does not, the form falls back to the JotForm embed and the phone number,
and you can simply not upload that one file.

---

## What to upload, and what to leave behind

Upload **everything except** the build tooling. None of it is secret, but a web
root is not the place for it:

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
`blog/`, `css/`, `js/`, `images/` and `webfonts/` must stay as folders. The site
uses relative paths throughout, which is deliberate: it means the whole thing
works unchanged whether it sits at a domain root or in a subfolder.

**`.htaccess` is easy to miss.** It starts with a dot, so most FTP clients and
file managers hide it by default. Without it you lose clean URLs, the custom 404
page, gzip and caching. Turn on "show hidden files" and confirm it arrived.

---

## Option A — cPanel or any shared Apache host

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

## Option B — a VPS running nginx

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
- [ ] **The form**: send yourself a test through `/quote` and confirm it arrives
      and lands on `/thanks`.
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
- Decide whether this division gets its own GA4 property and JotForm, or keeps
  sharing the yardwork ones. The IDs are at the top of `_build.py`.

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

**Form does not send** — PHP is not enabled, or the host blocks `mail()`. Many
shared hosts do. The JotForm embed on `/quote` works regardless and needs no
server support at all.

**Everything redirects to a dead domain** — the canonical-host block in
`.htaccess` was uncommented before DNS resolved. Comment it out again.
