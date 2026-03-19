<?php
/**
 * Lawn Gardner functions and definitions
 *
 * @package Lawn Gardner
 */

if ( ! defined( 'LAWN_GARDNER_VERSION' ) ) {
	// Replace the version number of the theme on each release.
	define( 'LAWN_GARDNER_VERSION', '1.0.0' );
}

function lawn_gardner_setup() {

	load_theme_textdomain( 'lawn-gardner', get_template_directory() . '/languages' );
	add_theme_support( 'automatic-feed-links' );
	add_theme_support( 'title-tag' );
	add_theme_support( 'post-thumbnails' );
	add_theme_support( 'woocommerce' );
	add_theme_support( "align-wide" );
	add_theme_support( "responsive-embeds" );

	register_nav_menus(
		array(
			'menu-1' => esc_html__( 'Primary', 'lawn-gardner' ),
			'social-menu' => esc_html__('Social Menu', 'lawn-gardner'),
		)
	);

	add_theme_support(
		'html5',
		array(
			'search-form',
			'comment-form',
			'comment-list',
			'gallery',
			'caption',
			'style',
			'script',
		)
	);

	add_theme_support(
		'custom-background',
		apply_filters(
			'lawn_gardner_custom_background_args',
			array(
				'default-color' => '#fafafa',
				'default-image' => '',
			)
		)
	);

	add_theme_support( 'customize-selective-refresh-widgets' );

	add_theme_support(
		'custom-logo',
		array(
			'height'      => 250,
			'width'       => 250,
			'flex-width'  => true,
			'flex-height' => true,
		)
	);
	
	add_theme_support( 'post-formats', array(
        'image',
        'video',
        'gallery',
        'audio', 
    ));

}
add_action( 'after_setup_theme', 'lawn_gardner_setup' );

/**
 * Set the content width in pixels, based on the theme's design and stylesheet.
 *
 * Priority 0 to make it available to lower priority callbacks.
 *
 * @global int $content_width
 */
function lawn_gardner_content_width() {
	$GLOBALS['content_width'] = apply_filters( 'lawn_gardner_content_width', 640 );
}
add_action( 'after_setup_theme', 'lawn_gardner_content_width', 0 );

/**
 * Register widget area.
 *
 * @link https://developer.wordpress.org/themes/functionality/sidebars/#registering-a-sidebar
 */
function lawn_gardner_widgets_init() {
	register_sidebar(
		array(
			'name'          => esc_html__( 'Sidebar', 'lawn-gardner' ),
			'id'            => 'sidebar-1',
			'description'   => esc_html__( 'Add widgets here.', 'lawn-gardner' ),
			'before_widget' => '<section id="%1$s" class="widget %2$s">',
			'after_widget'  => '</section>',
			'before_title'  => '<h2 class="widget-title">',
			'after_title'   => '</h2>',
		)
	);

	register_sidebar(
		array(
			'name'          => esc_html__( 'Footer 1', 'lawn-gardner' ),
			'id'            => 'footer-1',
			'description'   => esc_html__( 'Add widgets here.', 'lawn-gardner' ),
			'before_widget' => '<section id="%1$s" class="widget %2$s">',
			'after_widget'  => '</section>',
			'before_title'  => '<h2 class="widget-title">',
			'after_title'   => '</h2>',
		)
	);

	register_sidebar(
		array(
			'name'          => esc_html__( 'Footer 2', 'lawn-gardner' ),
			'id'            => 'footer-2',
			'description'   => esc_html__( 'Add widgets here.', 'lawn-gardner' ),
			'before_widget' => '<section id="%1$s" class="widget %2$s">',
			'after_widget'  => '</section>',
			'before_title'  => '<h2 class="widget-title">',
			'after_title'   => '</h2>',
		)
	);

	register_sidebar(
		array(
			'name'          => esc_html__( 'Footer 3', 'lawn-gardner' ),
			'id'            => 'footer-3',
			'description'   => esc_html__( 'Add widgets here.', 'lawn-gardner' ),
			'before_widget' => '<section id="%1$s" class="widget %2$s">',
			'after_widget'  => '</section>',
			'before_title'  => '<h2 class="widget-title">',
			'after_title'   => '</h2>',
		)
	);
}
add_action( 'widgets_init', 'lawn_gardner_widgets_init' );


