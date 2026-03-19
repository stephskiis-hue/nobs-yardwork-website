<?php
/**
 * The sidebar containing the main widget area
 *
 * @package Lawn Gardner
 */

?>

<?php

if ( is_active_sidebar( 'sidebar-1' )) { ?>
	<aside id="secondary" class="widget-area sidebar-width">
		<?php dynamic_sidebar( 'sidebar-1' ); ?>
	</aside>
<?php } else { ?>
	<aside id="secondary" class="widget-area sidebar-width">
		<div class="default-sidebar">
			<aside id="search-3" class="widget widget_search">
	            <h2 class="widget-title"><?php esc_html_e('Search Anything', 'lawn-gardner'); ?></h2>
	            <?php get_search_form(); ?>
	        </aside>
			<aside id="recent-posts-2" class="widget widget_recent_entries">
				<h2 class="widget-title"><?php esc_html_e('Latest Posts', 'lawn-gardner'); ?></h2>
				<ul>
					<?php
					$lawn_gardner_recent_posts = wp_get_recent_posts(array('numberposts' => 10));
					foreach ($lawn_gardner_recent_posts as $lawn_gardner_post) {
						echo '<li><a href="' . esc_url(get_permalink($lawn_gardner_post['ID'])) . '">' . esc_html($lawn_gardner_post['post_title']) . '</a></li>';
					}
					?>
				</ul>
			</aside>
			<aside id="recent-comments-2" class="widget widget_recent_comments">
				<h2 class="widget-title"><?php esc_html_e('Latest Comments', 'lawn-gardner'); ?></h2>
				<ul id="recentcomments">
					<?php
						$lawn_gardner_comments = get_comments(array(
							'number' => 10,
							'status' => 'approve',
						));
						foreach ($lawn_gardner_comments as $lawn_gardner_comment) {
							echo '<li class="recentcomments">' . esc_html($lawn_gardner_comment->comment_author) . ': <a href="' . esc_url(get_comment_link($lawn_gardner_comment->comment_ID)) . '">' . esc_html(get_the_title($lawn_gardner_comment->comment_post_ID)) . '</a></li>';
						}
					?>
				</ul>
			</aside>
	        <aside id="categories-2" class="widget widget_categories">
	            <h2 class="widget-title"><?php esc_html_e('Explore Categories', 'lawn-gardner'); ?></h2>
	            <ul>
	                <?php
						wp_list_categories(array(
							'title_li' => '',
							'number' => 10
						));
	                ?>
	            </ul>
	        </aside>
	        <aside id="archives-2" class="widget widget_archive">
	            <h2 class="widget-title"><?php esc_html_e('Blog Archives', 'lawn-gardner'); ?></h2>
	            <ul>
					<?php
						wp_get_archives(array(
							'type' => 'postbypost',
							'format' => 'html',
							'limit'  => 10	
						));
					?>
	        	</ul>
	       </aside>
	        <aside id="pages-2" class="widget widget_pages">
	            <h2 class="widget-title"><?php esc_html_e('Explore Our Pages', 'lawn-gardner'); ?></h2>
	            <ul>
	                <?php
						wp_list_pages(array(
							'title_li' => '',
							'number' => 10
						));
	                ?>
	            </ul>
	        </aside>
		   <aside id="calendar-2" class="widget widget_calendar">
	            <h2 class="widget-title"><?php esc_html_e('Calender', 'lawn-gardner'); ?></h2>
	            <?php get_calendar(); ?>
	       </aside>
	   </div>
	</aside>
<?php } ?>