<?php
/**
 * Template part for displaying posts
 *
 * @package Lawn Gardner
 */

?>

<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
	<div class="card-item card-blog-post">
		<?php
			// Get the post ID
			$post_id = get_the_ID();

			// Check if there are audio embedded in the post content
			$post = get_post($post_id);
			$lawn_gardner_content = do_shortcode(apply_filters('the_content', $post->post_content));
			$lawn_gardner_embeds = get_media_embedded_in_content($lawn_gardner_content);

			// Track displayed audio embeds
			$lawn_gardner_displayed_embeds = [];
			
			// Check if not in a singular view
			if (!is_singular() && !empty($lawn_gardner_embeds)) {
				foreach ($lawn_gardner_embeds as $lawn_gardner_embed) {
					if (strpos($lawn_gardner_embed, 'audio') !== false && !in_array($lawn_gardner_embed, $lawn_gardner_displayed_embeds)) {
						$lawn_gardner_displayed_embeds[] = $lawn_gardner_embed;
						?>
						<div class="custom-embedded-audio">
							<div class="media-container">
								<?php echo $lawn_gardner_embed; ?>
							</div>
						</div>
						<?php
					}
				}
			}
		?>

		<!-- .TITLE & META -->
		<header class="entry-header">
			<?php
			if ( 'post' === get_post_type() ) :

				if (is_singular()) {
					lawn_gardner_breadcrumbs();
				}
				
				if ( is_singular() ) :
					$lawn_gardner_single_enable_title = absint(get_theme_mod('lawn_gardner_enable_single_blog_post_title', 1));
					if ($lawn_gardner_single_enable_title == 1) {
						the_title( '<h1 class="entry-title">', '</h1>' );
					} ?>
				<?php
				else :
					$lawn_gardner_enable_title = absint(get_theme_mod('lawn_gardner_enable_blog_post_title', 1));
					if ($lawn_gardner_enable_title == 1) {
						the_title( '<h3 class="entry-title"><a href="' . esc_url( get_permalink() ) . '" rel="bookmark">', '</a></h3>' );
					}
				endif;

				// Check if is singular
				if ( is_singular() ) : ?>
					<?php
					$lawn_gardner_single_blog_meta = absint(get_theme_mod('lawn_gardner_enable_single_blog_post_meta', 1));
					if($lawn_gardner_single_blog_meta == 1){ ?>
					<div class="entry-meta">
						<?php
						lawn_gardner_posted_on();
						lawn_gardner_posted_by();
						?>
					</div><!-- .entry-meta -->
					<?php } ?>
				<?php else : 
					$lawn_gardner_blog_meta = absint(get_theme_mod('lawn_gardner_enable_blog_post_meta', 1));
					if($lawn_gardner_blog_meta == 1){ ?>
						<div class="entry-meta">
							<?php
							lawn_gardner_posted_on();
							lawn_gardner_posted_by();
							?>
						</div><!-- .entry-meta -->
					<?php }
				endif;

			endif;
			?>
		</header>
		<!-- .TITLE & META -->

		
		<!-- .POST TAG -->
		<?php
		// Check if is singular
		if ( is_singular() ) : ?>
			<?php
			$lawn_gardner_single_post_tags = absint(get_theme_mod('lawn_gardner_enable_single_blog_post_tags', 1));
			if($lawn_gardner_single_post_tags == 1){ ?>
			<?php
				$post_tags = get_the_tags();
				if ( $post_tags ) {
					echo '<div class="post-tags"><strong>' . esc_html__('Post Tags: ', 'lawn-gardner') . '</strong>';
					the_tags('', ', ', '');
					echo '</div>';
				}
			?><!-- .tags -->
			<?php } ?>
		<?php else : 
			$lawn_gardner_post_tags = absint(get_theme_mod('lawn_gardner_enable_blog_post_tags', 1));
			if($lawn_gardner_post_tags == 1){ ?>
				<?php
					$post_tags = get_the_tags();
					if ( $post_tags ) {
						echo '<div class="post-tags"><strong>' . esc_html__('Post Tags: ', 'lawn-gardner') . '</strong>';
						the_tags('', ', ', '');
						echo '</div>';
					}
				?><!-- .tags -->
			<?php }
		endif;
		?>
		<!-- .POST TAG -->

		<!-- .IMAGE -->
		<?php if ( is_singular() ) : ?>
			<?php 
			$lawn_gardner_blog_thumbnail = absint(get_theme_mod('lawn_gardner_enable_single_post_image', 1));
			if ( $lawn_gardner_blog_thumbnail == 1 ) { 
			?>
				<?php if ( has_post_thumbnail() ) { ?>
					<div class="card-media">
						<?php lawn_gardner_post_thumbnail(); ?>
					</div>
				<?php } else {
					// Fallback default image
					$lawn_gardner_default_post_thumbnail = get_template_directory_uri() . '/revolution/assets/images/project1.png';
					echo '<img class="default-post-img" src="' . esc_url( $lawn_gardner_default_post_thumbnail ) . '" alt="' . esc_attr( get_the_title() ) . '">';
				} ?>
			<?php } ?>
		<?php else : ?>
		<?php 
			$lawn_gardner_blog_thumbnail = absint(get_theme_mod('lawn_gardner_enable_blog_post_image', 1));
			if ( $lawn_gardner_blog_thumbnail == 1 ) { 
			?>
				<?php if ( has_post_thumbnail() ) { ?>
					<div class="card-media">
						<?php lawn_gardner_post_thumbnail(); ?>
					</div>
				<?php } else {
					// Fallback default image
					$lawn_gardner_default_post_thumbnail = get_template_directory_uri() . '/revolution/assets/images/project1.png';
					echo '<img class="default-post-img" src="' . esc_url( $lawn_gardner_default_post_thumbnail ) . '" alt="' . esc_attr( get_the_title() ) . '">';
				} ?>
			<?php } ?>
		<?php endif; ?>
		<!-- .IMAGE -->

		<!-- .CONTENT & BUTTON -->
		<div class="entry-content">
			<?php
				if ( is_singular() ) :
					$lawn_gardner_single_enable_excerpt = absint(get_theme_mod('lawn_gardner_enable_single_blog_post_content', 1));
					if ($lawn_gardner_single_enable_excerpt == 1) {
						the_content();
					} ?>
				<?php else :
					// Excerpt functionality for archive pages
					$lawn_gardner_enable_excerpt = absint(get_theme_mod('lawn_gardner_enable_blog_post_content', 1));
					if ($lawn_gardner_enable_excerpt == 1) {
						echo "<p>".wp_trim_words(get_the_excerpt(), get_theme_mod('lawn_gardner_excerpt_limit', 25))."</p>";
					}
					?>
					<?php // Check if 'Continue Reading' button should be displayed
					$lawn_gardner_enable_read_more = absint(get_theme_mod('lawn_gardner_enable_blog_post_button', 1));
					if ($lawn_gardner_enable_read_more == 1) {
						if ( get_theme_mod( 'lawn_gardner_read_more_text', __('Continue Reading....', 'lawn-gardner') ) ) :
							?>
							<a href="<?php the_permalink(); ?>" class="btn read-btn text-uppercase">
								<?php echo esc_html( get_theme_mod( 'lawn_gardner_read_more_text', __('Continue Reading....', 'lawn-gardner') ) ); ?>
							</a>
							<?php
						endif;
					}?>
				<?php endif; ?>
			<?php
			wp_link_pages(
				array(
					'before' => '<div class="page-links">' . esc_html__( 'Pages:', 'lawn-gardner' ),
					'after'  => '</div>',
				)
			);
			?>
		</div>
		<!-- .CONTENT & BUTTON -->
	</div>
</article><!-- #post-<?php the_ID(); ?> -->