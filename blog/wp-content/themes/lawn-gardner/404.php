<?php
/**
 * The template for displaying 404 pages (not found)
 *
 * @package Lawn Gardner
 */

?>
<style>
    /* This stops the floating RSS error visually */
    .widget_rss, .rss-error, .widget_block_rss, .widget_block.widget_rss {
        display: none !important;
    }
</style>
<?php
get_header();
?>

<div class="container">
	<div class="site-wrapper">
		<main id="primary" class="site-main">
			<section class="error-404 not-found">
				<header class="page-header">
					<h1 class="page-title"><?php esc_html_e( 'Oops! That page can&rsquo;t be found.', 'lawn-gardner' ); ?></h1>
				</header>
				<div class="page-content">
					<p><?php esc_html_e( 'It looks like nothing was found at this location. Maybe try one of the links below or a search?', 'lawn-gardner' ); ?></p>
					<?php get_search_form(); ?>
				</div>
			</section>
		</main>
	</div>
</div>

<?php
get_footer();
