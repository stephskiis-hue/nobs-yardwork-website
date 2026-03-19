<?php
/**
 * Breadcrumb Trail - A breadcrumb menu script for WordPress.
 *
 * Breadcrumb Trail is a script for showing a breadcrumb trail for any type of page.  It tries to
 * anticipate any type of structure and display the best possible trail that matches your site's
 * permalink structure.  While not perfect, it attempts to fill in the gaps left by many other
 * breadcrumb scripts.
 *
 * This program is free software; you can redistribute it and/or modify it under the terms of the GNU
 * General Public License as published by the Free Software Foundation; either version 2 of the License,
 * or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
 * even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 *
 * @package   BreadcrumbTrail
 * @version   1.1.0
 * @author    Justin Tadlock <justin@justintadlock.com>
 * @copyright Copyright (c) 2008 - 2017, Justin Tadlock
 * @link      https://themehybrid.com/plugins/breadcrumb-trail
 * @license   http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
 */

/**
 * Shows a breadcrumb for all types of pages.  This is a wrapper function for the Lawn_Gardner_Breadcrumb_Trail class,
 * which should be used in theme templates.
 *
 * @since  0.1.0
 * @access public
 * @param  array $lawn_gardner_args Arguments to pass to Lawn_Gardner_Breadcrumb_Trail.
 * @return void
 */
function lawn_gardner_breadcrumbs_trail( $lawn_gardner_args = array() ) {

    $lawn_gardner_breadcrumb = apply_filters( 'lawn_gardner_breadcrumbs_trail_object', null, $lawn_gardner_args );

    if ( ! is_object( $lawn_gardner_breadcrumb ) )
        $lawn_gardner_breadcrumb = new Lawn_Gardner_Breadcrumb_Trail( $lawn_gardner_args );

    return $lawn_gardner_breadcrumb->trail();
}

/**
 * Creates a breadcrumbs menu for the site based on the current page that's being viewed by the user.
 *
 * @since  0.6.0
 * @access public
 */
class Lawn_Gardner_Breadcrumb_Trail {

    /**
     * Array of items belonging to the current breadcrumb trail.
     *
     * @since  0.1.0
     * @access public
     * @var    array
     */
    public $items = array();

    /**
     * Arguments used to build the breadcrumb trail.
     *
     * @since  0.1.0
     * @access public
     * @var    array
     */
    public $lawn_gardner_args = array();

    /**
     * Array of text labels.
     *
     * @since  1.0.0
     * @access public
     * @var    array
     */
    public $lawn_gardner_labels = array();

    /**
     * Array of post types (key) and taxonomies (value) to use for single post views.
     *
     * @since  1.0.0
     * @access public
     * @var    array
     */
    public $lawn_gardner_post_taxonomy = array();

    public $labels;
    public $post_taxonomy;
	public $args;

    /* ====== Magic Methods ====== */

    /**
     * Magic method to use in case someone tries to output the layout object as a string.
     * We'll just return the trail HTML.
     *
     * @since  1.0.0
     * @access public
     * @return string
     */
    public function __toString() {
        return $this->trail();
    }

    /**
     * Sets up the breadcrumb trail properties.  Calls the `Lawn_Gardner_Breadcrumb_Trail::add_items()` method
     * to creat the array of breadcrumb items.
     *
     * @since  0.6.0
     * @access public
     * @param  array   $lawn_gardner_args  {
     *     @type string    $container      Container HTML element. nav|div
     *     @type string    $before         String to output before breadcrumb menu.
     *     @type string    $after          String to output after breadcrumb menu.
     *     @type string    $browse_tag     The HTML tag to use to wrap the "Browse" header text.
     *     @type string    $list_tag       The HTML tag to use for the list wrapper.
     *     @type string    $lawn_gardner_item_tag       The HTML tag to use for the item wrapper.
     *     @type bool      $show_on_front  Whether to show when `is_front_page()`.
     *     @type bool      $lawn_gardner_network        Whether to link to the network main site (multisite only).
     *     @type bool      $show_title     Whether to show the title (last item) in the trail.
     *     @type bool      $show_browse    Whether to show the breadcrumb menu header.
     *     @type array     $lawn_gardner_labels         Text labels. @see Lawn_Gardner_Breadcrumb_Trail::set_labels()
     *     @type array     $lawn_gardner_post_taxonomy  Taxonomies to use for post types. @see Lawn_Gardner_Breadcrumb_Trail::set_post_taxonomy()
     *     @type bool      $echo           Whether to print or return the breadcrumbs.
     * }
     * @return void
     */
    public function __construct( $lawn_gardner_args = array() ) {

        $lawn_gardner_defaults = array(
            'container'       => 'nav',
            'before'          => '',
            'after'           => '',
            'browse_tag'      => 'h2',
            'list_tag'        => 'ul',
            'item_tag'        => 'li',
            'show_on_front'   => true,
            'network'         => false,
            'show_title'      => true,
            'show_browse'     => false,
            'labels'          => array(),
            'post_taxonomy'   => array(),
            'echo'            => true
        );

        // Parse the arguments with the deaults.
        $this->args = apply_filters( 'lawn_gardner_breadcrumbs_trail_args', wp_parse_args( $lawn_gardner_args, $lawn_gardner_defaults ) );

        // Set the labels and post taxonomy properties.
        $this->set_labels();
        $this->set_post_taxonomy();

        // Let's find some items to add to the trail!
        $this->add_items();
    }

    /* ====== Public Methods ====== */

