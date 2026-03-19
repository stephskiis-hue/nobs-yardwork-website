<?php
/**
 * @package Demo Import
 * @since 1.0.0
 */

class ThemeWhizzie {

	protected $version = '1.1.0';

	/** @var string Current theme name, used as namespace in actions. */
	protected $theme_name = '';
	protected $theme_title = '';

	/** @var string Demo Import page slug and title. */
	protected $page_slug = '';
	protected $page_title = '';

	/** @var array Demo Import steps set by user. */
	protected $config_steps = array();
	public $parent_slug;
	/**
	 * Constructor
	 *
	 * @param $lawn_gardner_config	Our config parameters
	*/
	public function __construct( $lawn_gardner_config ) {
		$this->set_vars( $lawn_gardner_config );
		$this->init();
	}

	/**
	 * Set some settings
	 * @since 1.0.0
	 * @param $lawn_gardner_config	Our config parameters
	*/
	public function set_vars( $lawn_gardner_config ) {
		if( isset( $lawn_gardner_config['page_slug'] ) ) {
			$this->page_slug = esc_attr( $lawn_gardner_config['page_slug'] );
		}
		if( isset( $lawn_gardner_config['page_title'] ) ) {
			$this->page_title = esc_attr( $lawn_gardner_config['page_title'] );
		}
		if( isset( $lawn_gardner_config['steps'] ) ) {
			$this->config_steps = $lawn_gardner_config['steps'];
		}

		$current_theme = wp_get_theme();
		$this->theme_title = $current_theme->get( 'Name' );
		$this->theme_name = strtolower( preg_replace( '#[^a-zA-Z]#', '', $current_theme->get( 'Name' ) ) );
		$this->page_slug = apply_filters( $this->theme_name . '_theme_setup_wizard_page_slug', $this->theme_name . '-demoimport' );
		$this->parent_slug = apply_filters( $this->theme_name . '_theme_setup_wizard_parent_slug', '' );
	}

	/**
	 * Hooks and filters
	 * @since 1.0.0
	*/
	public function init() {
		add_action( 'admin_enqueue_scripts', array( $this, 'enqueue_scripts' ) );
		add_action( 'admin_menu', array( $this, 'menu_page' ) );
		add_action( 'wp_ajax_setup_widgets', array( $this, 'setup_widgets' ) );
	}
	
	public function enqueue_scripts() {
		wp_enqueue_style( 'demo-import-style', get_template_directory_uri() . '/demo-import/assets/css/demo-import-style.css');
		wp_register_script( 'demo-import-script', get_template_directory_uri() . '/demo-import/assets/js/demo-import-script.js', array( 'jquery' ), time() );
		wp_localize_script(
			'demo-import-script',
			'lawn_gardner_whizzie_params',
			array(
				'ajaxurl' 		=> admin_url( 'admin-ajax.php' ),
				'wpnonce' 		=> wp_create_nonce( 'whizzie_nonce' ),
				'verify_text'	=> esc_html( 'verifying', 'lawn-gardner' )
			)
		);
		wp_enqueue_script( 'demo-import-script' );
	}

	/**  Make a modal screen for the wizard **/
	public function menu_page() {
		add_menu_page( esc_html( $this->page_title ), esc_html( $this->page_title ), 'manage_options', $this->page_slug, array( $this, 'lawn_gardner_guide' ) ,'',40);
	}

