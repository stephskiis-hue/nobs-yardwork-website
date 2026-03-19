<?php
/**
 * The header for our theme
 *
 * @package Lawn Gardner
 */

?>
<!doctype html>
<html <?php language_attributes(); ?>>
<head>
	<meta charset="<?php bloginfo( 'charset' ); ?>">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="profile" href="https://gmpg.org/xfn/11">

	<?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<div id="page" class="site">
	<a class="skip-link screen-reader-text" href="#primary"><?php esc_html_e( 'Skip to content', 'lawn-gardner' ); ?></a>
 <?php
$lawn_gardner_preloader_wrap = absint(get_theme_mod('lawn_gardner_enable_preloader', 0));
if($lawn_gardner_preloader_wrap == 1){ ?>

	<div id="loader">
		<div class="loader-container">
			<div id="preloader" class="loader-2">
				<div class="dot"></div>
			</div>
		</div>
	</div>

<?php } ?>

	<header id="masthead" class="site-header">

		<?php 
		$lawn_gardner_top_header = absint(get_theme_mod('lawn_gardner_enable_top_header', 1));

		$lawn_gardner_has_header_image = has_header_image();

		if($lawn_gardner_top_header == 1){ 
			?>		
			<div class="top-header-wrap">
				<div class="container">
					<div class="flex-row">
						<div class="top-header-left">
							<?php if ( get_theme_mod('lawn_gardner_location_option','ADDRESS: Riverside Works, Forde Rd, Newton Abbot, TQ12 4AD') ) : ?><span><i class="<?php echo esc_attr(get_theme_mod('lawn_gardner_location_option_icon','fas fa-map-marker-alt')); ?>"></i> <span class="Email-head"><?php esc_html_e( 'Address:', 'lawn-gardner' ); ?></span> <?php echo esc_html(get_theme_mod('lawn_gardner_location_option', 'ADDRESS: Riverside Works, Forde Rd, Newton Abbot, TQ12 4AD')); ?></span><?php endif; ?>
						</div>
						<div class="top-header-right">
							<?php if ( get_theme_mod('lawn_gardner_email_address_option','MAIL: Gardeningcompany@gmail.com') ) : ?><span><i class="<?php echo esc_attr(get_theme_mod('lawn_gardner_email_address_option_icon','fas fa-envelope')); ?>"></i> <span class="Email-head"><?php esc_html_e( 'Email:', 'lawn-gardner' ); ?> <?php echo esc_html(get_theme_mod('lawn_gardner_email_address_option', 'MAIL: Gardeningcompany@gmail.com')); ?></span><?php endif; ?>
						</div>
					</div>
				</div>
			</div>
		<?php } ?>

		<div class="main-header-wrap">
			<div class="container">
				<div class="top-box <?php echo esc_attr( get_theme_mod( 'lawn_gardner_enable_sticky_header', false ) ? 'sticky-header' : '' ); ?>" <?php if (!empty($lawn_gardner_has_header_image)) { ?> style="background-image: url(<?php echo header_image(); ?>);" <?php } ?>>
					<div class="flex-row">
						<div class="main-header main-header-box">
							<div class="site-branding">
								<?php
								the_custom_logo();
								if ( is_front_page() && is_home() ) :
									?>
								<?php if( get_theme_mod('lawn_gardner_site_title_text',true)){ ?>
									<h1 class="site-title"><a href="<?php echo esc_url( home_url( '/' ) ); ?>" rel="home"><?php bloginfo( 'name' ); ?></a></h1>
								<?php } ?>
									<?php
								else :
									?>
								<?php if( get_theme_mod('lawn_gardner_site_title_text',true)){ ?>
									<p class="site-title"><a href="<?php echo esc_url( home_url( '/' ) ); ?>" rel="home"><?php bloginfo( 'name' ); ?></a></p>
								<?php } ?>
									<?php
								endif;
								$lawn_gardner_description = get_bloginfo( 'description', 'display' );
								if ( $lawn_gardner_description || is_customize_preview() ) :
									?>
									<?php if( get_theme_mod('lawn_gardner_site_tagline_text',false)){ ?>
										<p class="site-description"><?php echo $lawn_gardner_description; ?></p>
									<?php } ?>
								<?php endif; ?>
							</div>
						</div>
						<div class="phone-box flex-row">
							<?php if ( get_theme_mod('lawn_gardner_phone_number_option','+00-123-4356-7890') ) : ?><div class="phone-icon"><i class="<?php echo esc_attr(get_theme_mod('lawn_gardner_phone_number_option_icon','fas fa-phone-volume')); ?>"></i></div><div class="phone-content"><h6><?php echo esc_html(get_theme_mod('lawn_gardner_phone_number_text', 'PHONE')); ?></h6><p><?php echo esc_html(get_theme_mod('lawn_gardner_phone_number_option', '+00-123-4356-7890')); ?></p></div><?php endif; ?>
						</div>
						<div class="social-box">
							<?php 
								$lawn_gardner_footer_social = absint(get_theme_mod('lawn_gardner_lawn_gardner_header_social_menu', 1));
								if($lawn_gardner_footer_social == 1){ 
								?>
								<div class="social-links">
									<?php
										lawn_gardner_social_menu();
									?>
								</div>
								<?php 
							} 
							?>
						</div>
						<div class="main-header-box">
							<?php if ( get_theme_mod('lawn_gardner_header_button_link' ) ||  get_theme_mod('lawn_gardner_header_button_text','BOOK AN APPOINTMENT' )) : ?><a class="header-button" href="<?php echo esc_url( get_theme_mod('lawn_gardner_header_button_link' ) ); ?>"><i class="fas fa-calendar-alt"></i><?php echo esc_html( get_theme_mod('lawn_gardner_header_button_text','BOOK AN APPOINTMENT' ) ); ?></a><?php endif; ?>
						</div>
					</div>
					<hr>
					<div class="flex-box">
						<div class="nav-box">
							<div class="section-nav main-header-box">
								<nav id="site-navigation" class="main-navigation">
									<button class="menu-toggle" aria-controls="primary-menu" aria-expanded="false"><i class="fas fa-bars"></i></button>
									<?php
										wp_nav_menu(
											array(
												'theme_location' => 'menu-1',
												'menu_id'        => 'primary-menu',
											)
										);
									?>
								</nav>
							</div>
						</div>
						<div class="">
							<?php if( get_theme_mod( 'lawn_gardner_header_search',true) == 1) { ?>
						        <div class="search-box">
				                  <span><a href="#"><i class="fas fa-search"></i></a></span>
				                </div>
					        <?php }?>
						</div>
					</div>
			    </div>
			</div>
		</div>
		<div class="serach_outer">
          <div class="closepop"><a href="#maincontent"><i class="fa fa-window-close"></i></a></div>
          <div class="serach_inner">
            <?php get_search_form(); ?>
          </div>
        </div>
	</header>