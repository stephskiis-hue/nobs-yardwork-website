#!/bin/sh
# Container start-up for the staging deploy.
#
# Two jobs:
#   1. Bind Apache to whatever port the platform assigns.
#   2. Rewrite the production domain to the actual staging host, so shared
#      links get a working preview card instead of a broken one.
set -e

# ---------------------------------------------------------------------------
# 1. Port
#
# Railway (and most PaaS) pass the port in $PORT and it is not always 80. Both
# ports.conf and the default vhost have to agree or Apache starts happily and
# nothing ever reaches it.
# ---------------------------------------------------------------------------
PORT="${PORT:-8080}"
sed -i "s/^Listen .*/Listen ${PORT}/" /etc/apache2/ports.conf
sed -i "s/<VirtualHost \*:[0-9]*>/<VirtualHost *:${PORT}>/" \
    /etc/apache2/sites-available/000-default.conf

# ---------------------------------------------------------------------------
# 2. Canonical / Open Graph host
#
# Every page hard-codes https://www.no-bs-junkremoval.com in its canonical,
# og:url and og:image. That is correct for production, but on staging the
# domain does not resolve — so pasting the staging link into Slack, Messenger
# or a text message produces a preview card with no image and a dead
# click-through. Rewriting the host at serve time fixes sharing without
# putting staging URLs into the committed HTML.
#
# RAILWAY_PUBLIC_DOMAIN is provided by Railway automatically once a domain is
# generated. PUBLIC_URL is the manual override for any other host.
# ---------------------------------------------------------------------------
DOMAIN="${PUBLIC_URL:-${RAILWAY_PUBLIC_DOMAIN:-}}"

if [ -n "$DOMAIN" ]; then
    case "$DOMAIN" in
        http://*|https://*) BASE="$DOMAIN" ;;
        *)                  BASE="https://$DOMAIN" ;;
    esac
    BASE="${BASE%/}"
    # Same FilesMatch scoping as railway.conf, and for the same reason: the
    # 404 ErrorDocument does not pick up AddOutputFilterByType. Apache merges
    # the Substitute directives from both files, so the banner and this
    # rewrite both apply.
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
    echo "Rewriting canonical/OG host to ${BASE}"
else
    echo "No PUBLIC_URL or RAILWAY_PUBLIC_DOMAIN set — canonical and og: tags"
    echo "will still point at no-bs-junkremoval.com, so shared-link previews"
    echo "will not load. Fine for local runs."
fi

echo "Serving No BS Junk Removal on port ${PORT}"
exec apache2-foreground
