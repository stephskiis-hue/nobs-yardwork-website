# Deploying the No-BS Yardwork Website

How site updates reach **https://no-bs-yardwork.com**.

> **TL;DR — to update the live site:** make your edits, then get them onto the
> **`main`** branch (merge the working branch, or push to `main`). The GitHub
> Action publishes to the server over FTP within about a minute. Edits on any
> other branch do **not** deploy.

---

## How the site actually updates

There are two real deploy paths (an earlier version of this doc wrongly said
GitHub doesn't deploy — it does):

1. **GitHub Actions — primary, automatic.**
   `.github/workflows/deploy.yml` runs on every **push to `main`** (and can be
   run manually from the Actions tab). It uses `lftp` to upload the site to
   `/public_html/` on the server over FTP. Credentials come from repository
   **secrets**: `FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`.

2. **Blog autopilot — for blog posts only.**
   `_blog-autopilot.py` uploads new posts directly over FTP using
   `_blog-ftp.env` (keys `FTP_HOST`, `FTP_USER`, `FTP_PASS`, `FTP_PATH`). This
   is separate from GitHub and has been the thing actually keeping the site
   current while the GitHub deploy was failing.

3. **Manual targeted deploy — optional helper.**
   `_deploy.py <files>` uploads specific files over FTP from a machine that has
   `_blog-ftp.env` (e.g. your local computer). Useful for a quick one-off push
   without going through `main`. Example: `python3 _deploy.py projects.html`

---

## ⚠️ The GitHub deploy needs correct FTP secrets

Every GitHub deploy so far has failed with **`530 Login authentication
failed`** — the workflow reaches the server (port 21) but the stored login is
wrong. Fix it under **Settings → Secrets and variables → Actions**:

| Secret | What it is | Value (from your working `_blog-ftp.env`) |
|---|---|---|
| `FTP_SERVER` | FTP host / IP | `FTP_HOST` |
| `FTP_USERNAME` | FTP user | `FTP_USER` |
| `FTP_PASSWORD` | FTP password | `FTP_PASS` |

After updating the secrets, push to `main` (or re-run the latest deploy from
the Actions tab) and confirm it goes green.

> Note: the login line uses `open -u user,password`. If the password contains a
> **comma or space**, that form breaks even when the password is correct — say
> so and the login can be hardened.

---

## Safety notes (important)

- The deploy uses `mirror --reverse` **without `--delete`**, and **excludes the
  WordPress `blog/` directory**. So it never deletes remote files and never
  overwrites the live WordPress install or its uploads. (The previous
  `--delete` would have wiped `wp-config.php`, `/uploads/`, and `.htaccess` on
  the first successful run.)
- Never commit `_blog-ftp.env` or real credentials. Secrets live in
  `_blog-ftp.env` locally and in GitHub repository secrets for CI.

---

## Where deploys can run

| Environment | Deploy works? | Why |
|---|---|---|
| **GitHub Actions** (push to `main`) | ✅ once secrets are correct | GitHub's runners can reach FTP |
| **Your local machine** | ✅ | `_blog-ftp.env` present, FTP allowed (`_deploy.py` / blog robot) |
| **claude.ai web app** (this cloud session) | ❌ | sandbox blocks outbound FTP entirely; edits here must be pushed to `main` so the Action deploys them |