    /**
     * Formats the HTML output for the breadcrumb trail.
     *
     * @since  0.6.0
     * @access public
     * @return string
     */
    public function trail() {

        // Set up variables that we'll need.
        $lawn_gardner_breadcrumb    = '';
        $lawn_gardner_item_count    = count( $this->items );
        $lawn_gardner_item_position = 0;

        // Connect the breadcrumb trail if there are items in the trail.
        if ( 0 < $lawn_gardner_item_count ) {

            // Add 'browse' label if it should be shown.
            if ( true === $this->args['show_browse'] ) {

                $lawn_gardner_breadcrumb .= sprintf(
                    '<%1$s class="trail-browse">%2$s</%1$s>',
                    tag_escape( $this->args['browse_tag'] ),
                    $this->labels['browse']
                );
            }

            // Open the unordered list.
            $lawn_gardner_breadcrumb .= sprintf(
                '<%s class="trail-items" itemscope itemtype="http://schema.org/BreadcrumbList">',
                tag_escape( $this->args['list_tag'] )
            );

            // Add the number of items and item list order schema.
            $lawn_gardner_breadcrumb .= sprintf( '<meta name="numberOfItems" content="%d" />', absint( $lawn_gardner_item_count ) );
            $lawn_gardner_breadcrumb .= '<meta name="itemListOrder" content="Ascending" />';

            // Loop through the items and add them to the list.
            foreach ( $this->items as $lawn_gardner_item ) {

                // Iterate the item position.
                ++$lawn_gardner_item_position;

                // Check if the item is linked.
                preg_match( '/(<a.*?>)(.*?)(<\/a>)/i', $lawn_gardner_item, $lawn_gardner_matches );

                // Wrap the item text with appropriate itemprop.
                $lawn_gardner_item = ! empty( $lawn_gardner_matches ) ? sprintf( '%s<span itemprop="name">%s</span>%s', $lawn_gardner_matches[1], $lawn_gardner_matches[2], $lawn_gardner_matches[3] ) : sprintf( '<span itemprop="name">%s</span>', $lawn_gardner_item );

                // If viewing a single post.
                if ( is_singular() || is_page() ){

                    global $post;
                    $lawn_gardner_link_item = get_permalink( $post->ID );

                }
                elseif ( is_archive() && ( !is_day() && !is_month() && !is_year() && !is_tag() ) ) {

                    $lawn_gardner_category = get_queried_object();
                    $lawn_gardner_link_item = get_category_link( $lawn_gardner_category->term_id );

                } elseif ( is_day() ) {

                    $lawn_gardner_link_item = get_day_link( get_the_time('Y'),get_the_time('m'),get_the_time('d') );

                } elseif ( is_month() ) {

                   $lawn_gardner_link_item = get_month_link( get_the_time('Y'),get_the_time('m') );

                } elseif ( is_year() ) {

                    $lawn_gardner_link_item = get_year_link( get_the_time('Y') );

                }elseif ( is_tag() ) {

                    $lawn_gardner_tag_id = get_queried_object()->term_id;
                    $lawn_gardner_link_item = get_tag_link( $lawn_gardner_tag_id );

                } elseif ( is_author() ) {

                    $lawn_gardner_link_item = get_author_posts_url( get_current_user_id() );

                }
                elseif ( is_search() ) {

                    $lawn_gardner_link_item = home_url();

                }
                else{

                    $lawn_gardner_link_item = home_url();

                }

                $lawn_gardner_item = ! empty( $lawn_gardner_matches )
                    ? preg_replace( '/(<a.*?)([\'"])>/i', '$1$2 itemprop=$2item$2>', $lawn_gardner_item )
                    : sprintf( '<a href="'.esc_url( $lawn_gardner_link_item ).'" itemprop="item">%s</a>', $lawn_gardner_item );

                // Add list item classes.
                $lawn_gardner_item_class = 'trail-item';

                if ( 1 === $lawn_gardner_item_position && 1 < $lawn_gardner_item_count )
                    $lawn_gardner_item_class .= ' trail-begin';

                elseif ( $lawn_gardner_item_count === $lawn_gardner_item_position )
                    $lawn_gardner_item_class .= ' trail-end';

                // Create list item attributes.
                $attributes = 'itemprop="itemListElement" itemscope itemtype="http://schema.org/ListItem" class="' . $lawn_gardner_item_class . '"';

                // Build the meta position HTML.
                $meta = sprintf( '<meta itemprop="position" content="%s" />', absint( $lawn_gardner_item_position ) );

                // Build the list item.
                $lawn_gardner_breadcrumb .= sprintf( '<%1$s %2$s>%3$s%4$s</%1$s>', tag_escape( $this->args['item_tag'] ),$attributes, $lawn_gardner_item, $meta );
            }

            // Close the unordered list.
            $lawn_gardner_breadcrumb .= sprintf( '</%s>', tag_escape( $this->args['list_tag'] ) );

            // Wrap the breadcrumb trail.
            $lawn_gardner_breadcrumb = sprintf(
                '<%1$s role="navigation" aria-label="%2$s" class="breadcrumb-trail" itemprop="breadcrumb">%3$s%4$s%5$s</%1$s>',
                tag_escape( $this->args['container'] ),
                esc_attr( $this->labels['aria_label'] ),
                $this->args['before'],
                $lawn_gardner_breadcrumb,
                $this->args['after']
            );
        }

        // Allow developers to filter the breadcrumb trail HTML.
        $lawn_gardner_breadcrumb = apply_filters( 'lawn_gardner_breadcrumbs_trail', $lawn_gardner_breadcrumb, $this->args );

        if ( false === $this->args['echo'] )
            return $lawn_gardner_breadcrumb;

        echo $lawn_gardner_breadcrumb;
    }

    /* ====== Protected Methods ====== */

    /**
     * Sets the labels property.  Parses the inputted labels array with the defaults.
     *
     * @since  1.0.0
     * @access protected
     * @return void
     */
    protected function set_labels() {

        $lawn_gardner_defaults = array(
            'browse'              => esc_html__( 'Browse:',                               'lawn-gardner' ),
            'aria_label'          => esc_attr_x( 'Breadcrumbs', 'breadcrumbs aria label', 'lawn-gardner' ),
            'home'                => esc_html__( 'Home',                                  'lawn-gardner' ),
            'error_404'           => esc_html__( '404 Not Found',                         'lawn-gardner' ),
            'archives'            => esc_html__( 'Archives',                              'lawn-gardner' ),
            // Translators: %s is the search query.
            'search'              => esc_html__( 'Search results for: %s',                'lawn-gardner' ),
            // Translators: %s is the page number.
            'paged'               => esc_html__( 'Page %s',                               'lawn-gardner' ),
            // Translators: %s is the page number.
            'paged_comments'      => esc_html__( 'Comment Page %s',                       'lawn-gardner' ),
            // Translators: Minute archive title. %s is the minute time format.
            'archive_minute'      => esc_html__( 'Minute %s',                             'lawn-gardner' ),
            // Translators: Weekly archive title. %s is the week date format.
            'archive_week'        => esc_html__( 'Week %s',                               'lawn-gardner' ),

            // "%s" is replaced with the translated date/time format.
            'archive_minute_hour' => '%s',
            'archive_hour'        => '%s',
            'archive_day'         => '%s',
            'archive_month'       => '%s',
            'archive_year'        => '%s',
        );

        $this->labels = apply_filters( 'lawn_gardner_breadcrumbs_trail_labels', wp_parse_args( $this->args['labels'], $lawn_gardner_defaults ) );
    }