	/** Make an interface for the wizard **/
	public function wizard_page() {
		/* If we arrive here, we have the filesystem */ ?>
		<div class="wrap">
			<?php echo '<div class="whizzie-wrap">';
				// The wizard is a list with only one item visible at a time
				$steps = $this->get_steps();
				echo '<ul class="whizzie-nav wizard-icon-nav">';?>
				<?php
					$stepI=1;
					foreach( $steps as $step ) {
						$stepAct=($stepI ==1)? 1 : 0;
						if( isset( $step['icon_text'] ) && $step['icon_text'] ) {
							echo '<li class="commom-cls nav-step-' . esc_attr( $step['id'] ) . '" wizard-steps="step-'.esc_attr( $step['id'] ).'" data-enable="'.$stepAct.'">
							<p>'.esc_attr( $step['icon_text'] ).'</p>
							</li>';
						}
					$stepI++;}
			 	echo '</ul>';
				echo '<ul class="whizzie-menu wizard-menu-page">';
				foreach( $steps as $step ) {
					$class = 'step step-' . esc_attr( $step['id'] );
					echo '<li data-step="' . esc_attr( $step['id'] ) . '" class="' . esc_attr( $class ) . '" >';
						$content = call_user_func( array( $this, $step['view'] ) );
						printf('<div class="wizard-button-wrapper">');
							if( isset( $step['button_text_one'] )) {
								printf(
									'<div class="button-wrap button-wrap-one">
										<a href="#" class="button button-primary do-it" data-callback="install_widgets" data-step="widgets"><p class="demo-type-text">%s</p></a>
									</div>',
									esc_html( $step['button_text_one'] )
								);
							}
						printf('</div>');
					echo '</li>';
				}
				echo '</ul>';
				?>
				<div class="step-loading"><span class="spinner">
					<img src="<?php echo esc_url(get_template_directory_uri().'/demo-import/assets/images/Spinner-Animaion.gif'); ?>">
				</span></div>
			<?php echo '</div>';?>
		</div>
	<?php }

	/**
	 * Set options for the steps
	 * @return Array
	*/
	public function get_steps() {
		$dev_steps = $this->config_steps;
		$steps = array(
			'widgets' => array(
				'id'			=> 'widgets',
				'title'			=> __( 'Customizer', 'lawn-gardner' ),
				'icon'			=> 'welcome-widgets-menus',
				'view'			=> 'get_step_widgets',
				'callback'		=> 'install_widgets',
				'button_text_one'	=> __( 'Import Demo', 'lawn-gardner' ),
				'can_skip'		=> true,
				'icon_text'      => 'Import Demo'
			),
			'done' => array(
				'id'			=> 'done',
				'title'			=> __( 'All Done', 'lawn-gardner' ),
				'icon'			=> 'yes',
				'view'			=> 'get_step_done',
				'callback'		=> '',
				'icon_text'      => 'Done'
			)
		);
		// Iterate through each step and replace with dev config values
		if( $dev_steps ) {
			// Configurable elements - these are the only ones the dev can update from config.php
			$can_config = array( 'title', 'icon', 'button_text', 'can_skip' );
			foreach( $dev_steps as $dev_step ) {
				// We can only proceed if an ID exists and matches one of our IDs
				if( isset( $dev_step['id'] ) ) {
					$id = $dev_step['id'];
					if( isset( $steps[$id] ) ) {
						foreach( $can_config as $element ) {
							if( isset( $dev_step[$element] ) ) {
								$steps[$id][$element] = $dev_step[$element];
							}
						}
					}
				}
			}
		}
		return $steps;
	}

	/**    Print the content for the intro step     **/
		public function get_step_importer() { ?>
		<div class="summary">
			<p>
				<?php esc_html_e('Thank you for choosing this Lawn Gardner Theme. Using this quick setup wizard, you will be able to configure your new website and get it running in just a few minutes. Just follow these simple steps mentioned in the wizard and get started with your website.','lawn-gardner'); ?>
			</p>
		</div>
	<?php }

	/**   Print the content for the widgets step   **/
	public function get_step_widgets() { ?>
		<div class="summary">
			<p>
				<?php esc_html_e('This theme allows you to import demo content and add widgets. Install them using the button below. You can also update or deactivate them using the Customizer.','lawn-gardner'); ?>
			</p>
		</div>
	<?php }