function lawn_gardner_social_menu()
    {
        if (has_nav_menu('social-menu')) :
            wp_nav_menu(array(
                'theme_location' => 'social-menu',
                'container' => 'ul',
                'menu_class' => 'social-menu menu',
                'menu_id'  => 'menu-social',
            ));
        endif;
    }

/**
 * Enqueue scripts and styles.
 */
function lawn_gardner_scripts() {

	// Load fonts locally
	require_once get_theme_file_path('revolution/inc/wptt-webfont-loader.php');

	$lawn_gardner_font_families = array(
		'Poppins:wght@100;400;500;600;700',
		'Lora:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600;1,700'
	);
	
	$lawn_gardner_fonts_url = add_query_arg( array(
		'family' => implode( '&family=', $lawn_gardner_font_families ),
		'display' => 'swap',
	), 'https://fonts.googleapis.com/css2' );

	wp_enqueue_style('lawn-gardner-google-fonts', wptt_get_webfont_url(esc_url_raw($lawn_gardner_fonts_url)), array(), '1.0.0');
	
	// Font Awesome CSS
	wp_enqueue_style('font-awesome-6', get_template_directory_uri() . '/revolution/assets/vendors/font-awesome-6/css/all.min.css', array(), '6.7.2');

	wp_enqueue_style('owl.carousel.style', get_template_directory_uri() . '/revolution/assets/css/owl.carousel.css', array());
	
	wp_enqueue_style( 'lawn-gardner-style', get_stylesheet_uri(), array(), LAWN_GARDNER_VERSION );

	require get_parent_theme_file_path( '/custom-style.php' );
	wp_add_inline_style( 'lawn-gardner-style',$lawn_gardner_custom_css );

	wp_style_add_data('lawn-gardner-style', 'rtl', 'replace');

	wp_enqueue_script( 'lawn-gardner-navigation', get_template_directory_uri() . '/js/navigation.js', array(), LAWN_GARDNER_VERSION, true );

	wp_enqueue_script( 'owl.carousel.jquery', get_template_directory_uri() . '/revolution/assets/js/owl.carousel.js', array(), LAWN_GARDNER_VERSION, true );

	wp_enqueue_script( 'lawn-gardner-custom-js', get_template_directory_uri() . '/revolution/assets/js/custom.js', array('jquery'), LAWN_GARDNER_VERSION, true );

	if ( is_singular() && comments_open() && get_option( 'thread_comments' ) ) {
		wp_enqueue_script( 'comment-reply' );
	}
}
add_action( 'wp_enqueue_scripts', 'lawn_gardner_scripts' );