    /**
     * Sets the `$lawn_gardner_post_taxonomy` property.  This is an array of post types (key) and taxonomies (value).
     * The taxonomy's terms are shown on the singular post view if set.
     *
     * @since  1.0.0
     * @access protected
     * @return void
     */
    protected function set_post_taxonomy() {

        $lawn_gardner_defaults = array();

        // If post permalink is set to `%postname%`, use the `category` taxonomy.
        if ( '%postname%' === trim( get_option( 'permalink_structure' ), '/' ) )
            $lawn_gardner_defaults['post'] = 'category';

        $this->post_taxonomy = apply_filters( 'lawn_gardner_breadcrumbs_trail_post_taxonomy', wp_parse_args( $this->args['post_taxonomy'], $lawn_gardner_defaults ) );
    }

    /**
     * Runs through the various WordPress conditional tags to check the current page being viewed.  Once
     * a condition is met, a specific method is launched to add items to the `$items` array.
     *
     * @since  1.0.0
     * @access protected
     * @return void
     */
    protected function add_items() {

        // If viewing the front page.
        if ( is_front_page() ) {
            $this->add_front_page_items();
        }

        // If not viewing the front page.
        else {

            // Add the network and site home links.
            $this->add_network_home_link();
            $this->add_site_home_link();

            // If viewing the home/blog page.
            if ( is_home() ) {
                $this->add_blog_items();
            }

            // If viewing a single post.
            elseif ( is_singular() ) {
                $this->add_singular_items();
            }

            // If viewing an archive page.
            elseif ( is_archive() ) {

                if ( is_post_type_archive() )
                    $this->add_post_type_archive_items();

                elseif ( is_category() || is_tag() || is_tax() )
                    $this->add_term_archive_items();

                elseif ( is_author() )
                    $this->add_user_archive_items();

                elseif ( get_query_var( 'minute' ) && get_query_var( 'hour' ) )
                    $this->add_minute_hour_archive_items();

                elseif ( get_query_var( 'minute' ) )
                    $this->add_minute_archive_items();

                elseif ( get_query_var( 'hour' ) )
                    $this->add_hour_archive_items();

                elseif ( is_day() )
                    $this->add_day_archive_items();

                elseif ( get_query_var( 'w' ) )
                    $this->add_week_archive_items();

                elseif ( is_month() )
                    $this->add_month_archive_items();

                elseif ( is_year() )
                    $this->add_year_archive_items();

                else
                    $this->add_default_archive_items();
            }

            // If viewing a search results page.
            elseif ( is_search() ) {
                $this->add_search_items();
            }

            // If viewing the 404 page.
            elseif ( is_404() ) {
                $this->add_404_items();
            }
        }

        // Add paged items if they exist.
        $this->add_paged_items();

        // Allow developers to overwrite the items for the breadcrumb trail.
        $this->items = array_unique( apply_filters( 'lawn_gardner_breadcrumbs_trail_items', $this->items, $this->args ) );
    }

    /**
     * Gets front items based on $wp_rewrite->front.
     *
     * @since  1.0.0
     * @access protected
     * @return void
     */
    protected function add_rewrite_front_items() {
        global $wp_rewrite;

        if ( $wp_rewrite->front )
            $this->add_path_parents( $wp_rewrite->front );
    }

    /**
     * Adds the page/paged number to the items array.
     *
     * @since  1.0.0
     * @access protected
     * @return void
     */
    protected function add_paged_items() {

        // If viewing a paged singular post.
        if ( is_singular() && 1 < get_query_var( 'page' ) && true === $this->args['show_title'] )
            $this->items[] = sprintf( $this->labels['paged'], number_format_i18n( absint( get_query_var( 'page' ) ) ) );

        // If viewing a singular post with paged comments.
        elseif ( is_singular() && get_option( 'page_comments' ) && 1 < get_query_var( 'cpage' ) )
            $this->items[] = sprintf( $this->labels['paged_comments'], number_format_i18n( absint( get_query_var( 'cpage' ) ) ) );

        // If viewing a paged archive-type page.
        elseif ( is_paged() && true === $this->args['show_title'] )
            $this->items[] = sprintf( $this->labels['paged'], number_format_i18n( absint( get_query_var( 'paged' ) ) ) );
    }

    /**
     * Adds the network (all sites) home page link to the items array.
     *
     * @since  1.0.0
     * @access protected
     * @return void
     */
    protected function add_network_home_link() {

        if ( is_multisite() && ! is_main_site() && true === $this->args['network'] )
            $this->items[] = sprintf( '<a href="%s" rel="home">%s</a>', esc_url( network_home_url() ), $this->labels['home'] );
    }

    /**
     * Adds the current site's home page link to the items array.
     *
     * @since  1.0.0
     * @access protected
     * @return void
     */
    protected function add_site_home_link() {

        $lawn_gardner_network = is_multisite() && ! is_main_site() && true === $this->args['network'];
        $lawn_gardner_label   = $lawn_gardner_network ? get_bloginfo( 'name' ) : $this->labels['home'];
        $rel     = $lawn_gardner_network ? '' : ' rel="home"';

        $this->items[] = sprintf( '<a href="%s"%s>%s</a>', esc_url( user_trailingslashit( home_url() ) ), $rel, $lawn_gardner_label );
    }

    /**
     * Adds items for the front page to the items array.
     *
     * @since  1.0.0
     * @access protected
     * @return void
     */
    protected function add_front_page_items() {

        // Only show front items if the 'show_on_front' argument is set to 'true'.
        if ( true === $this->args['show_on_front'] || is_paged() || ( is_singular() && 1 < get_query_var( 'page' ) ) ) {

            // Add network home link.
            $this->add_network_home_link();

            // If on a paged view, add the site home link.
            if ( is_paged() )
                $this->add_site_home_link();

            // If on the main front page, add the network home title.
            elseif ( true === $this->args['show_title'] )
                $this->items[] = is_multisite() && true === $this->args['network'] ? get_bloginfo( 'name' ) : $this->labels['home'];
        }
    }

