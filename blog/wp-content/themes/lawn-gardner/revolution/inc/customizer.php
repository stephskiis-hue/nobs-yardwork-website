<?php
/**
 * Lawn Gardner Theme Customizer
 *
 * @package Lawn Gardner
 */

function lawn_gardner_customize_register( $wp_customize ) {

	load_template( trailingslashit( get_template_directory() ) . 'revolution/inc/fontawesome-change.php' );
	
	$wp_customize->get_setting( 'blogname' )->transport         = 'postMessage';
	$wp_customize->get_setting( 'blogdescription' )->transport  = 'postMessage';
	$wp_customize->get_setting( 'header_textcolor' )->transport = 'postMessage';

	if ( isset( $wp_customize->selective_refresh ) ) {
		$wp_customize->selective_refresh->add_partial(
			'blogname',
			array(
				'selector'        => '.site-title a',
				'render_callback' => 'lawn_gardner_customize_partial_blogname',
			)
		);
		$wp_customize->selective_refresh->add_partial(
			'blogdescription',
			array(
				'selector'        => '.site-description',
				'render_callback' => 'lawn_gardner_customize_partial_blogdescription',
			)
		);
	}

	/*
    * Theme Options Panel
    */
	$wp_customize->add_panel('lawn_gardner_panel', array(
		'priority' => 25,
		'capability' => 'edit_theme_options',
		'title' => __('Lawn Gardner Theme Options', 'lawn-gardner'),
	));

	/*
	* Customizer top header section
	*/

	$wp_customize->add_setting(
		'lawn_gardner_site_title_text',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => 1,
			'sanitize_callback' => 'lawn_gardner_sanitize_checkbox',
		)
	);

	$wp_customize->add_control(
		'lawn_gardner_site_title_text',
		array(
			'label'       => __('Enable Title', 'lawn-gardner'),
			'description' => __('Enable or Disable Title from the site', 'lawn-gardner'),
			'section'     => 'title_tagline',
			'type'        => 'checkbox',
		)
	);

	$wp_customize->add_setting(
		'lawn_gardner_site_tagline_text',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => 0,
			'sanitize_callback' => 'lawn_gardner_sanitize_checkbox',
		)
	);

	$wp_customize->add_control(
		'lawn_gardner_site_tagline_text',
		array(
			'label'       => __('Enable Tagline', 'lawn-gardner'),
			'description' => __('Enable or Disable Tagline from the site', 'lawn-gardner'),
			'section'     => 'title_tagline',
			'type'        => 'checkbox',
		)
	);

	$wp_customize->add_setting(
		'lawn_gardner_logo_width',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => '150',
			'sanitize_callback' => 'sanitize_text_field',
		)
	);

	$wp_customize->add_control(
		'lawn_gardner_logo_width',
		array(
			'label'       => __('Logo Width in PX', 'lawn-gardner'),
			'section'     => 'title_tagline',
			'type'        => 'number',
			'input_attrs' => array(
	            'min' => 100,
	             'max' => 300,
	             'step' => 1,
	         ),
		)
	);

	/* WooCommerce custom settings */

	$wp_customize->add_section('woocommerce_custom_settings', array(
		'priority'       => 5,
		'capability'     => 'edit_theme_options',
		'theme_supports' => '',
		'title'          => __('WooCommerce Custom Settings', 'lawn-gardner'),
		'panel'       => 'woocommerce',
	));

	$wp_customize->add_setting(
		'lawn_gardner_per_columns',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => '3',
			'sanitize_callback' => 'sanitize_text_field',
		)
	);

	$wp_customize->add_control(
		'lawn_gardner_per_columns',
		array(
			'label'       => __('Product Per Single Row', 'lawn-gardner'),
			'section'     => 'woocommerce_custom_settings',
			'type'        => 'number',
			'input_attrs' => array(
	            'min' => 1,
	             'max' => 4,
	             'step' => 1,
	         ),
		)
	);

	$wp_customize->add_setting(
		'lawn_gardner_product_per_page',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => '6',
			'sanitize_callback' => 'sanitize_text_field',
		)
	);

	$wp_customize->add_control(
		'lawn_gardner_product_per_page',
		array(
			'label'       => __('Product Per One Page', 'lawn-gardner'),
			'section'     => 'woocommerce_custom_settings',
			'type'        => 'number',
			'input_attrs' => array(
	            'min' => 1,
	             'max' => 12,
	             'step' => 1,
	         ),
		)
	);

	/*Related Products Enable Option*/
	$wp_customize->add_setting(
		'lawn_gardner_enable_related_product',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => 1,
			'sanitize_callback' => 'lawn_gardner_sanitize_checkbox',
		)
	);

	$wp_customize->add_control(
		'lawn_gardner_enable_related_product',
		array(
			'label'       => __('Enable Related Product', 'lawn-gardner'),
			'description' => __('Checked to show Related Product', 'lawn-gardner'),
			'section'     => 'woocommerce_custom_settings',
			'type'        => 'checkbox',
		)
	);

	$wp_customize->add_setting(
		'custom_related_products_number',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => '3',
			'sanitize_callback' => 'sanitize_text_field',
		)
	);

	$wp_customize->add_control(
		'custom_related_products_number',
		array(
			'label'       => __('Related Product Count', 'lawn-gardner'),
			'section'     => 'woocommerce_custom_settings',
			'type'        => 'number',
			'input_attrs' => array(
	            'min' => 1,
	             'max' => 20,
	             'step' => 1,
	         ),
		)
	);

	$wp_customize->add_setting(
		'custom_related_products_number_per_row',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => '3',
			'sanitize_callback' => 'sanitize_text_field',
		)
	);

	$wp_customize->add_control(
		'custom_related_products_number_per_row',
		array(
			'label'       => __('Related Product Per Row', 'lawn-gardner'),
			'section'     => 'woocommerce_custom_settings',
			'type'        => 'number',
			'input_attrs' => array(
	            'min' => 1,
	             'max' => 4,
	             'step' => 1,
	         ),
		)
	);

	/*Archive Product layout*/
	$wp_customize->add_setting('lawn_gardner_archive_product_layout',array(
        'default' => 'layout-1',
        'sanitize_callback' => 'lawn_gardner_sanitize_choices'
	));
	$wp_customize->add_control('lawn_gardner_archive_product_layout',array(
        'type' => 'select',
        'label' => esc_html__('Archive Product Layout','lawn-gardner'),
        'section' => 'woocommerce_custom_settings',
        'choices' => array(
            'layout-1' => esc_html__('Sidebar On Right','lawn-gardner'),
            'layout-2' => esc_html__('Sidebar On Left','lawn-gardner'),
			'layout-3' => esc_html__('Full Width Layout','lawn-gardner')
        ),
	) );

	/*Single Product layout*/
	$wp_customize->add_setting('lawn_gardner_single_product_layout',array(
        'default' => 'layout-1',
        'sanitize_callback' => 'lawn_gardner_sanitize_choices'
	));
	$wp_customize->add_control('lawn_gardner_single_product_layout',array(
        'type' => 'select',
        'label' => esc_html__('Single Product Layout','lawn-gardner'),
        'section' => 'woocommerce_custom_settings',
        'choices' => array(
            'layout-1' => esc_html__('Sidebar On Right','lawn-gardner'),
            'layout-2' => esc_html__('Sidebar On Left','lawn-gardner'),
			'layout-3' => esc_html__('Full Width Layout','lawn-gardner')
        ),
	) );

	$wp_customize->add_setting('lawn_gardner_woocommerce_product_sale',array(
		'capability'        => 'edit_theme_options',
		'transport'         => 'refresh',
        'default'           => 'Right',
        'sanitize_callback' => 'lawn_gardner_sanitize_choices'
    ));
    $wp_customize->add_control('lawn_gardner_woocommerce_product_sale',array(
        'label'       => esc_html__( 'Woocommerce Product Sale Positions','lawn-gardner' ),
        'type' => 'select',
        'section' => 'woocommerce_custom_settings',
        'choices' => array(
            'Right' => __('Right','lawn-gardner'),
            'Left' => __('Left','lawn-gardner'),
            'Center' => __('Center','lawn-gardner')
        ),
    ) );

	/*Additional Options*/
	$wp_customize->add_section('lawn_gardner_additional_section', array(
		'priority'       => 5,
		'capability'     => 'edit_theme_options',
		'theme_supports' => '',
		'title'          => __('Additional Options', 'lawn-gardner'),
		'panel'       => 'lawn_gardner_panel',
	));

	/*Main Slider Enable Option*/
	$wp_customize->add_setting(
		'lawn_gardner_enable_sticky_header',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => false,
			'sanitize_callback' => 'lawn_gardner_sanitize_checkbox',
		)
	);

	$wp_customize->add_control(
		'lawn_gardner_enable_sticky_header',
		array(
			'label'       => __('Enable Sticky Header', 'lawn-gardner'),
			'description' => __('Checked to enable sticky header', 'lawn-gardner'),
			'section'     => 'lawn_gardner_additional_section',
			'type'        => 'checkbox',
		)
	);

	/*Main Slider Enable Option*/
	$wp_customize->add_setting(
		'lawn_gardner_enable_preloader',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => 0,
			'sanitize_callback' => 'lawn_gardner_sanitize_checkbox',
		)
	);

	$wp_customize->add_control(
		'lawn_gardner_enable_preloader',
		array(
			'label'       => __('Enable Preloader', 'lawn-gardner'),
			'description' => __('Checked to show preloader', 'lawn-gardner'),
			'section'     => 'lawn_gardner_additional_section',
			'type'        => 'checkbox',
		)
	);

	/*Breadcrumbs Enable Option*/
	$wp_customize->add_setting(
		'lawn_gardner_enable_breadcrumbs',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => 1,
			'sanitize_callback' => 'lawn_gardner_sanitize_checkbox',
		)
	);

	$wp_customize->add_control(
		'lawn_gardner_enable_breadcrumbs',
		array(
			'label'       => __('Enable Breadcrumbs', 'lawn-gardner'),
			'description' => __('Checked to show Breadcrumbs', 'lawn-gardner'),
			'section'     => 'lawn_gardner_additional_section',
			'type'        => 'checkbox',
		)
	);

	/*Post layout*/
	$wp_customize->add_setting('lawn_gardner_archive_layout',array(
        'default' => 'layout-1',
        'sanitize_callback' => 'lawn_gardner_sanitize_choices'
	));
	$wp_customize->add_control('lawn_gardner_archive_layout',array(
        'type' => 'select',
        'label' => esc_html__('Posts Layout','lawn-gardner'),
        'section' => 'lawn_gardner_additional_section',
        'choices' => array(
            'layout-1' => esc_html__('Sidebar On Right','lawn-gardner'),
            'layout-2' => esc_html__('Sidebar On Left','lawn-gardner'),
			'layout-3' => esc_html__('Full Width Layout','lawn-gardner')
        ),
	) );

	/*single post layout*/
	$wp_customize->add_setting('lawn_gardner_post_layout',array(
        'default' => 'layout-1',
        'sanitize_callback' => 'lawn_gardner_sanitize_choices'
	));
	$wp_customize->add_control('lawn_gardner_post_layout',array(
        'type' => 'select',
        'label' => esc_html__('Single Post Layout','lawn-gardner'),
        'section' => 'lawn_gardner_additional_section',
        'choices' => array(
            'layout-1' => esc_html__('Sidebar On Right','lawn-gardner'),
            'layout-2' => esc_html__('Sidebar On Left','lawn-gardner'),
			'layout-3' => esc_html__('Full Width Layout','lawn-gardner')
        ),
	) );

	/*single page layout*/
	$wp_customize->add_setting('lawn_gardner_page_layout',array(
        'default' => 'layout-1',
        'sanitize_callback' => 'lawn_gardner_sanitize_choices'
	));
	$wp_customize->add_control('lawn_gardner_page_layout',array(
        'type' => 'select',
        'label' => esc_html__('Single Page Layout','lawn-gardner'),
        'section' => 'lawn_gardner_additional_section',
        'choices' => array(
            'layout-1' => esc_html__('Sidebar On Right','lawn-gardner'),
            'layout-2' => esc_html__('Sidebar On Left','lawn-gardner'),
			'layout-3' => esc_html__('Full Width Layout','lawn-gardner')
        ),
	) );

	/*Archive Post Options*/
	$wp_customize->add_section('lawn_gardner_blog_post_section', array(
		'priority'       => 5,
		'capability'     => 'edit_theme_options',
		'theme_supports' => '',
		'title'          => __('Blog Page Options', 'lawn-gardner'),
		'panel'       => 'lawn_gardner_panel',
	));

	$wp_customize->add_setting('lawn_gardner_enable_blog_post_title',array(
		'capability'        => 'edit_theme_options',
		'transport'         => 'refresh',
		'default'           => 1,
		'sanitize_callback' => 'lawn_gardner_sanitize_checkbox',
	));
	$wp_customize->add_control('lawn_gardner_enable_blog_post_title',array(
		'label'       => __('Enable Blog Post Title', 'lawn-gardner'),
		'description' => __('Checked To Show Blog Post Title', 'lawn-gardner'),
		'section'     => 'lawn_gardner_blog_post_section',
		'type'        => 'checkbox',
	));

	$wp_customize->add_setting('lawn_gardner_enable_blog_post_meta',array(
		'capability'        => 'edit_theme_options',
		'transport'         => 'refresh',
		'default'           => 1,
		'sanitize_callback' => 'lawn_gardner_sanitize_checkbox',
	));
	$wp_customize->add_control('lawn_gardner_enable_blog_post_meta',array(
		'label'       => __('Enable Blog Post Meta', 'lawn-gardner'),
		'description' => __('Checked To Show Blog Post Meta Feilds', 'lawn-gardner'),
		'section'     => 'lawn_gardner_blog_post_section',
		'type'        => 'checkbox',
	));

	$wp_customize->add_setting('lawn_gardner_enable_blog_post_tags',array(
		'capability'        => 'edit_theme_options',
		'transport'         => 'refresh',
		'default'           => 1,
		'sanitize_callback' => 'lawn_gardner_sanitize_checkbox',
	));
	$wp_customize->add_control('lawn_gardner_enable_blog_post_tags',array(
		'label'       => __('Enable Blog Post Tags', 'lawn-gardner'),
		'description' => __('Checked To Show Blog Post Tags', 'lawn-gardner'),
		'section'     => 'lawn_gardner_blog_post_section',
		'type'        => 'checkbox',
	));

	$wp_customize->add_setting('lawn_gardner_enable_blog_post_image',array(
		'capability'        => 'edit_theme_options',
		'transport'         => 'refresh',
		'default'           => 1,
		'sanitize_callback' => 'lawn_gardner_sanitize_checkbox',
	));
	$wp_customize->add_control('lawn_gardner_enable_blog_post_image',array(
		'label'       => __('Enable Blog Post Image', 'lawn-gardner'),
		'description' => __('Checked To Show Blog Post Image', 'lawn-gardner'),
		'section'     => 'lawn_gardner_blog_post_section',
		'type'        => 'checkbox',
	));

	$wp_customize->add_setting('lawn_gardner_enable_blog_post_content',array(
		'capability'        => 'edit_theme_options',
		'transport'         => 'refresh',
		'default'           => 1,
		'sanitize_callback' => 'lawn_gardner_sanitize_checkbox',
	));
	$wp_customize->add_control('lawn_gardner_enable_blog_post_content',array(
		'label'       => __('Enable Blog Post Content', 'lawn-gardner'),
		'description' => __('Checked To Show Blog Post Content', 'lawn-gardner'),
		'section'     => 'lawn_gardner_blog_post_section',
		'type'        => 'checkbox',
	));

	$wp_customize->add_setting('lawn_gardner_enable_blog_post_button',array(
		'capability'        => 'edit_theme_options',
		'transport'         => 'refresh',
		'default'           => 1,
		'sanitize_callback' => 'lawn_gardner_sanitize_checkbox',
	));
	$wp_customize->add_control('lawn_gardner_enable_blog_post_button',array(
		'label'       => __('Enable Blog Post Read More Button', 'lawn-gardner'),
		'description' => __('Checked To Show Blog Post Read More Button', 'lawn-gardner'),
		'section'     => 'lawn_gardner_blog_post_section',
		'type'        => 'checkbox',
	));

	/*Blog post Content layout*/
	$wp_customize->add_setting('lawn_gardner_blog_Post_content_layout',array(
        'default' => 'Left',
        'sanitize_callback' => 'lawn_gardner_sanitize_choices'
	));
	$wp_customize->add_control('lawn_gardner_blog_Post_content_layout',array(
        'type' => 'select',
        'label' => esc_html__('Blog Post Content Layout','lawn-gardner'),
        'section' => 'lawn_gardner_blog_post_section',
        'choices' => array(
            'Left' => esc_html__('Left','lawn-gardner'),
            'Center' => esc_html__('Center','lawn-gardner'),
            'Right' => esc_html__('Right','lawn-gardner')
        ),
	) );

	/*Excerpt*/
    $wp_customize->add_setting(
		'lawn_gardner_excerpt_limit',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => '25',
			'sanitize_callback' => 'sanitize_text_field',
		)
	);

	$wp_customize->add_control(
		'lawn_gardner_excerpt_limit',
		array(
			'label'       => __('Excerpt Limit', 'lawn-gardner'),
			'section'     => 'lawn_gardner_blog_post_section',
			'type'        => 'number',
			'input_attrs' => array(
	            'min' => 2,
	             'max' => 50,
	             'step' => 2,
	         ),
		)
	);

	/*Archive Button Text*/
	$wp_customize->add_setting(
		'lawn_gardner_read_more_text',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => 'Continue Reading....',
			'sanitize_callback' => 'sanitize_text_field',
		)
	);

	$wp_customize->add_control(
		'lawn_gardner_read_more_text',
		array(
			'label'       => __('Edit Button Text ', 'lawn-gardner'),
			'section'     => 'lawn_gardner_blog_post_section',
			'type'        => 'text',
		)
	);

	/*Single Post Options*/
	$wp_customize->add_section('lawn_gardner_single_post_section', array(
		'priority'       => 5,
		'capability'     => 'edit_theme_options',
		'theme_supports' => '',
		'title'          => __('Single Post Options', 'lawn-gardner'),
		'panel'       => 'lawn_gardner_panel',
	));

	$wp_customize->add_setting('lawn_gardner_enable_single_blog_post_title',array(
		'capability'        => 'edit_theme_options',
		'transport'         => 'refresh',
		'default'           => 1,
		'sanitize_callback' => 'lawn_gardner_sanitize_checkbox',
	));
	$wp_customize->add_control('lawn_gardner_enable_single_blog_post_title',array(
		'label'       => __('Enable Single Post Title', 'lawn-gardner'),
		'description' => __('Checked To Show Single Blog Post Title', 'lawn-gardner'),
		'section'     => 'lawn_gardner_single_post_section',
		'type'        => 'checkbox',
	));

	$wp_customize->add_setting('lawn_gardner_enable_single_blog_post_meta',array(
		'capability'        => 'edit_theme_options',
		'transport'         => 'refresh',
		'default'           => 1,
		'sanitize_callback' => 'lawn_gardner_sanitize_checkbox',
	));
	$wp_customize->add_control('lawn_gardner_enable_single_blog_post_meta',array(
		'label'       => __('Enable Single Post Meta', 'lawn-gardner'),
		'description' => __('Checked To Show Single Blog Post Meta Feilds', 'lawn-gardner'),
		'section'     => 'lawn_gardner_single_post_section',
		'type'        => 'checkbox',
	));

	$wp_customize->add_setting('lawn_gardner_enable_single_blog_post_tags',array(
		'capability'        => 'edit_theme_options',
		'transport'         => 'refresh',
		'default'           => 1,
		'sanitize_callback' => 'lawn_gardner_sanitize_checkbox',
	));
	$wp_customize->add_control('lawn_gardner_enable_single_blog_post_tags',array(
		'label'       => __('Enable Single Post Tags', 'lawn-gardner'),
		'description' => __('Checked To Show Single Blog Post Tags', 'lawn-gardner'),
		'section'     => 'lawn_gardner_single_post_section',
		'type'        => 'checkbox',
	));

	$wp_customize->add_setting('lawn_gardner_enable_single_post_image',array(
		'capability'        => 'edit_theme_options',
		'transport'         => 'refresh',
		'default'           => 1,
		'sanitize_callback' => 'lawn_gardner_sanitize_checkbox',
	));
	$wp_customize->add_control('lawn_gardner_enable_single_post_image',array(
		'label'       => __('Enable Single Post Image', 'lawn-gardner'),
		'description' => __('Checked To Show Single Post Image', 'lawn-gardner'),
		'section'     => 'lawn_gardner_single_post_section',
		'type'        => 'checkbox',
	));

	$wp_customize->add_setting('lawn_gardner_enable_single_blog_post_content',array(
		'capability'        => 'edit_theme_options',
		'transport'         => 'refresh',
		'default'           => 1,
		'sanitize_callback' => 'lawn_gardner_sanitize_checkbox',
	));
	$wp_customize->add_control('lawn_gardner_enable_single_blog_post_content',array(
		'label'       => __('Enable Single Post Content', 'lawn-gardner'),
		'description' => __('Checked To Show Single Blog Post Content', 'lawn-gardner'),
		'section'     => 'lawn_gardner_single_post_section',
		'type'        => 'checkbox',
	));

	/*Related Post Enable Option*/
	$wp_customize->add_setting(
		'lawn_gardner_enable_related_post',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => 1,
			'sanitize_callback' => 'lawn_gardner_sanitize_checkbox',
		)
	);

	$wp_customize->add_control(
		'lawn_gardner_enable_related_post',
		array(
			'label'       => __('Enable Related Post', 'lawn-gardner'),
			'description' => __('Checked to show Related Post', 'lawn-gardner'),
			'section'     => 'lawn_gardner_single_post_section',
			'type'        => 'checkbox',
		)
	);

	/*Related post Edit Text*/
	$wp_customize->add_setting(
		'lawn_gardner_related_post_text',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => 'Related Post',
			'sanitize_callback' => 'sanitize_text_field',
		)
	);

	$wp_customize->add_control(
		'lawn_gardner_related_post_text',
		array(
			'label'       => __('Edit Related Post Text ', 'lawn-gardner'),
			'section'     => 'lawn_gardner_single_post_section',
			'type'        => 'text',
		)
	);	

	/*Related Post Per Page*/
	$wp_customize->add_setting(
		'lawn_gardner_related_post_count',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => '3',
			'sanitize_callback' => 'sanitize_text_field',
		)
	);

	$wp_customize->add_control(
		'lawn_gardner_related_post_count',
		array(
			'label'       => __('Related Post Count', 'lawn-gardner'),
			'section'     => 'lawn_gardner_single_post_section',
			'type'        => 'number',
			'input_attrs' => array(
	            'min' => 1,
	             'max' => 9,
	             'step' => 1,
	         ),
		)
	);

	/*
	* Customizer Global COlor
	*/

	/*Global Color Options*/
	$wp_customize->add_section('lawn_gardner_global_color_section', array(
		'priority'       => 1,
		'capability'     => 'edit_theme_options',
		'theme_supports' => '',
		'title'          => __('Global Color Options', 'lawn-gardner'),
		'panel'       => 'lawn_gardner_panel',
	));

	$wp_customize->add_setting( 'lawn_gardner_primary_color',
		array(
		'default'           => '#81b60c',
		'capability'        => 'edit_theme_options',
		'sanitize_callback' => 'sanitize_hex_color',
		)
	);
	$wp_customize->add_control( 
		new WP_Customize_Color_Control( 
		$wp_customize, 
		'lawn_gardner_primary_color',
		array(
			'label'      => esc_html__( 'Primary Color', 'lawn-gardner' ),
			'section'    => 'lawn_gardner_global_color_section',
			'settings'   => 'lawn_gardner_primary_color',
		) ) 
	);

	$wp_customize->add_setting( 'lawn_gardner_secondary_color',
		array(
		'default'           => '#123417',
		'capability'        => 'edit_theme_options',
		'sanitize_callback' => 'sanitize_hex_color',
		)
	);
	$wp_customize->add_control( 
		new WP_Customize_Color_Control( 
		$wp_customize, 
		'lawn_gardner_secondary_color',
		array(
			'label'      => esc_html__( 'Secondary Color', 'lawn-gardner' ),
			'section'    => 'lawn_gardner_global_color_section',
			'settings'   => 'lawn_gardner_secondary_color',
		) ) 
	);

	/*Typography Options*/
	$wp_customize->add_section( 'lawn_gardner_typography_section', array(
		'panel'       => 'lawn_gardner_panel',
        'title'    => __( 'Typography Options', 'lawn-gardner' ),
        'priority' => 2,
    ) );

    $wp_customize->add_setting( 'lawn_gardner_font_family', array(
		'default'           => 'default',
		'sanitize_callback' => 'lawn_gardner_sanitize_font_family',
	) );
	
	$wp_customize->add_control( 'lawn_gardner_font_family', array(
		'label'    => __( 'Global Font Family', 'lawn-gardner' ),
		'section'  => 'lawn_gardner_typography_section',
		'type'     => 'select',
		'choices'  => array(
			'default'          => __( 'Default (Theme Font)', 'lawn-gardner' ),
			'bad_script'       => 'Bad Script',
			'roboto'           => 'Roboto',
			'playfair_display' => 'Playfair Display',
			'open_sans'        => 'Open Sans',
			'lobster'          => 'Lobster',
			'merriweather'     => 'Merriweather',
			'oswald'           => 'Oswald',
			'raleway'          => 'Raleway',
		),
	) );

	/*Top Header Options*/
	$wp_customize->add_section('lawn_gardner_header_section', array(
		'priority'       => 5,
		'capability'     => 'edit_theme_options',
		'theme_supports' => '',
		'title'          => __('Top Header Options', 'lawn-gardner'),
		'panel'       => 'lawn_gardner_panel',
	));

	/*Top header section enable*/
	$wp_customize->add_setting(
		'lawn_gardner_enable_top_header',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => 1,
			'sanitize_callback' => 'lawn_gardner_sanitize_checkbox',
		)
	);

	$wp_customize->add_control(
		'lawn_gardner_enable_top_header',
		array(
			'label'       => __('Enable Top Header', 'lawn-gardner'),
			'description' => __('Checked to show the top header section.', 'lawn-gardner'),
			'section'     => 'lawn_gardner_header_section',
			'type'        => 'checkbox',
		)
	);

	/*Phone Number*/
	$wp_customize->add_setting(
		'lawn_gardner_location_option',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => 'ADDRESS: Riverside Works, Forde Rd, Newton Abbot, TQ12 4AD',
			'sanitize_callback' => 'sanitize_text_field',
		)
	);

	$wp_customize->add_control(
		'lawn_gardner_location_option',
		array(
			'label'       => __('Edit Location', 'lawn-gardner'),
			'section'     => 'lawn_gardner_header_section',
			'type'        => 'text',
		)
	);

	$wp_customize->add_setting('lawn_gardner_location_option_icon',array(
		'default'	=> 'fas fa-map-marker-alt',
		'sanitize_callback'	=> 'sanitize_text_field'
	));
	$wp_customize->add_control(new Lawn_Gardner_Icon_Changer(
        $wp_customize,'lawn_gardner_location_option_icon',array(
		'label'	=> __('Address Icon','lawn-gardner'),
		'transport' => 'refresh',
		'section'	=> 'lawn_gardner_header_section',
		'type'		=> 'icon'
	)));

	/*Email Address*/
	$wp_customize->add_setting(
		'lawn_gardner_email_address_option',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => 'MAIL: Gardeningcompany@gmail.com',
			'sanitize_callback' => 'sanitize_text_field',
		)
	);

	$wp_customize->add_control(
		'lawn_gardner_email_address_option',
		array(
			'label'       => __('Edit Email Address', 'lawn-gardner'),
			'section'     => 'lawn_gardner_header_section',
			'type'        => 'text',
		)
	);

	$wp_customize->add_setting('lawn_gardner_email_address_option_icon',array(
		'default'	=> 'fas fa-envelope',
		'sanitize_callback'	=> 'sanitize_text_field'
	));
	$wp_customize->add_control(new Lawn_Gardner_Icon_Changer(
        $wp_customize,'lawn_gardner_email_address_option_icon',array(
		'label'	=> __('Email Icon','lawn-gardner'),
		'transport' => 'refresh',
		'section'	=> 'lawn_gardner_header_section',
		'type'		=> 'icon'
	)));

	/*Enable Social Menu at the top*/
	$wp_customize->add_setting(
		'lawn_gardner_lawn_gardner_header_social_menu',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => 1,
			'sanitize_callback' => 'lawn_gardner_sanitize_checkbox',
		)
	);

	$wp_customize->add_control(
		'lawn_gardner_lawn_gardner_header_social_menu',
		array(
			'label'       => __('Enable Top Social Menu', 'lawn-gardner'),
			'description' => __('Checked to show the top social menu. Go to Dashboard >> Appearance >> Menus >> Create New Menu >> Add Custom Link >> Add Social Menu >> Checked Social Menu >> Save Menu.', 'lawn-gardner'),
			'section'     => 'lawn_gardner_header_section',
			'type'        => 'checkbox',
		)
	);

	/*Header Button Text*/
	$wp_customize->add_setting(
		'lawn_gardner_header_button_text',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => 'BOOK AN APPOINTMENT',
			'sanitize_callback' => 'sanitize_text_field',
		)
	);

	$wp_customize->add_control(
		'lawn_gardner_header_button_text',
		array(
			'label'       => __('Edit Button Text ', 'lawn-gardner'),
			'description' => __('Edit the header button text.', 'lawn-gardner'),
			'section'     => 'lawn_gardner_header_section',
			'type'        => 'text',
		)
	);

	/*Header Button URL*/
	$wp_customize->add_setting(
		'lawn_gardner_header_button_link',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => '',
			'sanitize_callback' => 'esc_url_raw',
		)
	);

	$wp_customize->add_control(
		'lawn_gardner_header_button_link',
		array(
			'label'       => __('Edit Button URL ', 'lawn-gardner'),
			'description' => __('Edit the header button url.', 'lawn-gardner'),
			'section'     => 'lawn_gardner_header_section',
			'type'        => 'url',
		)
	);

	/*Phone Number Text*/
	$wp_customize->add_setting(
		'lawn_gardner_phone_number_text',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => 'PHONE',
			'sanitize_callback' => 'sanitize_text_field',
		)
	);

	$wp_customize->add_control(
		'lawn_gardner_phone_number_text',
		array(
			'label'       => __('Edit Phone Text', 'lawn-gardner'),
			'section'     => 'lawn_gardner_header_section',
			'type'        => 'text',
		)
	);

	/*Phone Number*/
	$wp_customize->add_setting(
		'lawn_gardner_phone_number_option',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => '+00-123-4356-7890',
			'sanitize_callback' => 'sanitize_text_field',
		)
	);

	$wp_customize->add_control(
		'lawn_gardner_phone_number_option',
		array(
			'label'       => __('Edit Phone Number', 'lawn-gardner'),
			'section'     => 'lawn_gardner_header_section',
			'type'        => 'text',
		)
	);

	$wp_customize->add_setting('lawn_gardner_phone_number_option_icon',array(
		'default'	=> 'fas fa-phone-volume',
		'sanitize_callback'	=> 'sanitize_text_field'
	));
	$wp_customize->add_control(new Lawn_Gardner_Icon_Changer(
        $wp_customize,'lawn_gardner_phone_number_option_icon',array(
		'label'	=> __('Phone Icon','lawn-gardner'),
		'transport' => 'refresh',
		'section'	=> 'lawn_gardner_header_section',
		'type'		=> 'icon'
	)));

	$wp_customize->add_setting(
		'lawn_gardner_header_search',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => 1,
			'sanitize_callback' => 'lawn_gardner_sanitize_checkbox',
		)
	);

	$wp_customize->add_control(
		'lawn_gardner_header_search',
		array(
			'label'       => __('Enable Disable Search', 'lawn-gardner'),
			'description' => __('Enable or Disable header Search', 'lawn-gardner'),
			'section'     => 'lawn_gardner_header_section',
			'type'        => 'checkbox',
		)
	);

	/*
	* Customizer main slider section
	*/
	/*Main Slider Options*/
	$wp_customize->add_section('lawn_gardner_slider_section', array(
		'priority'       => 5,
		'capability'     => 'edit_theme_options',
		'theme_supports' => '',
		'title'          => __('Main Slider Options', 'lawn-gardner'),
		'panel'       => 'lawn_gardner_panel',
	));

	/*Main Slider Enable Option*/
	$wp_customize->add_setting(
		'lawn_gardner_enable_slider',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => 0,
			'sanitize_callback' => 'lawn_gardner_sanitize_checkbox',
		)
	);

	$wp_customize->add_control(
		'lawn_gardner_enable_slider',
		array(
			'label'       => __('Enable Main Slider', 'lawn-gardner'),
			'description' => __('Checked to show the main slider', 'lawn-gardner'),
			'section'     => 'lawn_gardner_slider_section',
			'type'        => 'checkbox',
		)
	);

	$wp_customize->add_setting(
		'lawn_gardner_slide_number',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'sanitize_callback' => 'sanitize_text_field',
		)
	);

	$wp_customize->add_control(
		'lawn_gardner_slide_number',
		array(
			'label'       => __('Number of slide to show', 'lawn-gardner'),
			'section'     => 'lawn_gardner_slider_section',
			'type'        => 'number',
			'input_attrs' => array(
				'min' => 1,     
				'max' => 3,   
			)
		)
	);

	$lawn_gardner_slide_count = (int)get_theme_mod('lawn_gardner_slide_number');

	for ($m=1; $m <= $lawn_gardner_slide_count; $m++) { 

		/*Main Slider Image*/
		$wp_customize->add_setting(
			'lawn_gardner_slider_image'.$m,
			array(
				'capability'    => 'edit_theme_options',
		        'default'       => '',
		        'transport'     => 'postMessage',
		        'sanitize_callback' => 'esc_url_raw',
	    	)
	    );

		$wp_customize->add_control( 
			new WP_Customize_Image_Control( $wp_customize, 
				'lawn_gardner_slider_image'.$m, 
				array(
			        'label' => __('Edit Slider Image ', 'lawn-gardner') .$m,
			        'description' => __('Edit the slider image.', 'lawn-gardner'),
			        'section' => 'lawn_gardner_slider_section',
				)
			)
		);

		/*Main Slider Heading*/
		$wp_customize->add_setting(
			'lawn_gardner_slider_heading'.$m,
			array(
				'capability'        => 'edit_theme_options',
				'transport'         => 'refresh',
				'default'           => '',
				'sanitize_callback' => 'sanitize_text_field',
			)
		);

		$wp_customize->add_control(
			'lawn_gardner_slider_heading'.$m,
			array(
				'label'       => __('Edit Heading Text ', 'lawn-gardner') .$m,
				'description' => __('Edit the slider heading text.', 'lawn-gardner'),
				'section'     => 'lawn_gardner_slider_section',
				'type'        => 'text',
			)
		);

		/*Main Slider Content*/
		$wp_customize->add_setting(
			'lawn_gardner_slider_text'.$m,
			array(
				'capability'        => 'edit_theme_options',
				'transport'         => 'refresh',
				'default'           => '',
				'sanitize_callback' => 'sanitize_text_field',
			)
		);

		$wp_customize->add_control(
			'lawn_gardner_slider_text'.$m,
			array(
				'label'       => __('Edit Content Text ', 'lawn-gardner') .$m,
				'description' => __('Edit the slider content text.', 'lawn-gardner'),
				'section'     => 'lawn_gardner_slider_section',
				'type'        => 'text',
			)
		);

		/*Main Slider Button1 Text*/
		$wp_customize->add_setting(
			'lawn_gardner_slider_button1_text'.$m,
			array(
				'capability'        => 'edit_theme_options',
				'transport'         => 'refresh',
				'default'           => '',
				'sanitize_callback' => 'sanitize_text_field',
			)
		);

		$wp_customize->add_control(
			'lawn_gardner_slider_button1_text'.$m,
			array(
				'label'       => __('Edit Button #1 Text ', 'lawn-gardner') .$m,
				'description' => __('Edit the slider button text.', 'lawn-gardner'),
				'section'     => 'lawn_gardner_slider_section',
				'type'        => 'text',
			)
		);

		/*Main Slider Button1 URL*/
		$wp_customize->add_setting(
			'lawn_gardner_slider_button1_link'.$m,
			array(
				'capability'        => 'edit_theme_options',
				'transport'         => 'refresh',
				'default'           => '',
				'sanitize_callback' => 'esc_url_raw',
			)
		);

		$wp_customize->add_control(
			'lawn_gardner_slider_button1_link'.$m,
			array(
				'label'       => __('Edit Button #1 URL ', 'lawn-gardner') .$m,
				'description' => __('Edit the slider button url.', 'lawn-gardner'),
				'section'     => 'lawn_gardner_slider_section',
				'type'        => 'url',
			)
		);
	}

	/*
	* Customizer project section
	*/
	/*Project Options*/
	$wp_customize->add_section('lawn_gardner_project_section', array(
		'priority'       => 5,
		'capability'     => 'edit_theme_options',
		'theme_supports' => '',
		'title'          => __('Project Options', 'lawn-gardner'),
		'panel'       => 'lawn_gardner_panel',
	));

	/*Project Enable Option*/
	$wp_customize->add_setting(
		'lawn_gardner_enable_project',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => 0,
			'sanitize_callback' => 'lawn_gardner_sanitize_checkbox',
		)
	);

	$wp_customize->add_control(
		'lawn_gardner_enable_project',
		array(
			'label'       => __('Enable Project Section', 'lawn-gardner'),
			'description' => __('Checked to show the project', 'lawn-gardner'),
			'section'     => 'lawn_gardner_project_section',
			'type'        => 'checkbox',
		)
	);

	/*Main Heading*/
	$wp_customize->add_setting(
		'lawn_gardner_project_heading',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => '',
			'sanitize_callback' => 'sanitize_text_field',
		)
	);

	$wp_customize->add_control(
		'lawn_gardner_project_heading',
		array(
			'label'       => __('Edit Main Heading ', 'lawn-gardner'),
			'description' => __('Edit the main section title.', 'lawn-gardner'),
			'section'     => 'lawn_gardner_project_section',
			'type'        => 'text',
		)
	);

	/*Main Tab1*/
	$wp_customize->add_setting(
		'lawn_gardner_project_tab1',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => '',
			'sanitize_callback' => 'sanitize_text_field',
		)
	);

	$wp_customize->add_control(
		'lawn_gardner_project_tab1',
		array(
			'label'       => __('Edit Tab1 Text', 'lawn-gardner'),
			'section'     => 'lawn_gardner_project_section',
			'type'        => 'text',
		)
	);

	for ($i=1; $i <= 3; $i++) { 

		/*Project Image*/
		$wp_customize->add_setting(
			'lawn_gardner_project_image_tab1'.$i,
			array(
				'capability'    => 'edit_theme_options',
		        'default'       => '',
		        'transport'     => 'postMessage',
		        'sanitize_callback' => 'esc_url_raw',
	    	)
	    );

		$wp_customize->add_control( 
			new WP_Customize_Image_Control( $wp_customize, 
				'lawn_gardner_project_image_tab1'.$i, 
				array(
			        'label' => __('Edit Project Image ', 'lawn-gardner') .$i,
			        'description' => __('Edit the project image.', 'lawn-gardner'),
			        'section' => 'lawn_gardner_project_section',
				)
			)
		);

		/*Project Title*/
		$wp_customize->add_setting(
			'lawn_gardner_project_box_heading_tab1'.$i,
			array(
				'capability'        => 'edit_theme_options',
				'transport'         => 'refresh',
				'default'           => '',
				'sanitize_callback' => 'sanitize_text_field',
			)
		);

		$wp_customize->add_control(
			'lawn_gardner_project_box_heading_tab1'.$i,
			array(
				'label'       => __('Edit Project Title ', 'lawn-gardner') .$i,
				'description' => __('Edit the project name.', 'lawn-gardner'),
				'section'     => 'lawn_gardner_project_section',
				'type'        => 'text',
			)
		);

		/*Project Text*/
		$wp_customize->add_setting(
			'lawn_gardner_project_box_content_tab1'.$i,
			array(
				'capability'        => 'edit_theme_options',
				'transport'         => 'refresh',
				'default'           => '',
				'sanitize_callback' => 'sanitize_text_field',
			)
		);

		$wp_customize->add_control(
			'lawn_gardner_project_box_content_tab1'.$i,
			array(
				'label'       => __('Edit Project Text ', 'lawn-gardner') .$i,
				'description' => __('Edit the project text.', 'lawn-gardner'),
				'section'     => 'lawn_gardner_project_section',
				'type'        => 'text',
			)
		);

		/*Project Content*/
		$wp_customize->add_setting(
			'lawn_gardner_project_box_text_tab1'.$i,
			array(
				'capability'        => 'edit_theme_options',
				'transport'         => 'refresh',
				'default'           => '',
				'sanitize_callback' => 'sanitize_text_field',
			)
		);

		$wp_customize->add_control(
			'lawn_gardner_project_box_text_tab1'.$i,
			array(
				'label'       => __('Edit Project Content ', 'lawn-gardner') .$i,
				'description' => __('Edit the project content.', 'lawn-gardner'),
				'section'     => 'lawn_gardner_project_section',
				'type'        => 'text',
			)
		);
	}

	/*Main Tab2*/
	$wp_customize->add_setting(
		'lawn_gardner_project_tab2',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => '',
			'sanitize_callback' => 'sanitize_text_field',
		)
	);

	$wp_customize->add_control(
		'lawn_gardner_project_tab2',
		array(
			'label'       => __('Edit Tab2 Text', 'lawn-gardner'),
			'section'     => 'lawn_gardner_project_section',
			'type'        => 'text',
		)
	);

	for ($i=1; $i <= 3; $i++) { 

		/*Project Image*/
		$wp_customize->add_setting(
			'lawn_gardner_project_image_tab2'.$i,
			array(
				'capability'    => 'edit_theme_options',
		        'default'       => '',
		        'transport'     => 'postMessage',
		        'sanitize_callback' => 'esc_url_raw',
	    	)
	    );

		$wp_customize->add_control( 
			new WP_Customize_Image_Control( $wp_customize, 
				'lawn_gardner_project_image_tab2'.$i, 
				array(
			        'label' => __('Edit Project Image ', 'lawn-gardner') .$i,
			        'description' => __('Edit the project image.', 'lawn-gardner'),
			        'section' => 'lawn_gardner_project_section',
				)
			)
		);

		/*Project Title*/
		$wp_customize->add_setting(
			'lawn_gardner_project_box_heading_tab2'.$i,
			array(
				'capability'        => 'edit_theme_options',
				'transport'         => 'refresh',
				'default'           => '',
				'sanitize_callback' => 'sanitize_text_field',
			)
		);

		$wp_customize->add_control(
			'lawn_gardner_project_box_heading_tab2'.$i,
			array(
				'label'       => __('Edit Project Title ', 'lawn-gardner') .$i,
				'description' => __('Edit the project name.', 'lawn-gardner'),
				'section'     => 'lawn_gardner_project_section',
				'type'        => 'text',
			)
		);

		/*Project Text*/
		$wp_customize->add_setting(
			'lawn_gardner_project_box_content_tab2'.$i,
			array(
				'capability'        => 'edit_theme_options',
				'transport'         => 'refresh',
				'default'           => '',
				'sanitize_callback' => 'sanitize_text_field',
			)
		);

		$wp_customize->add_control(
			'lawn_gardner_project_box_content_tab2'.$i,
			array(
				'label'       => __('Edit Project Text ', 'lawn-gardner') .$i,
				'description' => __('Edit the project Text.', 'lawn-gardner'),
				'section'     => 'lawn_gardner_project_section',
				'type'        => 'text',
			)
		);

		/*Project Content*/
		$wp_customize->add_setting(
			'lawn_gardner_project_box_text_tab2'.$i,
			array(
				'capability'        => 'edit_theme_options',
				'transport'         => 'refresh',
				'default'           => '',
				'sanitize_callback' => 'sanitize_text_field',
			)
		);

		$wp_customize->add_control(
			'lawn_gardner_project_box_text_tab2'.$i,
			array(
				'label'       => __('Edit Project Content ', 'lawn-gardner') .$i,
				'description' => __('Edit the project content.', 'lawn-gardner'),
				'section'     => 'lawn_gardner_project_section',
				'type'        => 'text',
			)
		);
	}

	/*Main Tab3*/
	$wp_customize->add_setting(
		'lawn_gardner_project_tab3',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => '',
			'sanitize_callback' => 'sanitize_text_field',
		)
	);

	$wp_customize->add_control(
		'lawn_gardner_project_tab3',
		array(
			'label'       => __('Edit Tab3 Text', 'lawn-gardner'),
			'section'     => 'lawn_gardner_project_section',
			'type'        => 'text',
		)
	);

	for ($i=1; $i <= 3; $i++) { 

		/*Project Image*/
		$wp_customize->add_setting(
			'lawn_gardner_project_image_tab3'.$i,
			array(
				'capability'    => 'edit_theme_options',
		        'default'       => '',
		        'transport'     => 'postMessage',
		        'sanitize_callback' => 'esc_url_raw',
	    	)
	    );

		$wp_customize->add_control( 
			new WP_Customize_Image_Control( $wp_customize, 
				'lawn_gardner_project_image_tab3'.$i, 
				array(
			        'label' => __('Edit Project Image ', 'lawn-gardner') .$i,
			        'description' => __('Edit the project image.', 'lawn-gardner'),
			        'section' => 'lawn_gardner_project_section',
				)
			)
		);

		/*Project Title*/
		$wp_customize->add_setting(
			'lawn_gardner_project_box_heading_tab3'.$i,
			array(
				'capability'        => 'edit_theme_options',
				'transport'         => 'refresh',
				'default'           => '',
				'sanitize_callback' => 'sanitize_text_field',
			)
		);

		$wp_customize->add_control(
			'lawn_gardner_project_box_heading_tab3'.$i,
			array(
				'label'       => __('Edit Project Title ', 'lawn-gardner') .$i,
				'description' => __('Edit the project name.', 'lawn-gardner'),
				'section'     => 'lawn_gardner_project_section',
				'type'        => 'text',
			)
		);

		/*Project Text*/
		$wp_customize->add_setting(
			'lawn_gardner_project_box_content_tab3'.$i,
			array(
				'capability'        => 'edit_theme_options',
				'transport'         => 'refresh',
				'default'           => '',
				'sanitize_callback' => 'sanitize_text_field',
			)
		);

		$wp_customize->add_control(
			'lawn_gardner_project_box_content_tab3'.$i,
			array(
				'label'       => __('Edit Project Content ', 'lawn-gardner') .$i,
				'description' => __('Edit the project Text.', 'lawn-gardner'),
				'section'     => 'lawn_gardner_project_section',
				'type'        => 'text',
			)
		);

		/*Project Content*/
		$wp_customize->add_setting(
			'lawn_gardner_project_box_text_tab3'.$i,
			array(
				'capability'        => 'edit_theme_options',
				'transport'         => 'refresh',
				'default'           => '',
				'sanitize_callback' => 'sanitize_text_field',
			)
		);

		$wp_customize->add_control(
			'lawn_gardner_project_box_text_tab3'.$i,
			array(
				'label'       => __('Edit Project Content ', 'lawn-gardner') .$i,
				'description' => __('Edit the project content.', 'lawn-gardner'),
				'section'     => 'lawn_gardner_project_section',
				'type'        => 'text',
			)
		);
	}

	/*
	* Customizer Footer Section
	*/
	/*Footer Options*/
	$wp_customize->add_section('lawn_gardner_footer_section', array(
		'priority'       => 5,
		'capability'     => 'edit_theme_options',
		'theme_supports' => '',
		'title'          => __('Footer Options', 'lawn-gardner'),
		'panel'       => 'lawn_gardner_panel',
	));

	/*Footer Enable Option*/
	$wp_customize->add_setting(
		'lawn_gardner_enable_footer',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => 1,
			'sanitize_callback' => 'lawn_gardner_sanitize_checkbox',
		)
	);
	$wp_customize->add_control(
		'lawn_gardner_enable_footer',
		array(
			'label'       => __('Enable Footer', 'lawn-gardner'),
			'description' => __('Checked to show Footer', 'lawn-gardner'),
			'section'     => 'lawn_gardner_footer_section',
			'type'        => 'checkbox',
		)
	);

	/*Footer bg image Option*/
	$wp_customize->add_setting('lawn_gardner_footer_bg_image',array(
		'capability'        => 'edit_theme_options',
		'transport'         => 'refresh',
        'default'           => '',
        'sanitize_callback' => 'esc_url_raw',
    ));
    $wp_customize->add_control( new WP_Customize_Image_Control($wp_customize,'lawn_gardner_footer_bg_image',array(
        'label' => __('Footer Background Image','lawn-gardner'),
        'section' => 'lawn_gardner_footer_section',
        'priority' => 1,
    )));


	/*Footer Social Menu Option*/
	$wp_customize->add_setting(
		'lawn_gardner_lawn_gardner_footer_social_menu',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => 1,
			'sanitize_callback' => 'lawn_gardner_sanitize_checkbox',
		)
	);

	$wp_customize->add_control(
		'lawn_gardner_lawn_gardner_footer_social_menu',
		array(
			'label'       => __('Enable Footer Social Menu', 'lawn-gardner'),
			'description' => __('Checked to show the footer social menu. Go to Dashboard >> Appearance >> Menus >> Create New Menu >> Add Custom Link >> Add Social Menu >> Checked Social Menu >> Save Menu.', 'lawn-gardner'),
			'section'     => 'lawn_gardner_footer_section',
			'type'        => 'checkbox',
		)
	);	

	/*Go To Top Option*/
	$wp_customize->add_setting(
		'lawn_gardner_enable_go_to_top_option',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => 1,
			'sanitize_callback' => 'lawn_gardner_sanitize_checkbox',
		)
	);

	$wp_customize->add_control(
		'lawn_gardner_enable_go_to_top_option',
		array(
			'label'       => __('Enable Go To Top', 'lawn-gardner'),
			'description' => __('Checked to enable Go To Top option.', 'lawn-gardner'),
			'section'     => 'lawn_gardner_footer_section',
			'type'        => 'checkbox',
		)
	);

	$wp_customize->add_setting('lawn_gardner_go_to_top_position',array(
        'capability'        => 'edit_theme_options',
		'transport'         => 'refresh',
		'default'           => 'Right',
        'sanitize_callback' => 'lawn_gardner_sanitize_choices'
    ));
    $wp_customize->add_control('lawn_gardner_go_to_top_position',array(
        'type' => 'select',
        'section' => 'lawn_gardner_footer_section',
        'label' => esc_html__('Go To Top Positions','lawn-gardner'),
        'choices' => array(
            'Right' => __('Right','lawn-gardner'),
            'Left' => __('Left','lawn-gardner'),
            'Center' => __('Center','lawn-gardner')
        ),
    ) );

	/*Footer Copyright Text Enable*/
	$wp_customize->add_setting(
		'lawn_gardner_copyright_option',
		array(
			'capability'        => 'edit_theme_options',
			'transport'         => 'refresh',
			'default'           => '',
			'sanitize_callback' => 'sanitize_text_field',
		)
	);

	$wp_customize->add_control(
		'lawn_gardner_copyright_option',
		array(
			'label'       => __('Edit Copyright Text', 'lawn-gardner'),
			'description' => __('Edit the Footer Copyright Section.', 'lawn-gardner'),
			'section'     => 'lawn_gardner_footer_section',
			'type'        => 'text',
		)
	);
}
add_action( 'customize_register', 'lawn_gardner_customize_register' );



