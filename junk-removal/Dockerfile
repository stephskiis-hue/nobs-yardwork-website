# =============================================================================
# Railway / container deployment for the No BS Junk Removal site.
#
# Uses php:apache rather than a plain static server on purpose: the production
# host is cPanel + Apache + PHP, so this image runs the SAME .htaccess and the
# SAME form-process.php. What you see on Railway is what you get on the real
# server — extensionless URLs, the 404 page, gzip, caching headers and the
# quote form all behave identically.
#
# This file only affects container deploys. The cPanel FTP deploy ignores it.
# =============================================================================

FROM php:8.2-apache

# mod_rewrite    -> extensionless URLs (.htaccess RewriteRules)
# mod_headers    -> Cache-Control and the noindex header
# mod_expires    -> the ExpiresByType rules in .htaccess
# mod_deflate    -> gzip
# mod_substitute -> rewrites the production domain in canonical/OG tags to the
#                   actual staging host, and injects the preview banner, so the
#                   committed HTML stays production-correct
# mod_filter     -> required by AddOutputFilterByType for SUBSTITUTE
RUN a2enmod rewrite headers expires deflate substitute filter

# .htaccess is ignored unless AllowOverride is on; Debian's default is None.
COPY deploy/railway.conf /etc/apache2/conf-available/railway.conf
RUN a2enconf railway

COPY . /var/www/html/
RUN chown -R www-data:www-data /var/www/html

# Railway assigns a port at runtime via $PORT and it is not always 80, so the
# listen port has to be patched at start rather than baked in. Falls back to
# 8080 for local `docker run` with no PORT set.
COPY deploy/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 8080
CMD ["/usr/local/bin/entrypoint.sh"]