    /**
     * Adds items for the posts page (i.e., is_home()) to the items array.
     *
     * @since  1.0.0
     * @access protected
     * @return void
     */
    protected function add_blog_items() {

        // Get the post ID and post.
        $lawn_gardner_post_id = get_queried_object_id();
        $post    = get_post( $lawn_gardner_post_id );

        // If the post has parents, add them to the trail.
        if ( 0 < $post->post_parent )
            $this->add_post_parents( $post->post_parent );

        // Get the page title.
        $lawn_gardner_title = get_the_title( $lawn_gardner_post_id );

        // Add the posts page item.
        if ( is_paged() )
            $this->items[] = sprintf( '<a href="%s">%s</a>', esc_url( get_permalink( $lawn_gardner_post_id ) ), $lawn_gardner_title );

        elseif ( $lawn_gardner_title && true === $this->args['show_title'] )
            $this->items[] = $lawn_gardner_title;
    }

    /**
     * Adds singular post items to the items array.
     *
     * @since  1.0.0
     * @access protected
     * @return void
     */
    protected function add_singular_items() {

        // Get the queried post.
        $post    = get_queried_object();
        $lawn_gardner_post_id = get_queried_object_id();

        // If the post has a parent, follow the parent trail.
        if ( 0 < $post->post_parent )
            $this->add_post_parents( $post->post_parent );

        // If the post doesn't have a parent, get its hierarchy based off the post type.
        else
            $this->add_post_hierarchy( $lawn_gardner_post_id );

        // Display terms for specific post type taxonomy if requested.
        if ( ! empty( $this->post_taxonomy[ $post->post_type ] ) )
            $this->add_post_terms( $lawn_gardner_post_id, $this->post_taxonomy[ $post->post_type ] );

        // End with the post title.
        if ( $lawn_gardner_post_title = single_post_title( '', false ) ) {

            if ( ( 1 < get_query_var( 'page' ) || is_paged() ) || ( get_option( 'page_comments' ) && 1 < absint( get_query_var( 'cpage' ) ) ) )
                $this->items[] = sprintf( '<a href="%s">%s</a>', esc_url( get_permalink( $lawn_gardner_post_id ) ), $lawn_gardner_post_title );

            elseif ( true === $this->args['show_title'] )
                $this->items[] = $lawn_gardner_post_title;
        }
    }

    /**
     * Adds the items to the trail items array for taxonomy term archives.
     *
     * @since  1.0.0
     * @access protected
     * @global object $wp_rewrite
     * @return void
     */
    protected function add_term_archive_items() {
        global $wp_rewrite;

        // Get some taxonomy and term variables.
        $lawn_gardner_term           = get_queried_object();
        $lawn_gardner_taxonomy       = get_taxonomy( $lawn_gardner_term->taxonomy );
        $lawn_gardner_done_post_type = false;

        // If there are rewrite rules for the taxonomy.
        if ( false !== $lawn_gardner_taxonomy->rewrite ) {

            // If 'with_front' is true, dd $wp_rewrite->front to the trail.
            if ( isset( $lawn_gardner_taxonomy->rewrite['with_front'] ) && $lawn_gardner_taxonomy->rewrite['with_front'] && isset( $wp_rewrite->front ) && $wp_rewrite->front )
                $this->add_rewrite_front_items();

            // Get parent pages by path if they exist.
            $this->add_path_parents( $lawn_gardner_taxonomy->rewrite['slug'] );

            // Add post type archive if its 'has_archive' matches the taxonomy rewrite 'slug'.
            if ( $lawn_gardner_taxonomy->rewrite['slug'] ) {

                $lawn_gardner_slug = trim( $lawn_gardner_taxonomy->rewrite['slug'], '/' );

                // Deals with the situation if the slug has a '/' between multiple
                // strings. For example, "movies/genres" where "movies" is the post
                // type archive.
                $lawn_gardner_matches = explode( '/', $lawn_gardner_slug );

                // If matches are found for the path.
                if ( isset( $lawn_gardner_matches ) ) {

                    // Reverse the array of matches to search for posts in the proper order.
                    $lawn_gardner_matches = array_reverse( $lawn_gardner_matches );

                    // Loop through each of the path matches.
                    foreach ( $lawn_gardner_matches as $lawn_gardner_match ) {

                        // If a match is found.
                        $lawn_gardner_slug = $lawn_gardner_match;

                        // Get public post types that match the rewrite slug.
                        $lawn_gardner_post_types = $this->get_post_types_by_slug( $lawn_gardner_match );

                        if ( ! empty( $lawn_gardner_post_types ) ) {

                            $lawn_gardner_post_type_object = $lawn_gardner_post_types[0];

                            // Add support for a non-standard label of 'archive_title' (special use case).
                            $lawn_gardner_label = ! empty( $lawn_gardner_post_type_object->labels->archive_title ) ? $lawn_gardner_post_type_object->labels->archive_title : $lawn_gardner_post_type_object->labels->name;

                            // Core filter hook.
                            $lawn_gardner_label = apply_filters( 'post_type_archive_title', $lawn_gardner_label, $lawn_gardner_post_type_object->name );

                            // Add the post type archive link to the trail.
                            $this->items[] = sprintf( '<a href="%s">%s</a>', esc_url( get_post_type_archive_link( $lawn_gardner_post_type_object->name ) ), $lawn_gardner_label );

                            $lawn_gardner_done_post_type = true;

                            // Break out of the loop.
                            break;
                        }
                    }
                }
            }
        }

        // If there's a single post type for the taxonomy, use it.
        if ( false === $lawn_gardner_done_post_type && 1 === count( $lawn_gardner_taxonomy->object_type ) && post_type_exists( $lawn_gardner_taxonomy->object_type[0] ) ) {

            // If the post type is 'post'.
            if ( 'post' === $lawn_gardner_taxonomy->object_type[0] ) {
                $lawn_gardner_post_id = get_option( 'page_for_posts' );

                if ( 'posts' !== get_option( 'show_on_front' ) && 0 < $lawn_gardner_post_id )
                    $this->items[] = sprintf( '<a href="%s">%s</a>', esc_url( get_permalink( $lawn_gardner_post_id ) ), get_the_title( $lawn_gardner_post_id ) );

            // If the post type is not 'post'.
            } else {
                $lawn_gardner_post_type_object = get_post_type_object( $lawn_gardner_taxonomy->object_type[0] );

                $lawn_gardner_label = ! empty( $lawn_gardner_post_type_object->labels->archive_title ) ? $lawn_gardner_post_type_object->labels->archive_title : $lawn_gardner_post_type_object->labels->name;

                // Core filter hook.
                $lawn_gardner_label = apply_filters( 'post_type_archive_title', $lawn_gardner_label, $lawn_gardner_post_type_object->name );

                $this->items[] = sprintf( '<a href="%s">%s</a>', esc_url( get_post_type_archive_link( $lawn_gardner_post_type_object->name ) ), $lawn_gardner_label );
            }
        }

        // If the taxonomy is hierarchical, list its parent terms.
        if ( is_taxonomy_hierarchical( $lawn_gardner_term->taxonomy ) && $lawn_gardner_term->parent )
            $this->add_term_parents( $lawn_gardner_term->parent, $lawn_gardner_term->taxonomy );

        // Add the term name to the trail end.
        if ( is_paged() )
            $this->items[] = sprintf( '<a href="%s">%s</a>', esc_url( get_term_link( $lawn_gardner_term, $lawn_gardner_term->taxonomy ) ), single_term_title( '', false ) );

        elseif ( true === $this->args['show_title'] )
            $this->items[] = single_term_title( '', false );
    }