/**
 * Render the site title for the selective refresh partial.
 *
 * @return void
 */
function lawn_gardner_customize_partial_blogname() {
	bloginfo( 'name' );
}

/**
 * Render the site tagline for the selective refresh partial.
 *
 * @return void
 */
function lawn_gardner_customize_partial_blogdescription() {
	bloginfo( 'description' );
}

/**
 * Binds JS handlers to make Theme Customizer preview reload changes asynchronously.
 */
function lawn_gardner_customize_preview_js() {
	wp_enqueue_script( 'lawn-gardner-customizer', get_template_directory_uri() . '/js/customizer.js', array( 'customize-preview' ), LAWN_GARDNER_VERSION, true );
}
add_action( 'customize_preview_init', 'lawn_gardner_customize_preview_js' );


/**
 * Singleton class for handling the theme's customizer integration.
 *
 * @since  1.0.0
 * @access public
 */
final class Lawn_Gardner_Customize {

	/**
	 * Returns the instance.
	 *
	 * @since  1.0.0
	 * @access public
	 * @return object
	 */
	public static function get_instance() {

		static $lawn_gardner_instance = null;

		if ( is_null( $lawn_gardner_instance ) ) {
			$lawn_gardner_instance = new self;
			$lawn_gardner_instance->setup_actions();
		}

		return $lawn_gardner_instance;
	}

