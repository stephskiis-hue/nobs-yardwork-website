<?php
/**
 * Custom typography options for this theme
 *
 * @package Art Blog
 */

function lawn_gardner_output_custom_font_css() {
    $lawn_gardner_font_choice = get_theme_mod( 'lawn_gardner_font_family', 'default' );

    if ( $lawn_gardner_font_choice === 'default' ) {
        return;
    }

    $lawn_gardner_font_map = array(
        'bad_script'       => '"Bad Script", cursive',
        'roboto'           => '"Roboto", sans-serif',
        'playfair_display' => '"Playfair Display", serif',
        'open_sans'        => '"Open Sans", sans-serif',
        'lobster'          => '"Lobster", cursive',
        'merriweather'     => '"Merriweather", serif',
        'oswald'           => '"Oswald", sans-serif',
        'raleway'          => '"Raleway", sans-serif',
    );

    $lawn_gardner_font_family = isset( $lawn_gardner_font_map[ $lawn_gardner_font_choice ] ) ? $lawn_gardner_font_map[ $lawn_gardner_font_choice ] : $lawn_gardner_font_map['pt_sans'];

    $lawn_gardner_custom_css = "
        body,
        h1, h2, h3, h4, h5, h6,
        p, a, span, div,
        .site, .entry-content, .main-navigation, .widget,
        input, textarea, button, .menu, .site-title, .site-description {
            font-family: {$lawn_gardner_font_family} !important;
        }
    ";

    wp_add_inline_style( 'lawn-gardner-google-fonts', $lawn_gardner_custom_css );
}
add_action( 'wp_enqueue_scripts', 'lawn_gardner_output_custom_font_css', 20 );


function lawn_gardner_sanitize_font_family( $lawn_gardner_input ) {
    $lawn_gardner_valid = array(
        'default', 'bad_script', 'roboto',
        'playfair_display', 'open_sans', 'lobster', 'merriweather', 'oswald', 'raleway'
    );
    return in_array( $lawn_gardner_input, $lawn_gardner_valid ) ? $lawn_gardner_input : 'default';
}

function lawn_gardner_enqueue_selected_google_font() {
    $lawn_gardner_font_choice = get_theme_mod( 'lawn_gardner_font_family', 'default' );

    $lawn_gardner_font_links = array(
        'bad_script'       => 'https://fonts.googleapis.com/css2?family=Bad+Script&display=swap',
        'roboto'           => 'https://fonts.googleapis.com/css2?family=Roboto&display=swap',
        'playfair_display' => 'https://fonts.googleapis.com/css2?family=Playfair+Display&display=swap',
        'open_sans'        => 'https://fonts.googleapis.com/css2?family=Open+Sans&display=swap',
        'lobster'          => 'https://fonts.googleapis.com/css2?family=Lobster&display=swap',
        'merriweather'     => 'https://fonts.googleapis.com/css2?family=Merriweather&display=swap',
        'oswald'           => 'https://fonts.googleapis.com/css2?family=Oswald&display=swap',
        'raleway'          => 'https://fonts.googleapis.com/css2?family=Raleway&display=swap',
    );

    if ( isset( $lawn_gardner_font_links[ $lawn_gardner_font_choice ] ) ) {
        wp_enqueue_style( 'lawn-gardner-dynamic-font', $lawn_gardner_font_links[ $lawn_gardner_font_choice ], array(), null );
    }
}
add_action( 'wp_enqueue_scripts', 'lawn_gardner_enqueue_selected_google_font' );