if (!function_exists('lawn_gardner_related_post')) :
    /**
     * Display related posts from same category
     *
     */

    function lawn_gardner_related_post($post_id){        
        $categories = get_the_category($post_id);
        if ($categories) {
            $category_ids = array();
            $category = get_category($category_ids);
            $categories = get_the_category($post_id);
            foreach ($categories as $category) {
                $category_ids[] = $category->term_id;
            }
            $count = $category->category_count;
            if ($count > 1) { ?>

         	<?php
		$lawn_gardner_related_post_wrap = absint(get_theme_mod('lawn_gardner_enable_related_post', 1));
		if($lawn_gardner_related_post_wrap == 1){ ?>
                <div class="related-post">
                    
                    <h2 class="post-title"><?php esc_html_e(get_theme_mod('lawn_gardner_related_post_text', __('Related Post', 'lawn-gardner'))); ?></h2>
                    <?php
                    $lawn_gardner_cat_post_args = array(
                        'category__in' => $category_ids,
                        'post__not_in' => array($post_id),
                        'post_type' => 'post',
                        'posts_per_page' =>  get_theme_mod( 'lawn_gardner_related_post_count', '3' ),
                        'post_status' => 'publish',
						'orderby'           => 'rand',
                        'ignore_sticky_posts' => true
                    );
                    $lawn_gardner_featured_query = new WP_Query($lawn_gardner_cat_post_args);
                    ?>
                    <div class="rel-post-wrap">
                        <?php
                        if ($lawn_gardner_featured_query->have_posts()) :

                        while ($lawn_gardner_featured_query->have_posts()) : $lawn_gardner_featured_query->the_post();
                            ?>

							<div class="card-item rel-card-item">
								<div class="card-content">
									<?php if ( has_post_thumbnail() ) { ?>
										<div class="card-media">
											<?php lawn_gardner_post_thumbnail(); ?>
										</div>
									<?php } else {
										// Fallback default image
										$lawn_gardner_default_post_thumbnail = get_template_directory_uri() . '/revolution/assets/images/project1.png';
										echo '<img class="default-post-img" src="' . esc_url( $lawn_gardner_default_post_thumbnail ) . '" alt="' . esc_attr( get_the_title() ) . '">';
									} ?>
									<div class="entry-title">
										<h3>
											<a href="<?php the_permalink() ?>">
												<?php the_title(); ?>
											</a>
										</h3>
									</div>
									<div class="entry-meta">
										<?php
										lawn_gardner_posted_on();
										lawn_gardner_posted_by();
										?>
									</div>
								</div>
							</div>
                        <?php
                        endwhile;
                        ?>
                <?php
                endif;
                wp_reset_postdata();
                ?>
                </div>
                <?php } ?>
                <?php
            }
        }
    }
endif;
add_action('lawn_gardner_related_posts', 'lawn_gardner_related_post', 10, 1);

function lawn_gardner_sanitize_choices( $input, $setting ) {
    global $wp_customize; 
    $control = $wp_customize->get_control( $setting->id ); 
    if ( array_key_exists( $input, $control->choices ) ) {
        return $input;
    } else {
        return $setting->default;
    }
}

//Excerpt 
function lawn_gardner_excerpt_function($excerpt_count = 35) {
    $excerpt = get_the_excerpt();
    $text_excerpt = wp_strip_all_tags($excerpt);
    $excerpt_limit = (int) get_theme_mod('lawn_gardner_excerpt_limit', $excerpt_count);
    $words = preg_split('/\s+/', $text_excerpt); 
    $trimmed_words = array_slice($words, 0, $excerpt_limit);
    $theme_excerpt = implode(' ', $trimmed_words);

    return $theme_excerpt;
}