	/** Print the content for the final step **/
	public function get_step_done() { ?>

		<div class="setup-finish">
			<p>
				<?php echo esc_html('Your demo content has been imported successfully. Click the finish button for more information.'); ?>
			</p>
			<div class="finish-buttons">
				<a href="<?php echo esc_url( admin_url( 'themes.php?page=lawn-gardner-getstart-page' ) ); ?>" class="wz-btn-customizer" target="_blank"><?php esc_html_e('About Lawn Gardner','lawn-gardner') ?></a>
				<a href="<?php echo esc_url(admin_url('/customize.php')); ?>" class="wz-btn-customizer" target="_blank"><?php esc_html_e('Customize Your Demo','lawn-gardner') ?></a>
				<a href="" class="wz-btn-builder" target="_blank"><?php esc_html_e('Customize Your Demo','lawn-gardner'); ?></a>
				<a href="<?php echo esc_url(home_url()); ?>" class="wz-btn-visit-site" target="_blank"><?php esc_html_e('Visit Your Site','lawn-gardner'); ?></a>
			</div>
			<div class="finish-buttons">
				<a href="<?php echo esc_url(admin_url()); ?>" class="button button-primary"><?php esc_html_e('Finish','lawn-gardner'); ?></a>
			</div>
		</div>

	<?php }


	public function lawn_gardner_customizer_nav_menu() {
		// ------- Create Primary Menu --------
		$lawn_gardner_themename = 'Lawn Gardner'; // Ensure the theme name is set
		$lawn_gardner_menuname = $lawn_gardner_themename . ' Primary Menu';
		$lawn_gardner_menulocation = 'menu-1';
		$lawn_gardner_menu_exists = wp_get_nav_menu_object($lawn_gardner_menuname);

		if (!$lawn_gardner_menu_exists) {
			$lawn_gardner_menu_id = wp_create_nav_menu($lawn_gardner_menuname);

			// Home
			wp_update_nav_menu_item($lawn_gardner_menu_id, 0, array(
				'menu-item-title' => __('Home', 'lawn-gardner'),
				'menu-item-classes' => 'home',
				'menu-item-url' => home_url('/'),
				'menu-item-status' => 'publish'
			));

			// About
			$lawn_gardner_page_about = get_page_by_path('about');
			if($lawn_gardner_page_about){
				wp_update_nav_menu_item($lawn_gardner_menu_id, 0, array(
					'menu-item-title' => __('About', 'lawn-gardner'),
					'menu-item-classes' => 'about',
					'menu-item-url' => get_permalink($lawn_gardner_page_about),
					'menu-item-status' => 'publish'
				));
			}

			// Services
			$lawn_gardner_page_services = get_page_by_path('services');
			if($lawn_gardner_page_services){
				wp_update_nav_menu_item($lawn_gardner_menu_id, 0, array(
					'menu-item-title' => __('Services', 'lawn-gardner'),
					'menu-item-classes' => 'services',
					'menu-item-url' => get_permalink($lawn_gardner_page_services),
					'menu-item-status' => 'publish'
				));
			}

			// Blog
			$lawn_gardner_page_blog = get_page_by_path('blog');
			if($lawn_gardner_page_blog){
				wp_update_nav_menu_item($lawn_gardner_menu_id, 0, array(
					'menu-item-title' => __('Blog', 'lawn-gardner'),
					'menu-item-classes' => 'blog',
					'menu-item-url' => get_permalink($lawn_gardner_page_blog),
					'menu-item-status' => 'publish'
				));
			}

			// Contact Us
			$lawn_gardner_page_contact = get_page_by_path('contact');
			if($lawn_gardner_page_contact){
				wp_update_nav_menu_item($lawn_gardner_menu_id, 0, array(
					'menu-item-title' => __('Contact Us', 'lawn-gardner'),
					'menu-item-classes' => 'contact',
					'menu-item-url' => get_permalink($lawn_gardner_page_contact),
					'menu-item-status' => 'publish'
				));
			}

			// Assign menu to location if not set
			if (!has_nav_menu($lawn_gardner_menulocation)) {
				$lawn_gardner_locations = get_theme_mod('nav_menu_locations');
				$lawn_gardner_locations[$lawn_gardner_menulocation] = $lawn_gardner_menu_id; // Use $lawn_gardner_menu_id here
				set_theme_mod('nav_menu_locations', $lawn_gardner_locations);
			}
		}
	}