	/**
	 * Constructor method.
	 *
	 * @since  1.0.0
	 * @access private
	 * @return void
	 */
	private function __construct() {}

	/**
	 * Sets up initial actions.
	 *
	 * @since  1.0.0
	 * @access private
	 * @return void
	 */
	private function setup_actions() {

		// Register panels, sections, settings, controls, and partials.
		add_action( 'customize_register', array( $this, 'sections' ) );

		// Register scripts and styles for the controls.
		add_action( 'customize_controls_enqueue_scripts', array( $this, 'enqueue_control_scripts' ), 0 );
	}

	/**
	 * Sets up the customizer sections.
	 *
	 * @since  1.0.0
	 * @access public
	 * @param  object  $lawn_gardner_manager
	 * @return void
	*/
	public function sections( $lawn_gardner_manager ) {

		// Load custom sections.
		load_template( trailingslashit( get_template_directory() ) . '/revolution/inc/section-pro.php' );

		// Register custom section types.
		$lawn_gardner_manager->register_section_type( 'lawn_gardner_Customize_Section_Pro' );

		// Register sections.
		$lawn_gardner_manager->add_section( new Lawn_Gardner_Customize_Section_Pro( $lawn_gardner_manager,'lawn_gardner_go_pro', array(
			'priority'   => 1,
			'title'    => esc_html__( 'Lawn Gardner Pro', 'lawn-gardner' ),
			'pro_text' => esc_html__( 'Buy Pro', 'lawn-gardner' ),
			'pro_url'    => esc_url( LAWN_GARDNER_BUY_NOW ),
		) )	);

		// Register sections.
		$lawn_gardner_manager->add_section( new Lawn_Gardner_Customize_Section_Pro( $lawn_gardner_manager,'lawn_gardner_lite_documentation', array(
			'priority'   => 1,
			'title'    => esc_html__( 'Lite Documentation', 'lawn-gardner' ),
			'pro_text' => esc_html__( 'Instruction', 'lawn-gardner' ),
			'pro_url'    => esc_url( LAWN_GARDNER_LITE_DOC ),
		) )	);

		$lawn_gardner_manager->add_section( new Lawn_Gardner_Customize_Section_Pro( $lawn_gardner_manager, 'lawn_gardner_live_demo', array(
		    'priority'   => 1,
		    'title'      => esc_html__( 'Pro Theme Demo', 'lawn-gardner' ),
		    'pro_text'   => esc_html__( 'Live Preview', 'lawn-gardner' ),
		    'pro_url'    => esc_url( LAWN_GARDNER_LIVE_DEMO ),
		) ) );	
		}

	/**
	 * Loads theme customizer CSS.
	 *
	 * @since  1.0.0
	 * @access public
	 * @return void
	 */
	public function enqueue_control_scripts() {

		wp_enqueue_script( 'lawn-gardner-customize-controls', trailingslashit( get_template_directory_uri() ) . '/revolution/assets/js/customize-controls.js', array( 'customize-controls' ) );

		wp_enqueue_style( 'lawn-gardner-customize-controls', trailingslashit( get_template_directory_uri() ) . '/revolution/assets/css/customize-controls.css' );
	}
}

// Doing this customizer thang!
Lawn_Gardner_Customize::get_instance();
