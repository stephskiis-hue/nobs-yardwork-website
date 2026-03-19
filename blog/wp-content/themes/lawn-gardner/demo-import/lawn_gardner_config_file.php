<?php
/**
 * Settings for Demo Import
 *
 * @package Whizzie
 * @since 1.0.0
 */

if ( ! defined( 'WHIZZIE_DIR' ) ) {
	define( 'WHIZZIE_DIR', dirname( __FILE__ ) );
}

require trailingslashit( WHIZZIE_DIR ) . 'importer.php';

$current_theme = wp_get_theme();
$theme_title = $current_theme->get( 'Name' );

$lawn_gardner_config['page_slug'] 	= 'lawn-gardner';
$lawn_gardner_config['page_title']	= 'Get Started';

$lawn_gardner_config['steps'] = array(
	'widgets' => array(
		'id'			=> 'widgets',
		'title'			=> __( 'Demo Importer', 'lawn-gardner' ),
		'icon'			=> 'welcome-widgets-menus',
		'button_text_one'	=> __( 'Click On The Image To Import Customizer Demo', 'lawn-gardner' ),
		'button_text_two'	=> __( 'Click On The Image To Import Gutenberg Block Demo', 'lawn-gardner' ),
		'can_skip'		=> true,
	),
	'done' => array(
		'id'			=> 'done',
		'title'			=> __( 'All Done', 'lawn-gardner' ),
		'icon'			=> 'yes',
	)
);

if( class_exists( 'ThemeWhizzie' ) ) {
	$ThemeWhizzie = new ThemeWhizzie( $lawn_gardner_config );
}