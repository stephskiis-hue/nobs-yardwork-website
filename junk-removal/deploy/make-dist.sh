#!/bin/sh
# Build the site and assemble dist/ — exactly what belongs on a web server,
# and nothing else.
#
# The repo root is not the web root. It also holds the generator (_build.py),
# the page sources (_pages/), the container config and the documentation. None
# of that is secret, but a web root is not the place for it, and on a host like
# Cloudflare Pages or Netlify every file in the published folder is downloadable.
#
# Used by the host's build command, and by hand before an FTP upload:
#
#     sh deploy/make-dist.sh && open dist
#
set -eu

cd "$(dirname "$0")/.."

python3 _build.py

rm -rf dist
mkdir -p dist

# Generated pages and the files search engines ask for.
cp ./*.html robots.txt sitemap.xml feed.xml llms.txt dist/

# Apache rewrite and caching rules. Ignored by Pages and Netlify, essential on
# cPanel — it costs nothing to carry, and forgetting it on an Apache host
# breaks every clean URL on the site.
if [ -f .htaccess ]; then cp .htaccess dist/; fi

# Asset folders, then strip the bits that are tooling or notes rather than site.
cp -R blog css js images fonts dist/
# Tooling that lives beside the assets it generates, and the photo credits
# note. .htaccess denies .py anyway, but a web root is not the place for it.
rm -f dist/images/*.py dist/images/CREDITS.md dist/fonts/*.py

files=$(find dist -type f | wc -l | tr -d ' ')
size=$(du -sh dist | cut -f1)
echo "dist/ ready: $files files, $size"