	public function lawn_gardner_social_menu() {

		// ------- Create Social Menu --------
		$lawn_gardner_menuname = $lawn_gardner_themename . 'Social Menu';
		$lawn_gardner_menulocation = 'social-menu';
		$lawn_gardner_menu_exists = wp_get_nav_menu_object( $lawn_gardner_menuname );

		if( !$lawn_gardner_menu_exists){
			$lawn_gardner_menu_id = wp_create_nav_menu($lawn_gardner_menuname);

			wp_update_nav_menu_item( $lawn_gardner_menu_id, 0, array(
				'menu-item-title'  => __( 'Facebook', 'lawn-gardner' ),
				'menu-item-url'    => 'https://www.facebook.com',
				'menu-item-status' => 'publish',
			) );

			wp_update_nav_menu_item( $lawn_gardner_menu_id, 0, array(
				'menu-item-title'  => __( 'Pinterest', 'lawn-gardner' ),
				'menu-item-url'    => 'https://www.pinterest.com',
				'menu-item-status' => 'publish',
			) );
	
			wp_update_nav_menu_item( $lawn_gardner_menu_id, 0, array(
				'menu-item-title'  => __( 'Twitter', 'lawn-gardner' ),
				'menu-item-url'    => 'https://www.twitter.com',
				'menu-item-status' => 'publish',
			) );
	
			wp_update_nav_menu_item( $lawn_gardner_menu_id, 0, array(
				'menu-item-title'  => __( 'Youtube', 'lawn-gardner' ),
				'menu-item-url'    => 'https://www.youtube.com',
				'menu-item-status' => 'publish',
			) );

			wp_update_nav_menu_item( $lawn_gardner_menu_id, 0, array(
				'menu-item-title'  => __( 'Instagram', 'lawn-gardner' ),
				'menu-item-url'    => 'https://www.instagram.com',
				'menu-item-status' => 'publish',
			) );

			if( !has_nav_menu( $lawn_gardner_menulocation ) ){
					$locations = get_theme_mod('nav_menu_locations');
					$locations[$lawn_gardner_menulocation] = $lawn_gardner_menu_id;
					set_theme_mod( 'nav_menu_locations', $locations );
			}
		}
	}