    /**
     * Adds the items to the trail items array for post type archives.
     *
     * @since  1.0.0
     * @access protected
     * @return void
     */
    protected function add_post_type_archive_items() {

        // Get the post type object.
        $lawn_gardner_post_type_object = get_post_type_object( get_query_var( 'post_type' ) );

        if ( false !== $lawn_gardner_post_type_object->rewrite ) {

            // If 'with_front' is true, add $wp_rewrite->front to the trail.
            if ( isset( $lawn_gardner_post_type_object->rewrite['with_front'] ) && $lawn_gardner_post_type_object->rewrite['with_front'] )
                $this->add_rewrite_front_items();

            // If there's a rewrite slug, check for parents.
            if ( ! empty( $lawn_gardner_post_type_object->rewrite['slug'] ) )
                $this->add_path_parents( $lawn_gardner_post_type_object->rewrite['slug'] );
        }

        // Add the post type [plural] name to the trail end.
        if ( is_paged() || is_author() )
            $this->items[] = sprintf( '<a href="%s">%s</a>', esc_url( get_post_type_archive_link( $lawn_gardner_post_type_object->name ) ), post_type_archive_title( '', false ) );

        elseif ( true === $this->args['show_title'] )
            $this->items[] = post_type_archive_title( '', false );

        // If viewing a post type archive by author.
        if ( is_author() )
            $this->add_user_archive_items();
    }

    /**
     * Adds the items to the trail items array for user (author) archives.
     *
     * @since  1.0.0
     * @access protected
     * @global object $wp_rewrite
     * @return void
     */
    protected function add_user_archive_items() {
        global $wp_rewrite;

        // Add $wp_rewrite->front to the trail.
        $this->add_rewrite_front_items();

        // Get the user ID.
        $user_id = get_query_var( 'author' );

        // If $author_base exists, check for parent pages.
        if ( ! empty( $wp_rewrite->author_base ) && ! is_post_type_archive() )
            $this->add_path_parents( $wp_rewrite->author_base );

        // Add the author's display name to the trail end.
        if ( is_paged() )
            $this->items[] = sprintf( '<a href="%s">%s</a>', esc_url( get_author_posts_url( $user_id ) ), get_the_author_meta( 'display_name', $user_id ) );

        elseif ( true === $this->args['show_title'] )
            $this->items[] = get_the_author_meta( 'display_name', $user_id );
    }

    /**
     * Adds the items to the trail items array for minute + hour archives.
     *
     * @since  1.0.0
     * @access protected
     * @return void
     */
    protected function add_minute_hour_archive_items() {

        // Add $wp_rewrite->front to the trail.
        $this->add_rewrite_front_items();

        // Add the minute + hour item.
        if ( true === $this->args['show_title'] )
            $this->items[] = sprintf( $this->labels['archive_minute_hour'], get_the_time( esc_html_x( 'g:i a', 'minute and hour archives time format', 'lawn-gardner' ) ) );
    }

    /**
     * Adds the items to the trail items array for minute archives.
     *
     * @since  1.0.0
     * @access protected
     * @return void
     */
    protected function add_minute_archive_items() {

        // Add $wp_rewrite->front to the trail.
        $this->add_rewrite_front_items();

        // Add the minute item.
        if ( true === $this->args['show_title'] )
            $this->items[] = sprintf( $this->labels['archive_minute'], get_the_time( esc_html_x( 'i', 'minute archives time format', 'lawn-gardner' ) ) );
    }

    /**
     * Adds the items to the trail items array for hour archives.
     *
     * @since  1.0.0
     * @access protected
     * @return void
     */
    protected function add_hour_archive_items() {

        // Add $wp_rewrite->front to the trail.
        $this->add_rewrite_front_items();

        // Add the hour item.
        if ( true === $this->args['show_title'] )
            $this->items[] = sprintf( $this->labels['archive_hour'], get_the_time( esc_html_x( 'g a', 'hour archives time format', 'lawn-gardner' ) ) );
    }

    /**
     * Adds the items to the trail items array for day archives.
     *
     * @since  1.0.0
     * @access protected
     * @return void
     */
    protected function add_day_archive_items() {

        // Add $wp_rewrite->front to the trail.
        $this->add_rewrite_front_items();

        // Get year, month, and day.
        $lawn_gardner_year  = sprintf( $this->labels['archive_year'],  get_the_time( esc_html_x( 'Y', 'yearly archives date format',  'lawn-gardner' ) ) );
        $lawn_gardner_month = sprintf( $this->labels['archive_month'], get_the_time( esc_html_x( 'F', 'monthly archives date format', 'lawn-gardner' ) ) );
        $lawn_gardner_day   = sprintf( $this->labels['archive_day'],   get_the_time( esc_html_x( 'j', 'daily archives date format',   'lawn-gardner' ) ) );

        // Add the year and month items.
        $this->items[] = sprintf( '<a href="%s">%s</a>', esc_url( get_year_link( get_the_time( 'Y' ) ) ), $lawn_gardner_year );
        $this->items[] = sprintf( '<a href="%s">%s</a>', esc_url( get_month_link( get_the_time( 'Y' ), get_the_time( 'm' ) ) ), $lawn_gardner_month );

        // Add the day item.
        if ( is_paged() )
            $this->items[] = sprintf( '<a href="%s">%s</a>', esc_url( get_day_link( get_the_time( 'Y' ) ), get_the_time( 'm' ), get_the_time( 'd' ) ), $lawn_gardner_day );

        elseif ( true === $this->args['show_title'] )
            $this->items[] = $lawn_gardner_day;
    }

