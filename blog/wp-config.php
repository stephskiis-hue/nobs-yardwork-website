<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the installation.
 * You don't have to use the web site, you can copy this file to "wp-config.php"
 * and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * Database settings
 * * Secret keys
 * * Database table prefix
 * * Localized language
 * * ABSPATH
 *
 * @link https://wordpress.org/support/article/editing-wp-config-php/
 *
 * @package WordPress
 */

// ** Database settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'so2wm0yi_wp_1oeau' );

/** Database username */
define( 'DB_USER', 'so2wm0yi_wp_zl0ie' );

/** Database password */
define( 'DB_PASSWORD', 'vf~jj@1OOAHd2V6E' );

/** Database hostname */
define( 'DB_HOST', 'localhost:3306' );

/** Database charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8' );

/** The database collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '' );

/**#@+
 * Authentication unique keys and salts.
 *
 * Change these to different unique phrases! You can generate these using
 * the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}.
 *
 * You can change these at any point in time to invalidate all existing cookies.
 * This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define('AUTH_KEY', '3%4EI6;Ns:03C*QG0Ir_@sI:1#7sU30@H4[WR4lNdcK#&VEW*C1&g#(i1/rV2ZGL');
define('SECURE_AUTH_KEY', 'D(6;51fuA2nY8jP5k1g/R|[)c60/k[-Rj3P*QL8L6[rLe_l;5F;%_L%l9zSgE#;_');
define('LOGGED_IN_KEY', '98u!(#iqchhv!%ZEPSbXu9SYu+A1b1&Ns~2(|IrvzV0[6+@(g9Ouu*dZ2_Rq)e+w');
define('NONCE_KEY', '!Xms1hDIA/hcjl:~Ag9xmUhU--%6%;4d4[%7ZKE[T#+[z1704Q-:D22mo)X_Cf29');
define('AUTH_SALT', 'jKb8j()8@7z4dl;VLY:WRs4EabtO!@*INq2T]%;/oC2rE;!~65h2n0vpPRw00423');
define('SECURE_AUTH_SALT', 'W38]23Py4%JP#I6oi8xEz;@;!9LXyamtV0iB9D9;k&__/%iE]b*4/_@(rI2_C10h');
define('LOGGED_IN_SALT', '5t:KuL45#9v26l2*4gG8b@eI8@3zy9b&9eB#Po1~kvYXp]&|o:7;u+xe5PQcR!Ri');
define('NONCE_SALT', '4K|i/s16U6cG6+@%5K[|v]yTzs~+T/7n1qR~9SpIT!YfQ|7|m7Kc:3Cy31~gcp7%');


/**#@-*/

/**
 * WordPress database table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix = '9CiYGZsZ_';


/* Add any custom values between this line and the "stop editing" line. */

define('WP_ALLOW_MULTISITE', true);
/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the documentation.
 *
 * @link https://wordpress.org/support/article/debugging-in-wordpress/
 */
if ( ! defined( 'WP_DEBUG' ) ) {
	define( 'WP_DEBUG', false );
}

/* That's all, stop editing! Happy publishing. */

/** Absolute path to the WordPress directory. */
if ( ! defined( 'ABSPATH' ) ) {
	define( 'ABSPATH', __DIR__ . '/' );
}

/** Sets up WordPress vars and included files. */
require_once ABSPATH . 'wp-settings.php';
