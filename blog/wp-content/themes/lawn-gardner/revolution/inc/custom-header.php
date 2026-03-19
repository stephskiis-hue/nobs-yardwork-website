<?php
/**
 * Sample implementation of the Custom Header feature
 *
 * @package Lawn Gardner
 */

function lawn_gardner_custom_header_setup() {
	add_theme_support(
		'custom-header',
		apply_filters(
			'lawn_gardner_custom_header_args',
			array(
				'default-image'      => '',
				'default-text-color' => '000000',
				'width'              => 1000,
				'height'             => 250,
				'flex-height'        => true,
				'wp-head-callback'   => 'lawn_gardner_header_style',
			)
		)
	);
}
add_action( 'after_setup_theme', 'lawn_gardner_custom_header_setup' );

if ( ! function_exists( 'lawn_gardner_header_style' ) ) :	
	function lawn_gardner_header_style() {
		$lawn_gardner_header_text_color = get_header_textcolor();
		if ( get_theme_support( 'custom-header', 'default-text-color' ) === $lawn_gardner_header_text_color ) {
			return;
		}
		?>
		<style type="text/css">
		<?php
		// Has the text been hidden?
		if ( ! display_header_text() ) :
			?>
			.site-title,
			.site-description {
				position: absolute;
				clip: rect(1px, 1px, 1px, 1px);
				}
			<?php
			// If the user has set a custom color for the text use that.
		else :
			?>
			.site-title a,
			.site-description {
				color: #<?php echo esc_attr( $lawn_gardner_header_text_color ); ?>;
			}
		<?php endif; ?>
		</style>
		<?php
	}
endif;