#!/bin/sh
# Container start-up for the staging deploy.
#
#   1. Bind Apache to whatever port the platform assigns.
#   2. Rewrite the production domain to the actual staging host, so shared
#      links get a working preview card instead of a broken one.
#   3. Validate the config and say so, loudly, before handing off to Apache.
#
# Step 3 matters because a crash here shows up in the platform's deploy log as
# a bare exit code. Everything below echoes what it did, so the log explains
# itself instead of needing a local reproduction.
set -e

echo "=== No BS Junk Removal — container start ==="

# ---------------------------------------------------------------------------
# 1. Port
#
# Railway and most PaaS pass the port in $PORT, and it is not always 80.
#
# ports.conf is REWRITTEN rather than sed-patched. The stock file carries
# `Listen 80` plus two `Listen 443` lines inside <IfModule> guards; a blanket
# substitution turns all three into the same port, which is harmless only for
# as long as mod_ssl stays disabled. Emitting a single Listen removes the
# possibility of an "Address already in use" bind failure entirely.
# ---------------------------------------------------------------------------
PORT="${PORT:-8080}"
printf 'Listen %s\n' "$PORT" > /etc/apache2/ports.conf
sed -i "s/<VirtualHost \*:[0-9]*>/<VirtualHost *:${PORT}>/" \
    /etc/apache2/sites-available/000-default.conf
echo "  port: ${PORT}"

# ---------------------------------------------------------------------------
# 2. Canonical / Open Graph host
#
# Every page hard-codes https://www.no-bs-junkremoval.com in its canonical,
# og:url and og:image. Correct for production, but on staging that domain does
# not resolve — so the link pasted into Slack or a text message renders a
# preview card with no image and a dead click-through. Rewriting the host at
# serve time fixes sharing without putting staging URLs in the committed HTML.
#
# RAILWAY_PUBLIC_DOMAIN is supplied by Railway once a domain is generated.
# PUBLIC_URL is the manual override for any other host.
# ---------------------------------------------------------------------------
DOMAIN="${PUBLIC_URL:-${RAILWAY_PUBLIC_DOMAIN:-}}"

if [ -n "$DOMAIN" ]; then
    case "$DOMAIN" in
        http://*|https://*) BASE="$DOMAIN" ;;
        *)                  BASE="https://$DOMAIN" ;;
    esac
    BASE="${BASE%/}"
    # Same FilesMatch scoping as railway.conf, and for the same reason: a 404
    # ErrorDocument does not pick up AddOutputFilterByType. Apache merges the
    # Substitute directives from both files, so the banner and this rewrite
    # both apply.
    cat > /etc/apache2/conf-enabled/zz-staging-host.conf <<CONF
<IfModule mod_substitute.c>
    <Directory /var/www/html>
        <FilesMatch "\.html\$">
            SetOutputFilter SUBSTITUTE
            Substitute "s#https://www.no-bs-junkremoval.com#${BASE}#n"
        </FilesMatch>
    </Directory>
</IfModule>
CONF
    echo "  canonical/OG host: ${BASE}"
else
    echo "  canonical/OG host: not set (no PUBLIC_URL or RAILWAY_PUBLIC_DOMAIN)."
    echo "    Shared-link previews will not load an image. Generate a domain in"
    echo "    Railway and redeploy to fix. Harmless for local runs."
fi

# ---------------------------------------------------------------------------
# 3. Force exactly one MPM
#
# Apache refuses to start with more than one Multi-Processing Module loaded:
#
#     AH00534: apache2: Configuration error: More than one MPM loaded.
#
# A clean `php:8.2-apache` ships only mpm_prefork, so this should never happen
# — but it did, on Railway, on every boot. The base image the build cache
# handed us had both mpm_prefork and mpm_event enabled. Nothing in this repo
# asks for that, which is exactly why it has to be corrected here rather than
# in the Dockerfile: a cached build layer is what introduced it, so a fix baked
# into another build layer can be cached straight past. This runs at container
# start, so whatever the image contains, Apache boots with one MPM.
#
# a2dismod is not used: it refuses to touch an MPM when it thinks the result
# would leave Apache without one, which is the very state being repaired.
# Removing the symlinks directly is unconditional.
#
# prefork specifically, because this image serves PHP through mod_php, which
# is not thread-safe and requires it.
# ---------------------------------------------------------------------------
LOADED_MPMS=$(cd /etc/apache2/mods-enabled 2>/dev/null && ls mpm_*.load 2>/dev/null | tr '\n' ' ')
echo "  MPM loaded: ${LOADED_MPMS:-none}"

rm -f /etc/apache2/mods-enabled/mpm_*.load /etc/apache2/mods-enabled/mpm_*.conf
ln -sf ../mods-available/mpm_prefork.load /etc/apache2/mods-enabled/mpm_prefork.load
ln -sf ../mods-available/mpm_prefork.conf /etc/apache2/mods-enabled/mpm_prefork.conf

case "$LOADED_MPMS" in
    "mpm_prefork.load ") : ;;  # already correct, nothing was changed
    *) echo "    -> corrected to mpm_prefork only" ;;
esac

# ---------------------------------------------------------------------------
# 4. Validate before starting
#
# Without this, a bad directive makes Apache exit immediately and the platform
# reports only "crashed". apache2ctl -t names the file and line.
# ---------------------------------------------------------------------------
if ! apache2ctl -t 2>&1; then
    echo "!! Apache config test FAILED — not starting. Config above names the file."
    exit 1
fi

echo "  web root: $(ls -1 /var/www/html/*.html 2>/dev/null | wc -l) html pages"
echo "=== starting Apache on port ${PORT} ==="
exec apache2-foreground