	/**
	* Imports the Demo Content
	* @since 1.1.0
	*/
	public function setup_widgets() {

		//................................................. MENU PAGES .................................................//
		
		$lawn_gardner_home_id='';
		$lawn_gardner_home_content = '';

		$lawn_gardner_home_title = 'Home';
		$lawn_gardner_home = array(
				'post_type' => 'page',
				'post_title' => $lawn_gardner_home_title,
				'post_content'  => $lawn_gardner_home_content,
				'post_status' => 'publish',
				'post_author' => 1,
				'post_slug' => 'home'
		);
		$lawn_gardner_home_id = wp_insert_post($lawn_gardner_home);

		//Set the home page template
		add_post_meta( $lawn_gardner_home_id, '_wp_page_template', 'revolution-home.php' );

		//Set the static front page
		$lawn_gardner_home = get_page_by_title( 'Home' );
		update_option( 'page_on_front', $lawn_gardner_home->ID );
		update_option( 'show_on_front', 'page' );


		// Create a posts page and assign the template
		$lawn_gardner_blog_title = 'Blog';
		$lawn_gardner_blog_check = get_page_by_path('blog');
		if (!$lawn_gardner_blog_check) {
			$lawn_gardner_blog = array(
				'post_type'    => 'page',
				'post_title'   => $lawn_gardner_blog_title,
				'post_status'  => 'publish',
				'post_author'  => 1,
				'post_name'    => 'blog' // Unique slug for the blog page
			);
			$lawn_gardner_blog_id = wp_insert_post($lawn_gardner_blog);

			// Set the posts page
			if (!is_wp_error($lawn_gardner_blog_id)) {
				update_option('page_for_posts', $lawn_gardner_blog_id);
			}
		}

		// Create a Contact Us page and assign the template
		$lawn_gardner_contact_title = 'Contact Us';
		$lawn_gardner_contact_check = get_page_by_path('contact');
		if (!$lawn_gardner_contact_check) {
			$lawn_gardner_contact = array(
				'post_type'    => 'page',
				'post_title'   => $lawn_gardner_contact_title,
				'post_content'   => '"More About The Free Gardener WordPress Theme"
										The theme typically boasts a range of homepage layouts, each thoughtfully crafted to suit different purposes. Whether you\'re aiming to showcase gardening services, exhibit outdoor products, or share insightful gardening tips, the Free Gardner theme offers tailored layouts to meet your needs. What sets this theme apart is its emphasis on customization, facilitated through an intuitive customization panel. Here, you can effortlessly tweak colors, fonts, layouts, and other visual elements to harmonize with your brand identity. For gardening-related businesses or blogs, image galleries are a pivotal feature. The Free Gardner theme generally integrates support for image galleries, enabling you to present gardening projects, landscape designs, plant collections, and outdoor events through high-quality visuals that captivate your visitors attention.

										Blog integration is another strength of this theme, featuring well-designed layouts and diverse post formats, allowing you to effectively share gardening insights, tips, and news. To encourage user engagement, the theme incorporates strategically placed call-to-action sections. Whether you\'re aiming to gather newsletter sign-ups or consultation requests, these sections serve as focal points to guide visitors towards key actions. Additionally, the theme emphasizes the integration of social media elements, simplifying the process of connecting with your audience through various platforms. Behind the scenes, the Free Gardner theme is built with search engine optimization (SEO) in mind, adhering to best practices to enhance your website\'s discoverability and ranking on search engines.

										The inclusion of contact forms streamlines communication with your audience, while user-friendly widgets provide options for displaying recent posts, popular content, and social media feeds. The theme typically comes with comprehensive documentation and basic support, ensuring that you can set up, customize, and troubleshoot effectively. Furthermore, it\'s important to note that reputable theme developers regularly release updates to maintain compatibility with the latest WordPress version and address any security or functionality concerns. In sum, the Free Gardner WordPress theme offers a holistic package that caters to gardening enthusiasts, landscapers, and outdoor-focused businesses, enabling them to create an engaging and visually stunning online presence.',
					'post_status'  => 'publish',
				'post_author'  => 1,
				'post_name'    => 'contact' // Unique slug for the Contact Us page
			);
			wp_insert_post($lawn_gardner_contact);
		}

		// Create a About page and assign the template
		$lawn_gardner_about_title = 'About';
		$lawn_gardner_about_check = get_page_by_path('about');
		if (!$lawn_gardner_about_check) {
			$lawn_gardner_about = array(
				'post_type'    => 'page',
				'post_title'   => $lawn_gardner_about_title,
				'post_content'   => '"More About The Free Gardener WordPress Theme"
										The theme typically boasts a range of homepage layouts, each thoughtfully crafted to suit different purposes. Whether you\'re aiming to showcase gardening services, exhibit outdoor products, or share insightful gardening tips, the Free Gardner theme offers tailored layouts to meet your needs. What sets this theme apart is its emphasis on customization, facilitated through an intuitive customization panel. Here, you can effortlessly tweak colors, fonts, layouts, and other visual elements to harmonize with your brand identity. For gardening-related businesses or blogs, image galleries are a pivotal feature. The Free Gardner theme generally integrates support for image galleries, enabling you to present gardening projects, landscape designs, plant collections, and outdoor events through high-quality visuals that captivate your visitors attention.

										Blog integration is another strength of this theme, featuring well-designed layouts and diverse post formats, allowing you to effectively share gardening insights, tips, and news. To encourage user engagement, the theme incorporates strategically placed call-to-action sections. Whether you\'re aiming to gather newsletter sign-ups or consultation requests, these sections serve as focal points to guide visitors towards key actions. Additionally, the theme emphasizes the integration of social media elements, simplifying the process of connecting with your audience through various platforms. Behind the scenes, the Free Gardner theme is built with search engine optimization (SEO) in mind, adhering to best practices to enhance your website\'s discoverability and ranking on search engines.

										The inclusion of contact forms streamlines communication with your audience, while user-friendly widgets provide options for displaying recent posts, popular content, and social media feeds. The theme typically comes with comprehensive documentation and basic support, ensuring that you can set up, customize, and troubleshoot effectively. Furthermore, it\'s important to note that reputable theme developers regularly release updates to maintain compatibility with the latest WordPress version and address any security or functionality concerns. In sum, the Free Gardner WordPress theme offers a holistic package that caters to gardening enthusiasts, landscapers, and outdoor-focused businesses, enabling them to create an engaging and visually stunning online presence.',
					'post_status'  => 'publish',
				'post_author'  => 1,
				'post_name'    => 'about' // Unique slug for the About page
			);
			wp_insert_post($lawn_gardner_about);
		}

		// Create a Services page and assign the template
		$lawn_gardner_services_title = 'Services';
		$lawn_gardner_services_check = get_page_by_path('services');
		if (!$lawn_gardner_services_check) {
			$lawn_gardner_services = array(
				'post_type'    => 'page',
				'post_title'   => $lawn_gardner_services_title,
				'post_content'   => '"More About The Free Gardener WordPress Theme"
										The theme typically boasts a range of homepage layouts, each thoughtfully crafted to suit different purposes. Whether you\'re aiming to showcase gardening services, exhibit outdoor products, or share insightful gardening tips, the Free Gardner theme offers tailored layouts to meet your needs. What sets this theme apart is its emphasis on customization, facilitated through an intuitive customization panel. Here, you can effortlessly tweak colors, fonts, layouts, and other visual elements to harmonize with your brand identity. For gardening-related businesses or blogs, image galleries are a pivotal feature. The Free Gardner theme generally integrates support for image galleries, enabling you to present gardening projects, landscape designs, plant collections, and outdoor events through high-quality visuals that captivate your visitors attention.

										Blog integration is another strength of this theme, featuring well-designed layouts and diverse post formats, allowing you to effectively share gardening insights, tips, and news. To encourage user engagement, the theme incorporates strategically placed call-to-action sections. Whether you\'re aiming to gather newsletter sign-ups or consultation requests, these sections serve as focal points to guide visitors towards key actions. Additionally, the theme emphasizes the integration of social media elements, simplifying the process of connecting with your audience through various platforms. Behind the scenes, the Free Gardner theme is built with search engine optimization (SEO) in mind, adhering to best practices to enhance your website\'s discoverability and ranking on search engines.

										The inclusion of contact forms streamlines communication with your audience, while user-friendly widgets provide options for displaying recent posts, popular content, and social media feeds. The theme typically comes with comprehensive documentation and basic support, ensuring that you can set up, customize, and troubleshoot effectively. Furthermore, it\'s important to note that reputable theme developers regularly release updates to maintain compatibility with the latest WordPress version and address any security or functionality concerns. In sum, the Free Gardner WordPress theme offers a holistic package that caters to gardening enthusiasts, landscapers, and outdoor-focused businesses, enabling them to create an engaging and visually stunning online presence.',
					'post_status'  => 'publish',
				'post_author'  => 1,
				'post_name'    => 'services' // Unique slug for the Services page
			);
			wp_insert_post($lawn_gardner_services);
		}


		// ------------------------------------------ Header -------------------------------------- //

			set_theme_mod('lawn_gardner_location_option','ADDRESS: Riverside Works, Forde Rd, Newton Abbot, TQ12 4AD');
			set_theme_mod('lawn_gardner_email_address_option','MAIL: Gardeningcompany@gmail.com');

			set_theme_mod('lawn_gardner_header_button_text','BOOK AN APPOINTMENT');
			set_theme_mod('lawn_gardner_header_button_link','#');

			set_theme_mod('lawn_gardner_phone_number_text','PHONE');
			set_theme_mod('lawn_gardner_phone_number_option','+00-123-4356-7890');

			set_theme_mod('lawn_gardner_enable_slider',1);
			set_theme_mod('lawn_gardner_enable_project',1);
			
		// ------------------------------------------ Slider Section -------------------------------------- //

			set_theme_mod('lawn_gardner_slide_number','3');

			for($i=1;$i<=3;$i++){
				set_theme_mod( 'lawn_gardner_slider_image'.$i,get_template_directory_uri().'/revolution/assets/images/slider'.$i.'.png' );
				set_theme_mod( 'lawn_gardner_slider_heading'.$i, 'WE KNOW THE PLANT A BETTER' );
				set_theme_mod( 'lawn_gardner_slider_text'.$i, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam ac lacinia lacus, id fermentum est. Etiam eget egestas nulla, eu finibus urna.' );
				set_theme_mod( 'lawn_gardner_slider_button1_text'.$i, 'Read More' );
				set_theme_mod( 'lawn_gardner_slider_button1_link'.$i, '#' );
			}

		// ------------------------------------------ Chef Section -------------------------------------- //

			set_theme_mod('lawn_gardner_project_heading', 'Our Awesome Project');

			$lawn_gardner_tabs = array(
				'tab1' => array(
					'title'   => 'Landscaping',
					'heading' => 'LANDSCAPING',
					'images'  => array('project1.png', 'project2.png', 'project3.png'),
				),
				'tab2' => array(
					'title'   => 'Tree Planting',
					'heading' => 'TREE PLANTING',
					'images'  => array('project2.png', 'project1.png', 'project3.png'),
				),
				'tab3' => array(
					'title'   => 'Gardening',
					'heading' => 'GARDENING',
					'images'  => array('project3.png', 'project2.png', 'project1.png'),
				),
			);

			foreach ($lawn_gardner_tabs as $lawn_gardner_tab_key => $lawn_gardner_tab_data) {
				set_theme_mod("lawn_gardner_project_{$lawn_gardner_tab_key}", $lawn_gardner_tab_data['title']);

				foreach ($lawn_gardner_tab_data['images'] as $i => $filename) {
					$lawn_gardner_index = $i + 1; // to get 1-based keys (e.g., tab11, tab12, etc.)
					$lawn_gardner_image_url = get_template_directory_uri() . '/revolution/assets/images/' . $filename;

					set_theme_mod("lawn_gardner_project_image_{$lawn_gardner_tab_key}{$lawn_gardner_index}", $lawn_gardner_image_url);
					set_theme_mod("lawn_gardner_project_box_heading_{$lawn_gardner_tab_key}{$lawn_gardner_index}", $lawn_gardner_tab_data['heading']);
					set_theme_mod("lawn_gardner_project_box_content_{$lawn_gardner_tab_key}{$lawn_gardner_index}", 'Lorem ipsum dolor sit');
					set_theme_mod("lawn_gardner_project_box_text_{$lawn_gardner_tab_key}{$lawn_gardner_index}", 'Our long history and regular clients prove that our service.');
				}
			}

		
  	 	$this->lawn_gardner_customizer_nav_menu();
  	 	$this->lawn_gardner_social_menu();
	}

	public function lawn_gardner_guide() {
		$display_string = '';
		$return = add_query_arg( array()) ;
		$theme = wp_get_theme( 'lawn-gardner' );
		?>
		<div class="wrapper-info get-stared-page-wrap">
			<div class="wrapper-info-content">
				<div class="buynow__">
					<h2><?php esc_html_e( 'Welcome to Lawn Gardner', 'lawn-gardner' ); ?> <span class="version">Version: <?php echo esc_html($theme['Version']);?></span></h2>
					<p><?php esc_html_e('The quick setup wizard will assist you in configuring your new website. This wizard will import the demo content.', 'lawn-gardner'); ?></p>
				</div>
				<div class="buynow_">
					<a target="_blank" class="buynow_themepage" href="<?php echo esc_url('https://www.revolutionwp.com/products/lawn-care-wordpress-theme'); ?>"><?php echo esc_html__('Go Premium Now', 'lawn-gardner'); ?></a>
				</div>
			</div>
			<div class="tab-sec theme-option-tab">
				<div id="demo_offer" class="tabcontent open">
					<?php $this->wizard_page(); ?>
				</div>
			</div>
		</div>
	<?php }
}