    /**
     * Adds the items to the trail items array for week archives.
     *
     * @since  1.0.0
     * @access protected
     * @return void
     */
    protected function add_week_archive_items() {

        // Add $wp_rewrite->front to the trail.
        $this->add_rewrite_front_items();

        // Get the year and week.
        $lawn_gardner_year = sprintf( $this->labels['archive_year'],  get_the_time( esc_html_x( 'Y', 'yearly archives date format', 'lawn-gardner' ) ) );
        $lawn_gardner_week = sprintf( $this->labels['archive_week'],  get_the_time( esc_html_x( 'W', 'weekly archives date format', 'lawn-gardner' ) ) );

        // Add the year item.
        $this->items[] = sprintf( '<a href="%s">%s</a>', esc_url( get_year_link( get_the_time( 'Y' ) ) ), $lawn_gardner_year );

        // Add the week item.
        if ( is_paged() )
            $this->items[] = esc_url( get_archives_link( add_query_arg( array( 'm' => get_the_time( 'Y' ), 'w' => get_the_time( 'W' ) ), home_url() ), $lawn_gardner_week, false ) );

        elseif ( true === $this->args['show_title'] )
            $this->items[] = $lawn_gardner_week;
    }

    /**
     * Adds the items to the trail items array for month archives.
     *
     * @since  1.0.0
     * @access protected
     * @return void
     */
    protected function add_month_archive_items() {

        // Add $wp_rewrite->front to the trail.
        $this->add_rewrite_front_items();

        // Get the year and month.
        $lawn_gardner_year  = sprintf( $this->labels['archive_year'],  get_the_time( esc_html_x( 'Y', 'yearly archives date format',  'lawn-gardner' ) ) );
        $lawn_gardner_month = sprintf( $this->labels['archive_month'], get_the_time( esc_html_x( 'F', 'monthly archives date format', 'lawn-gardner' ) ) );

        // Add the year item.
        $this->items[] = sprintf( '<a href="%s">%s</a>', esc_url( get_year_link( get_the_time( 'Y' ) ) ), $lawn_gardner_year );

        // Add the month item.
        if ( is_paged() )
            $this->items[] = sprintf( '<a href="%s">%s</a>', esc_url( get_month_link( get_the_time( 'Y' ), get_the_time( 'm' ) ) ), $lawn_gardner_month );

        elseif ( true === $this->args['show_title'] )
            $this->items[] = $lawn_gardner_month;
    }

    /**
     * Adds the items to the trail items array for year archives.
     *
     * @since  1.0.0
     * @access protected
     * @return void
     */
    protected function add_year_archive_items() {

        // Add $wp_rewrite->front to the trail.
        $this->add_rewrite_front_items();

        // Get the year.
        $lawn_gardner_year  = sprintf( $this->labels['archive_year'],  get_the_time( esc_html_x( 'Y', 'yearly archives date format',  'lawn-gardner' ) ) );

        // Add the year item.
        if ( is_paged() )
            $this->items[] = sprintf( '<a href="%s">%s</a>', esc_url( get_year_link( get_the_time( 'Y' ) ) ), $lawn_gardner_year );

        elseif ( true === $this->args['show_title'] )
            $this->items[] = $lawn_gardner_year;
    }

    /**
     * Adds the items to the trail items array for archives that don't have a more specific method
     * defined in this class.
     *
     * @since  1.0.0
     * @access protected
     * @return void
     */
    protected function add_default_archive_items() {

        // If this is a date-/time-based archive, add $wp_rewrite->front to the trail.
        if ( is_date() || is_time() )
            $this->add_rewrite_front_items();

        if ( true === $this->args['show_title'] )
            $this->items[] = $this->labels['archives'];
    }

    /**
     * Adds the items to the trail items array for search results.
     *
     * @since  1.0.0
     * @access protected
     * @return void
     */
    protected function add_search_items() {

        if ( is_paged() )
            $this->items[] = sprintf( '<a href="%s">%s</a>', esc_url( get_search_link() ), sprintf( $this->labels['search'], get_search_query() ) );

        elseif ( true === $this->args['show_title'] )
            $this->items[] = sprintf( $this->labels['search'], get_search_query() );
    }

    /**
     * Adds the items to the trail items array for 404 pages.
     *
     * @since  1.0.0
     * @access protected
     * @return void
     */
    protected function add_404_items() {

        if ( true === $this->args['show_title'] )
            $this->items[] = $this->labels['error_404'];
    }

    /**
     * Adds a specific post's parents to the items array.
     *
     * @since  1.0.0
     * @access protected
     * @param  int    $lawn_gardner_post_id
     * @return void
     */
    protected function add_post_parents( $lawn_gardner_post_id ) {
        $lawn_gardner_parents = array();

        while ( $lawn_gardner_post_id ) {

            // Get the post by ID.
            $post = get_post( $lawn_gardner_post_id );

            // If we hit a page that's set as the front page, bail.
            if ( 'page' == $post->post_type && 'page' == get_option( 'show_on_front' ) && $lawn_gardner_post_id == get_option( 'page_on_front' ) )
                break;

            // Add the formatted post link to the array of parents.
            $lawn_gardner_parents[] = sprintf( '<a href="%s">%s</a>', esc_url( get_permalink( $lawn_gardner_post_id ) ), get_the_title( $lawn_gardner_post_id ) );

            // If there's no longer a post parent, break out of the loop.
            if ( 0 >= $post->post_parent )
                break;

            // Change the post ID to the parent post to continue looping.
            $lawn_gardner_post_id = $post->post_parent;
        }

        // Get the post hierarchy based off the final parent post.
        $this->add_post_hierarchy( $lawn_gardner_post_id );

        // Display terms for specific post type taxonomy if requested.
        if ( ! empty( $this->post_taxonomy[ $post->post_type ] ) )
            $this->add_post_terms( $lawn_gardner_post_id, $this->post_taxonomy[ $post->post_type ] );

        // Merge the parent items into the items array.
        $this->items = array_merge( $this->items, array_reverse( $lawn_gardner_parents ) );
    }

