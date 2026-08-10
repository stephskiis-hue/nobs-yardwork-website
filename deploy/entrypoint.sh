#!/bin/sh
# Bind Apache to the port the platform assigns.
#
# Railway (and most PaaS) pass the port in $PORT and it is not always 80. Both
# ports.conf and the default vhost have to agree or Apache starts but nothing
# reaches it.
set -e

PORT="${PORT:-8080}"

sed -i "s/^Listen .*/Listen ${PORT}/" /etc/apache2/ports.conf
sed -i "s/<VirtualHost \*:[0-9]*>/<VirtualHost *:${PORT}>/" \
    /etc/apache2/sites-available/000-default.conf

echo "Serving No BS Junk Removal on port ${PORT}"
exec apache2-foreground
