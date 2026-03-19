<?php
/**
 * Custom template tags for this theme
 *
 * @package Lawn Gardner
 */

if ( ! function_exists( 'lawn_gardner_posted_on' ) ) :
	function lawn_gardner_posted_on() {
		$lawn_gardner_time_string = '<time class="entry-date published updated" datetime="%1$s">%2$s</time>';
		
		if ( get_the_time( 'U' ) !== get_the_modified_time( 'U' ) ) {
			$lawn_gardner_time_string = '<time class="entry-date published" datetime="%1$s">%2$s</time><time class="updated" datetime="%3$s">%4$s</time>';
		}

		$lawn_gardner_time_string = sprintf(
			$lawn_gardner_time_string,
			esc_attr( get_the_date( DATE_W3C ) ),
			esc_html( get_the_date() ),
			esc_attr( get_the_modified_date( DATE_W3C ) ),
			esc_html( get_the_modified_date() )
		);

		$lawn_gardner_posted_on = sprintf(
			/* translators: %s: post date. */
			wp_kses_post( __( '<strong>Posted on:</strong> %s', 'lawn-gardner' ) ),
			'<a href="' . esc_url( get_permalink() ) . '" rel="bookmark">' . $lawn_gardner_time_string . '</a>'
		);

		echo '<span class="posted-on">' . $lawn_gardner_posted_on . '</span>';
	}
endif;

if ( ! function_exists( 'lawn_gardner_posted_by' ) ) :	
	function lawn_gardner_posted_by() {
		$byline = sprintf(
			/* translators: %s: post author. */
			esc_html_x( '- %s', 'post author', 'lawn-gardner' ),
			'<span class="author vcard"><a class="url fn n" href="' . esc_url( get_author_posts_url( get_the_author_meta( 'ID' ) ) ) . '">' . esc_html( get_the_author() ) . '</a></span>'
		);

		echo '<span class="byline"> ' . $byline . '</span>'; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped

	}
endif;

if ( ! function_exists( 'lawn_gardner_entry_footer' ) ) :	
	function lawn_gardner_entry_footer() {
		// Hide category and tag text for pages.
		if ( 'post' === get_post_type() ) {
			/* translators: used between list items, there is a space after the comma */
			$lawn_gardner_categories_list = get_the_category_list( esc_html__( ', ', 'lawn-gardner' ) );
			if ( $lawn_gardner_categories_list ) {
				/* translators: 1: list of categories. */
				printf( '<span class="cat-links">' . esc_html__( 'Posted in %1$s', 'lawn-gardner' ) . '</span>', $lawn_gardner_categories_list ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
			}

			/* translators: used between list items, there is a space after the comma */
			$lawn_gardner_tags_list = get_the_tag_list( '', esc_html_x( ', ', 'list item separator', 'lawn-gardner' ) );
			if ( $lawn_gardner_tags_list ) {
				/* translators: 1: list of tags. */
				printf( '<span class="tags-links">' . esc_html__( 'Tagged %1$s', 'lawn-gardner' ) . '</span>', $lawn_gardner_tags_list ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
			}
		}

		if ( ! is_single() && ! post_password_required() && ( comments_open() || get_comments_number() ) ) {
			echo '<span class="comments-link">';
			comments_popup_link(
				sprintf(
					wp_kses(
						/* translators: %s: post title */
						__( 'Leave a Comment<span class="screen-reader-text"> on %s</span>', 'lawn-gardner' ),
						array(
							'span' => array(
								'class' => array(),
							),
						)
					),
					wp_kses_post( get_the_title() )
				)
			);
			echo '</span>';
		}

		edit_post_link(
			sprintf(
				wp_kses(
					/* translators: %s: Name of current post. Only visible to screen readers */
					__( 'Edit <span class="screen-reader-text">%s</span>', 'lawn-gardner' ),
					array(
						'span' => array(
							'class' => array(),
						),
					)
				),
				wp_kses_post( get_the_title() )
			),
			'<span class="edit-link">',
			'</span>'
		);
	}
endif;

if ( ! function_exists( 'lawn_gardner_post_thumbnail' ) ) :
	function lawn_gardner_post_thumbnail() {
		if ( post_password_required() || is_attachment() || ! has_post_thumbnail() ) {
			return;
		}

		if ( is_singular() ) :
			?>

			<div class="post-thumbnail">
				<?php the_post_thumbnail(); ?>
			</div><!-- .post-thumbnail -->

		<?php else : ?>

			<a class="post-thumbnail" href="<?php the_permalink(); ?>" aria-hidden="true" tabindex="-1">
				<?php
					the_post_thumbnail(
						'post-thumbnail',
						array(
							'alt' => the_title_attribute(
								array(
									'echo' => false,
								)
							),
						)
					);
				?>
			</a>

			<?php
		endif; // End is_singular().
	}
endif;

if ( ! function_exists( 'wp_body_open' ) ) :
	function wp_body_open() {
		do_action( 'wp_body_open' );
	}
endif;

if( !function_exists('lawn_gardner_breadcrumbs') ) :
    /**
     * Lawn Gardner Breadcrumbs Function
     */
    function lawn_gardner_breadcrumbs($lawn_gardner_comment = null){

        echo '<div class="lawn-gardner-breadcrumbs">';
        	lawn_gardner_breadcrumbs_trail();
        echo '</div>';

    }
endif;