    /**
     * Adds a specific post's hierarchy to the items array.  The hierarchy is determined by post type's
     * rewrite arguments and whether it has an archive page.
     *
     * @since  1.0.0
     * @access protected
     * @param  int    $lawn_gardner_post_id
     * @return void
     */
    protected function add_post_hierarchy( $lawn_gardner_post_id ) {

        // Get the post type.
        $lawn_gardner_post_type        = get_post_type( $lawn_gardner_post_id );
        $lawn_gardner_post_type_object = get_post_type_object( $lawn_gardner_post_type );

        // If this is the 'post' post type, get the rewrite front items and map the rewrite tags.
        if ( 'post' === $lawn_gardner_post_type ) {

            // Add $wp_rewrite->front to the trail.
            $this->add_rewrite_front_items();

            // Map the rewrite tags.
            $this->map_rewrite_tags( $lawn_gardner_post_id, get_option( 'permalink_structure' ) );
        }

        // If the post type has rewrite rules.
        elseif ( false !== $lawn_gardner_post_type_object->rewrite ) {

            // If 'with_front' is true, add $wp_rewrite->front to the trail.
            if ( isset( $lawn_gardner_post_type_object->rewrite['with_front'] ) && $lawn_gardner_post_type_object->rewrite['with_front'] )
                $this->add_rewrite_front_items();

            // If there's a path, check for parents.
            if ( ! empty( $lawn_gardner_post_type_object->rewrite['slug'] ) )
                $this->add_path_parents( $lawn_gardner_post_type_object->rewrite['slug'] );
        }

        // If there's an archive page, add it to the trail.
        if ( $lawn_gardner_post_type_object->has_archive ) {

            // Add support for a non-standard label of 'archive_title' (special use case).
            $lawn_gardner_label = ! empty( $lawn_gardner_post_type_object->labels->archive_title ) ? $lawn_gardner_post_type_object->labels->archive_title : $lawn_gardner_post_type_object->labels->name;

            // Core filter hook.
            $lawn_gardner_label = apply_filters( 'post_type_archive_title', $lawn_gardner_label, $lawn_gardner_post_type_object->name );

            $this->items[] = sprintf( '<a href="%s">%s</a>', esc_url( get_post_type_archive_link( $lawn_gardner_post_type ) ), $lawn_gardner_label );
        }

        // Map the rewrite tags if there's a `%` in the slug.
        if ( 'post' !== $lawn_gardner_post_type && ! empty( $lawn_gardner_post_type_object->rewrite['slug'] ) && false !== strpos( $lawn_gardner_post_type_object->rewrite['slug'], '%' ) )
            $this->map_rewrite_tags( $lawn_gardner_post_id, $lawn_gardner_post_type_object->rewrite['slug'] );
    }

    /**
     * Gets post types by slug.  This is needed because the get_post_types() function doesn't exactly
     * match the 'has_archive' argument when it's set as a string instead of a boolean.
     *
     * @since  0.6.0
     * @access protected
     * @param  int    $lawn_gardner_slug  The post type archive slug to search for.
     * @return void
     */
    protected function get_post_types_by_slug( $lawn_gardner_slug ) {

        $lawn_gardner_return = array();

        $lawn_gardner_post_types = get_post_types( array(), 'objects' );

        foreach ( $lawn_gardner_post_types as $lawn_gardner_type ) {

            if ( $lawn_gardner_slug === $lawn_gardner_type->has_archive || ( true === $lawn_gardner_type->has_archive && $lawn_gardner_slug === $lawn_gardner_type->rewrite['slug'] ) )
                $lawn_gardner_return[] = $lawn_gardner_type;
        }

        return $lawn_gardner_return;
    }

    /**
     * Adds a post's terms from a specific taxonomy to the items array.
     *
     * @since  1.0.0
     * @access protected
     * @param  int     $lawn_gardner_post_id  The ID of the post to get the terms for.
     * @param  string  $lawn_gardner_taxonomy The taxonomy to get the terms from.
     * @return void
     */
    protected function add_post_terms( $lawn_gardner_post_id, $lawn_gardner_taxonomy ) {

        // Get the post type.
        $lawn_gardner_post_type = get_post_type( $lawn_gardner_post_id );

        // Get the post categories.
        $lawn_gardner_terms = get_the_terms( $lawn_gardner_post_id, $lawn_gardner_taxonomy );

        // Check that categories were returned.
        if ( $lawn_gardner_terms && ! is_wp_error( $lawn_gardner_terms ) ) {

            // Sort the terms by ID and get the first category.
            if ( function_exists( 'wp_list_sort' ) )
                $lawn_gardner_terms = wp_list_sort( $lawn_gardner_terms, 'term_id' );

            else
                usort( $lawn_gardner_terms, '_usort_terms_by_ID' );

            $lawn_gardner_term = get_term( $lawn_gardner_terms[0], $lawn_gardner_taxonomy );

            // If the category has a parent, add the hierarchy to the trail.
            if ( 0 < $lawn_gardner_term->parent )
                $this->add_term_parents( $lawn_gardner_term->parent, $lawn_gardner_taxonomy );

            // Add the category archive link to the trail.
            $this->items[] = sprintf( '<a href="%s">%s</a>', esc_url( get_term_link( $lawn_gardner_term, $lawn_gardner_taxonomy ) ), $lawn_gardner_term->name );
        }
    }

