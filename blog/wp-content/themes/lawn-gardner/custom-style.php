<?php 
	$lawn_gardner_custom_css ='';

/*----------------Related Product show/hide -------------------*/

$lawn_gardner_enable_related_product = get_theme_mod('lawn_gardner_enable_related_product',1);

	if($lawn_gardner_enable_related_product == 0){
		$lawn_gardner_custom_css .='.related.products{';
			$lawn_gardner_custom_css .='display: none;';
		$lawn_gardner_custom_css .='}';
	}

/*----------------blog post content alignment -------------------*/

$lawn_gardner_blog_Post_content_layout = get_theme_mod( 'lawn_gardner_blog_Post_content_layout','Left');
    if($lawn_gardner_blog_Post_content_layout == 'Left'){
		$lawn_gardner_custom_css .='.ct-post-wrapper .card-item {';
			$lawn_gardner_custom_css .='text-align:start;';
		$lawn_gardner_custom_css .='}';
	}else if($lawn_gardner_blog_Post_content_layout == 'Center'){
		$lawn_gardner_custom_css .='.ct-post-wrapper .card-item {';
			$lawn_gardner_custom_css .='text-align:center;';
		$lawn_gardner_custom_css .='}';
	}else if($lawn_gardner_blog_Post_content_layout == 'Right'){
		$lawn_gardner_custom_css .='.ct-post-wrapper .card-item {';
			$lawn_gardner_custom_css .='text-align:end;';
		$lawn_gardner_custom_css .='}';
	}

	/*--------------------------- Footer background image -------------------*/

    $lawn_gardner_footer_bg_image = get_theme_mod('lawn_gardner_footer_bg_image');
    if($lawn_gardner_footer_bg_image != false){
        $lawn_gardner_custom_css .='.footer-top{';
            $lawn_gardner_custom_css .='background: url('.esc_attr($lawn_gardner_footer_bg_image).');';
        $lawn_gardner_custom_css .='}';
    }

	/*--------------------------- Go to top positions -------------------*/

    $lawn_gardner_go_to_top_position = get_theme_mod( 'lawn_gardner_go_to_top_position','Right');
    if($lawn_gardner_go_to_top_position == 'Right'){
        $lawn_gardner_custom_css .='.footer-go-to-top{';
            $lawn_gardner_custom_css .='right: 20px;';
        $lawn_gardner_custom_css .='}';
    }else if($lawn_gardner_go_to_top_position == 'Left'){
        $lawn_gardner_custom_css .='.footer-go-to-top{';
            $lawn_gardner_custom_css .='left: 20px;';
        $lawn_gardner_custom_css .='}';
    }else if($lawn_gardner_go_to_top_position == 'Center'){
        $lawn_gardner_custom_css .='.footer-go-to-top{';
            $lawn_gardner_custom_css .='right: 50%;left: 50%;';
        $lawn_gardner_custom_css .='}';
    }

    /*--------------------------- Woocommerce Product Sale Positions -------------------*/

    $lawn_gardner_product_sale = get_theme_mod( 'lawn_gardner_woocommerce_product_sale','Right');
    if($lawn_gardner_product_sale == 'Right'){
        $lawn_gardner_custom_css .='.woocommerce ul.products li.product .onsale{';
            $lawn_gardner_custom_css .='left: auto; ';
        $lawn_gardner_custom_css .='}';
    }else if($lawn_gardner_product_sale == 'Left'){
        $lawn_gardner_custom_css .='.woocommerce ul.products li.product .onsale{';
            $lawn_gardner_custom_css .='right: auto;left:0;';
        $lawn_gardner_custom_css .='}';
    }else if($lawn_gardner_product_sale == 'Center'){
        $lawn_gardner_custom_css .='.woocommerce ul.products li.product .onsale{';
            $lawn_gardner_custom_css .='right: 50%; left: 50%; ';
        $lawn_gardner_custom_css .='}';
    }


    /*-------------------- Primary Color -------------------*/

	$lawn_gardner_primary_color = get_theme_mod('lawn_gardner_primary_color', '#81b60c'); // Add a fallback if the color isn't set

	if ($lawn_gardner_primary_color) {
		$lawn_gardner_custom_css .= ':root {';
		$lawn_gardner_custom_css .= '--secondary-color: ' . esc_attr($lawn_gardner_primary_color) . ';';
		$lawn_gardner_custom_css .= '}';
	}

    /*-------------------- Secondary Color -------------------*/

	$lawn_gardner_secondary_color = get_theme_mod('lawn_gardner_secondary_color', '#123417'); // Add a fallback if the color isn't set

	if ($lawn_gardner_secondary_color) {
		$lawn_gardner_custom_css .= ':root {';
		$lawn_gardner_custom_css .= '--tertiary-color: ' . esc_attr($lawn_gardner_secondary_color) . ';';
		$lawn_gardner_custom_css .= '}';
	}

    /*----------------Enable/Disable Breadcrumbs -------------------*/

    $lawn_gardner_enable_breadcrumbs = get_theme_mod('lawn_gardner_enable_breadcrumbs',1);

    if($lawn_gardner_enable_breadcrumbs == 0){
        $lawn_gardner_custom_css .='.lawn-gardner-breadcrumbs, nav.woocommerce-breadcrumb{';
            $lawn_gardner_custom_css .='display: none;';
        $lawn_gardner_custom_css .='}';
    }