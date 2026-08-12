# =============================================================================
# Repo-root container build — serves the JUNK REMOVAL site.
#
# WHY THIS IS HERE
# ----------------
# Railway builds from the repo root unless you set Settings -> Root Directory
# to `junk-removal`. With no Dockerfile at the root it auto-detects a static
# site and serves this repo's index.html — which is no-bs-yardwork.com, not the
# junk removal site. That is the wrong site on the staging URL.
#
# This file removes the trap: whether or not Root Directory is set, Railway
# serves the junk removal site.
#   - Root Directory unset  -> Railway uses THIS file
#   - Root Directory set to `junk-removal` -> Railway uses junk-removal/Dockerfile
# Both produce the same image.
#
# It changes nothing about the cPanel FTP deploy, which does not use Docker.
# =============================================================================

FROM php:8.2-apache

# Same modules as junk-removal/Dockerfile — see the comments there for what
# each one is for.
RUN a2enmod rewrite headers expires deflate substitute filter

COPY junk-removal/deploy/railway.conf /etc/apache2/conf-available/railway.conf
RUN a2enconf railway

# Only the junk removal folder becomes the web root. The yardwork site is not
# copied in at all.
COPY junk-removal/ /var/www/html/
RUN chown -R www-data:www-data /var/www/html

COPY junk-removal/deploy/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 8080
CMD ["/usr/local/bin/entrypoint.sh"]