    /**
     * Get parent posts by path.  Currently, this method only supports getting parents of the 'page'
     * post type.  The goal of this function is to create a clear path back to home given what would
     * normally be a "ghost" directory.  If any page matches the given path, it'll be added.
     *
     * @since  1.0.0
     * @access protected
     * @param  string $lawn_gardner_path The path (slug) to search for posts by.
     * @return void
     */
    function add_path_parents( $lawn_gardner_path ) {

        // Trim '/' off $lawn_gardner_path in case we just got a simple '/' instead of a real path.
        $lawn_gardner_path = trim( $lawn_gardner_path, '/' );

        // If there's no path, return.
        if ( empty( $lawn_gardner_path ) )
            return;

        // Get parent post by the path.
        $post = get_page_by_path( $lawn_gardner_path );

        if ( ! empty( $post ) ) {
            $this->add_post_parents( $post->ID );
        }

        elseif ( is_null( $post ) ) {

            // Separate post names into separate paths by '/'.
            $lawn_gardner_path = trim( $lawn_gardner_path, '/' );
            preg_match_all( "/\/.*?\z/", $lawn_gardner_path, $lawn_gardner_matches );

            // If matches are found for the path.
            if ( isset( $lawn_gardner_matches ) ) {

                // Reverse the array of matches to search for posts in the proper order.
                $lawn_gardner_matches = array_reverse( $lawn_gardner_matches );

                // Loop through each of the path matches.
                foreach ( $lawn_gardner_matches as $lawn_gardner_match ) {

                    // If a match is found.
                    if ( isset( $lawn_gardner_match[0] ) ) {

                        // Get the parent post by the given path.
                        $lawn_gardner_path = str_replace( $lawn_gardner_match[0], '', $lawn_gardner_path );
                        $post = get_page_by_path( trim( $lawn_gardner_path, '/' ) );

                        // If a parent post is found, set the $lawn_gardner_post_id and break out of the loop.
                        if ( ! empty( $post ) && 0 < $post->ID ) {
                            $this->add_post_parents( $post->ID );
                            break;
                        }
                    }
                }
            }
        }
    }

    /**
     * Searches for term parents of hierarchical taxonomies.  This function is similar to the WordPress
     * function get_category_parents() but handles any type of taxonomy.
     *
     * @since  1.0.0
     * @param  int    $lawn_gardner_term_id  ID of the term to get the parents of.
     * @param  string $lawn_gardner_taxonomy Name of the taxonomy for the given term.
     * @return void
     */
    function add_term_parents( $lawn_gardner_term_id, $lawn_gardner_taxonomy ) {

        // Set up some default arrays.
        $lawn_gardner_parents = array();

        // While there is a parent ID, add the parent term link to the $lawn_gardner_parents array.
        while ( $lawn_gardner_term_id ) {

            // Get the parent term.
            $lawn_gardner_term = get_term( $lawn_gardner_term_id, $lawn_gardner_taxonomy );

            // Add the formatted term link to the array of parent terms.
            $lawn_gardner_parents[] = sprintf( '<a href="%s">%s</a>', esc_url( get_term_link( $lawn_gardner_term, $lawn_gardner_taxonomy ) ), $lawn_gardner_term->name );

            // Set the parent term's parent as the parent ID.
            $lawn_gardner_term_id = $lawn_gardner_term->parent;
        }

        // If we have parent terms, reverse the array to put them in the proper order for the trail.
        if ( ! empty( $lawn_gardner_parents ) )
            $this->items = array_merge( $this->items, array_reverse( $lawn_gardner_parents ) );
    }

    /**
     * Turns %tag% from permalink structures into usable links for the breadcrumb trail.  This feels kind of
     * hackish for now because we're checking for specific %tag% examples and only doing it for the 'post'
     * post type.  In the future, maybe it'll handle a wider variety of possibilities, especially for custom post
     * types.
     *
     * @since  0.6.0
     * @access protected
     * @param  int    $lawn_gardner_post_id ID of the post whose parents we want.
     * @param  string $lawn_gardner_path    Path of a potential parent page.
     * @param  array  $lawn_gardner_args    Mixed arguments for the menu.
     * @return array
     */
    protected function map_rewrite_tags( $lawn_gardner_post_id, $lawn_gardner_path ) {

        $post = get_post( $lawn_gardner_post_id );

        // Trim '/' from both sides of the $lawn_gardner_path.
        $lawn_gardner_path = trim( $lawn_gardner_path, '/' );

        // Split the $lawn_gardner_path into an array of strings.
        $lawn_gardner_matches = explode( '/', $lawn_gardner_path );

        // If matches are found for the path.
        if ( is_array( $lawn_gardner_matches ) ) {

            // Loop through each of the matches, adding each to the $trail array.
            foreach ( $lawn_gardner_matches as $lawn_gardner_match ) {

                // Trim any '/' from the $lawn_gardner_match.
                $lawn_gardner_tag = trim( $lawn_gardner_match, '/' );

                // If using the %year% tag, add a link to the yearly archive.
                if ( '%year%' == $lawn_gardner_tag )
                    $this->items[] = sprintf( '<a href="%s">%s</a>', esc_url( get_year_link( get_the_time( 'Y', $lawn_gardner_post_id ) ) ), sprintf( $this->labels['archive_year'], get_the_time( esc_html_x( 'Y', 'yearly archives date format',  'lawn-gardner' ) ) ) );

                // If using the %monthnum% tag, add a link to the monthly archive.
                elseif ( '%monthnum%' == $lawn_gardner_tag )
                    $this->items[] = sprintf( '<a href="%s">%s</a>', esc_url( get_month_link( get_the_time( 'Y', $lawn_gardner_post_id ), get_the_time( 'm', $lawn_gardner_post_id ) ) ), sprintf( $this->labels['archive_month'], get_the_time( esc_html_x( 'F', 'monthly archives date format', 'lawn-gardner' ) ) ) );

                // If using the %day% tag, add a link to the daily archive.
                elseif ( '%day%' == $lawn_gardner_tag )
                    $this->items[] = sprintf( '<a href="%s">%s</a>', esc_url( get_day_link( get_the_time( 'Y', $lawn_gardner_post_id ), get_the_time( 'm', $lawn_gardner_post_id ), get_the_time( 'd', $lawn_gardner_post_id ) ) ), sprintf( $this->labels['archive_day'], get_the_time( esc_html_x( 'j', 'daily archives date format', 'lawn-gardner' ) ) ) );

                // If using the %author% tag, add a link to the post author archive.
                elseif ( '%author%' == $lawn_gardner_tag )
                    $this->items[] = sprintf( '<a href="%s">%s</a>', esc_url( get_author_posts_url( $post->post_author ) ), get_the_author_meta( 'display_name', $post->post_author ) );

                // If using the %category% tag, add a link to the first category archive to match permalinks.
                elseif ( taxonomy_exists( trim( $lawn_gardner_tag, '%' ) ) ) {

                    // Force override terms in this post type.
                    $this->post_taxonomy[ $post->post_type ] = false;

                    // Add the post categories.
                    $this->add_post_terms( $lawn_gardner_post_id, trim( $lawn_gardner_tag, '%' ) );
                }
            }
        }
    }
}