// Add admin notice
function lawn_gardner_admin_notice() { 
    global $pagenow;
    $theme_args      = wp_get_theme();
    $meta            = get_option( 'lawn_gardner_admin_notice' );
    $name            = $theme_args->__get( 'Name' );
    $current_screen  = get_current_screen();

    if( !$meta ){
	    if( is_network_admin() ){
	        return;
	    }

	    if( ! current_user_can( 'manage_options' ) ){
	        return;
	    } 
		
		if( $lawn_gardner_current_screen->base !== 'appearance_page_lawn_gardner_guide' && 
            $lawn_gardner_current_screen->base !== 'toplevel_page_lawngardner-demoimport' ) { ?>

            <div class="notice notice-success lawn-gardner-welcome-notice">
                <p class="lawn-gardner-dismiss-link">
                    <strong>
                        <a href="<?php echo esc_url( add_query_arg( 'lawn_gardner_admin_notice', '1' ) ); ?>">
                            <?php esc_html_e( 'Dismiss', 'lawn-gardner' ); ?>
                        </a>
                    </strong>
                </p>

                <div class="lawn-gardner-welcome-notice-wrap">
                    <h2 class="lawn-gardner-notice-title">
                        <span class="dashicons dashicons-admin-home"></span> 
                        <?php 
                            $lawn_gardner_theme_name = wp_get_theme()->get( 'Name' );
                            /* translators: %s!: Theme Name. */
                            echo esc_html( sprintf( __( 'Welcome to the free theme: %s!', 'lawn-gardner' ), $lawn_gardner_theme_name ) );
                        ?>
                    </h2>
                    <p class="lawn-gardner-notice-desc">
                        <?php esc_html_e( 'Get started by exploring the features of your new theme. Customize your design, add your content, and create a site that fits your vision.', 'lawn-gardner' ); ?>
                    </p>

                    <div class="lawn-gardner-welcome-info">
                        <div class="lawn-gardner-welcome-thumb">
                            <img src="<?php echo esc_url( get_stylesheet_directory_uri() . '/screenshot.png' ); ?>" alt="<?php esc_attr_e( 'Theme Screenshot', 'lawn-gardner' ); ?>">
                        </div>

                        <div class="lawn-gardner-welcome-import">
                            <h3><span class="dashicons dashicons-download"></span> <?php esc_html_e( 'Quick Start: Import Demo', 'lawn-gardner' ); ?></h3>
                            <p><?php esc_html_e( 'Use the Demo Importer to quickly set up your site with a pre-made layout. Get a complete site in minutes.', 'lawn-gardner' ); ?></p>
                            <p><a class="button info-link button-primary" href="<?php echo esc_url( admin_url( 'themes.php?page=lawngardner-demoimport' ) ); ?>"><?php esc_html_e( 'Go to Demo Importer', 'lawn-gardner' ); ?></a></p>
                        </div>

                        <div class="lawn-gardner-welcome-getting-started">
                            <h3><span class="dashicons dashicons-art"></span> <?php esc_html_e( 'Customize Your Theme', 'lawn-gardner' ); ?></h3>
                            <p><?php esc_html_e( 'Want to make it truly yours? Explore the Getting Started Guide to personalize your site to suit your needs.', 'lawn-gardner' ); ?></p>
                            <p><a class="info-link button" href="<?php echo esc_url( admin_url( 'themes.php?page=lawn-gardner-getstart-page' ) ); ?>"><?php esc_html_e( 'View Getting Started Guide', 'lawn-gardner' ); ?></a></p>
                        </div>
                    </div>
                </div>
            </div>

            <?php
        }

	}
}

add_action( 'admin_notices', 'lawn_gardner_admin_notice' );

if( ! function_exists( 'lawn_gardner_update_admin_notice' ) ) :
/**
 * Updating admin notice on dismiss
*/
function lawn_gardner_update_admin_notice(){
    if ( isset( $_GET['lawn_gardner_admin_notice'] ) && $_GET['lawn_gardner_admin_notice'] = '1' ) {
        update_option( 'lawn_gardner_admin_notice', true );
    }
}
endif;
add_action( 'admin_init', 'lawn_gardner_update_admin_notice' );


add_action('after_switch_theme', 'lawn_gardner_setup_options');
function lawn_gardner_setup_options () {
    update_option('lawn_gardner_admin_notice', FALSE );
}


/**
 * Checkbox sanitization callback example.
 *
 * Sanitization callback for 'checkbox' type controls. This callback sanitizes `$checked`
 * as a boolean value, either TRUE or FALSE.
 */
function lawn_gardner_sanitize_checkbox($checked)
{
    // Boolean check.
    return ((isset($checked) && true == $checked) ? true : false);
}

/**
 * Implement the Custom Header feature.
 */
require get_template_directory() . '/revolution/inc/custom-header.php';

/**
 * Custom template tags for this theme.
 */
require get_template_directory() . '/revolution/inc/template-tags.php';

/**
 * Functions which enhance the theme by hooking into WordPress.
 */
require get_template_directory() . '/revolution/inc/template-functions.php';

/**
 * Customizer additions.
 */
require get_template_directory() . '/revolution/inc/customizer.php';

/**
 * Breadcrumb File.
 */
require get_template_directory() . '/revolution/inc/breadcrumbs.php';

/**
 * Custom typography options for this theme.
 */
require get_template_directory() . '/revolution/inc/typography-options.php';


