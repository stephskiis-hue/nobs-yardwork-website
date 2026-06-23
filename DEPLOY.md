# Deploying the No-BS Yardwork Website

This is the single source of truth for how edits get from files to the **live
site** at <https://no-bs-yardwork.com>.

> **TL;DR for Claude:** When the user says *"update the site"* / *"push that
> live"* / *"deploy it"*, run:
> ```
> python3 _deploy.py <files they changed>
> ```
> or to push everything that changed:
> ```
> python3 _deploy.py --all-changed
> ```
> This only works in a session that has the FTP credentials **and** is allowed
> to make outbound FTP connections (i.e. running locally — **not** the
> claude.ai web app). See "Where this works" below.

---

## The key thing to understand

**GitHub does NOT deploy this site.** Pushing to GitHub only updates the Git
repo. The live website is hosted on shared hosting (Moniker) and is updated by
**uploading files over FTP**. They are two separate worlds:

| Action | What it changes |
|---|---|
| `git push` | The GitHub repo only. **Live site unchanged.** |
| `python3 _deploy.py <file>` | The **live site** (uploads over FTP). |

So a normal workflow is: **edit → deploy (go live) → optionally commit to Git**
for history.

---

## How to deploy

```bash
# One page
python3 _deploy.py projects.html

# Several files at once
python3 _deploy.py index.html about.html css/custom.css

# A file in a subfolder (the folder structure is preserved on the server)
python3 _deploy.py images/blog-foo.webp

# Everything git currently sees as modified
python3 _deploy.py --all-changed

# Preview without uploading anything
python3 _deploy.py --dry-run projects.html
```

`_deploy.py` uses the **same FTP login and the same upload logic** as the blog
autopilot (`_blog-autopilot.py`), so if blog auto-posting works, deploying does
too.

> **Blog posts are special.** New blog posts should still go through
> `_blog-autopilot.py`, because that also fetches the image, updates
> `posts.json`, and patches the inline post list in `blog.html`. Use `_deploy.py`
> for everything else (regular pages, CSS, images, fixes).

---

## Credentials (one-time setup)

`_deploy.py` reads `_blog-ftp.env` in this folder — the **same file the blog
robot already uses**. If blog auto-posting is working on a machine, this file
already exists there and deploying needs no extra setup.

`_blog-ftp.env` format (this file is git-ignored and must **never** be committed):

```
FTP_HOST=ftp.your-host.com
FTP_PORT=21
FTP_USER=your-ftp-username
FTP_PASS=your-ftp-password
FTP_PATH=/public_html            # the remote web root that serves the site
SITE_URL=https://no-bs-yardwork.com
```

If `_blog-ftp.env` is absent, `_deploy.py` will also read these same names from
OS environment variables as a fallback.

---

## Where this works (important)

| Environment | Can deploy? | Why |
|---|---|---|
| **Your local machine** (Claude Code / terminal) | ✅ Yes | `_blog-ftp.env` is present and FTP is allowed. This is where the blog robot runs. |
| **claude.ai web app** (this cloud session) | ❌ No | The sandbox blocks all outbound FTP (port 21), and `_blog-ftp.env` isn't present. Edits can be made and pushed to GitHub here, but **going live must happen locally.** |

**Practical workflow when working from the web app:** Claude edits the files
and pushes them to the Git branch. To publish, pull the branch on your local
machine and run `python3 _deploy.py --all-changed` (or just ask Claude to do it
in a local session).
