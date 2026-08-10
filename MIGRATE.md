# Moving this into its own GitHub repo

This site was built to be a **standalone repository**. It currently lives as a
subdirectory of `nobs-yardwork-website` for one reason: the session that built it
was bound to that repository and could not create a new one on GitHub
(`POST /user/repos` is blocked at the proxy — "sessions are bound to their
configured repositories").

Nothing about the site depends on that arrangement. Every asset path is relative
and no file reaches outside this directory, so moving it is a copy.

---

## Option A — move it, keeping the git history (recommended)

`git subtree split` extracts this directory's commits into a branch where these
files sit at the root, then pushes that branch to the new repo.

```bash
# 1. On github.com, create a new PRIVATE repo: no-bs-junkremoval-website
#    Do NOT initialise it with a README, .gitignore or licence.

# 2. From a clone of nobs-yardwork-website, on the branch holding this work:
git subtree split --prefix=junk-removal -b junk-site

# 3. Push that branch as the new repo's main branch:
git push https://github.com/stephskiis-hue/no-bs-junkremoval-website.git junk-site:main

# 4. Clone the new repo somewhere fresh and check it:
git clone https://github.com/stephskiis-hue/no-bs-junkremoval-website.git
cd no-bs-junkremoval-website
python3 -m http.server 8000     # then open http://localhost:8000/
```

## Option B — plain copy, fresh history

Simpler, loses the commit history for these files.

```bash
mkdir ~/no-bs-junkremoval-website
cp -r junk-removal/. ~/no-bs-junkremoval-website/
cd ~/no-bs-junkremoval-website
git init -b main
git add -A
git commit -m "Initial commit: No BS Junk Removal Winnipeg site"
git remote add origin https://github.com/stephskiis-hue/no-bs-junkremoval-website.git
git push -u origin main
```

Note that `cp -r junk-removal/.` (with the trailing `/.`) copies the dotfiles too
— `.htaccess`, `.gitignore` and `.github/`. Without it you would silently lose
the `.htaccess`, and the site would 404 on every extensionless URL.

---

## After the move

- `.github/workflows/deploy.yml` only starts working once these files are at a
  repo root. Read the comments at the top of it before enabling — it is disabled
  on purpose, and enabling it carelessly can delete the live yardwork site.
- Delete this file once the move is done.

## If you leave it where it is

That also works. As a subdirectory of `nobs-yardwork-website`, merging to `main`
publishes it to `no-bs-yardwork.com/junk-removal/` through the existing FTP
deploy, with no extra setup. You would then point the addon domain's document
root at `/public_html/junk-removal` and uncomment the canonical-host rule in
`.htaccess`.