//////////////////////////////////////////////   Function for Translation Error   //////////////////////////////////////////////////////
function lawn_gardner_enqueue_function() {

	/**
	* GET START.
	*/
	require get_template_directory() . '/getstarted/lawn_gardner_about_page.php';

	/**
	* DEMO IMPORT.
	*/
	require get_template_directory() . '/demo-import/lawn_gardner_config_file.php';

	define('LAWN_GARDNER_FREE_SUPPORT',__('https://wordpress.org/support/theme/lawn-gardner/','lawn-gardner'));
	define('LAWN_GARDNER_PRO_SUPPORT',__('https://www.revolutionwp.com/pages/community/','lawn-gardner'));
	define('LAWN_GARDNER_PRO_THEME',__('https://www.revolutionwp.com/products/lawn-care-wordpress-theme','lawn-gardner'));
	define('LAWN_GARDNER_REVIEW',__('https://wordpress.org/support/theme/lawn-gardner/reviews/#new-post','lawn-gardner'));
	define('LAWN_GARDNER_BUY_NOW',__('https://www.revolutionwp.com/products/lawn-care-wordpress-theme','lawn-gardner'));
	define('LAWN_GARDNER_LIVE_DEMO',__('https://demo.revolutionwp.com/lawn-care-pro/','lawn-gardner'));
	define('LAWN_GARDNER_LITE_DOC',__('https://demo.revolutionwp.com/wpdocs/lawn-gardner-free/','lawn-gardner'));
	
}
add_action( 'after_setup_theme', 'lawn_gardner_enqueue_function' );

/**
 * Load Jetpack compatibility file.
 */
if ( defined( 'JETPACK__VERSION' ) ) {
	require get_template_directory() . '/revolution/inc/jetpack.php';
}


function lawn_gardner_remove_customize_register() {
    global $wp_customize;

    $wp_customize->remove_setting( 'display_header_text' );
    $wp_customize->remove_control( 'display_header_text' );

}

add_action( 'customize_register', 'lawn_gardner_remove_customize_register', 11 );

/**
 * WooCommerce custom filters
 */
add_filter('loop_shop_columns', 'lawn_gardner_loop_columns');

if (!function_exists('lawn_gardner_loop_columns')) {

	function lawn_gardner_loop_columns() {

		$lawn_gardner_columns = get_theme_mod( 'lawn_gardner_per_columns', 3 );

		return $lawn_gardner_columns;
	}
}

/************************************************************************************/

add_filter( 'loop_shop_per_page', 'lawn_gardner_per_page', 20 );

function lawn_gardner_per_page( $lawn_gardner_cols ) {

  	$lawn_gardner_cols = get_theme_mod( 'lawn_gardner_product_per_page', 9 );

	return $lawn_gardner_cols;
}

/************************************************************************************/

add_filter( 'woocommerce_output_related_products_args', 'lawn_gardner_products_args' );

function lawn_gardner_products_args( $args ) {

    $args['posts_per_page'] = get_theme_mod( 'custom_related_products_number', 6 );

    $args['columns'] = get_theme_mod( 'custom_related_products_number_per_row', 3 );

    return $args;
}

/************************************************************************************/

/**
 * Custom logo
 */

function lawn_gardner_custom_css() {
?>
	<style type="text/css" id="custom-theme-colors" >
        :root {
           
            --lawn_gardner_logo_width: <?php echo absint(get_theme_mod('lawn_gardner_logo_width')); ?> ;   
        }
        .main-header .site-branding {
            max-width:<?php echo esc_html(get_theme_mod('lawn_gardner_logo_width')); ?>px ;    
        }         
	</style>
<?php
}
add_action( 'wp_head', 'lawn_gardner_custom_css' );

function get_changelog_from_readme() {
    $file_path = get_template_directory() . '/readme.txt'; // Adjust path if necessary

    if (file_exists($file_path)) {
        $content = file_get_contents($file_path);

        // Extract changelog section
        $changelog_start = strpos($content, "== Changelog ==");
        $changelog = substr($content, $changelog_start);

        // Split changelog into versions
        preg_match_all('/\*\s([\d\.]+)\s-\s(.+?)\n((?:\t-\s.+?\n)+)/', $changelog, $matches, PREG_SET_ORDER);
        
        return $matches;
    }
    return [];
}
