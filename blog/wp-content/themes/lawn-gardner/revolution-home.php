<?php
/**
 * Template Name: Home Page
 */

get_header();
?>

<?php 
$lawn_gardner_slide_count = get_theme_mod('lawn_gardner_slide_number');
$lawn_gardner_main_slider_wrap = absint(get_theme_mod('lawn_gardner_enable_slider', 0));
if($lawn_gardner_main_slider_wrap == 1){ 
?>

<section id="main-slider-wrap">
    <div class="owl-carousel">
        <?php for ($i=1; $i<=$lawn_gardner_slide_count; $i++) { ?>
            <div class="main-slider-inner-box">
                <?php if ( get_theme_mod('lawn_gardner_slider_image'.$i) ) : ?>
                    <img src="<?php echo esc_url( get_theme_mod('lawn_gardner_slider_image'.$i) ); ?>">
                    <div class="main-slider-content-box">
                        <?php if ( get_theme_mod('lawn_gardner_slider_heading'.$i) ) : ?><h3><?php echo esc_html( get_theme_mod('lawn_gardner_slider_heading'.$i) ); ?></h3><?php endif; ?>
                        <?php if ( get_theme_mod('lawn_gardner_slider_text'.$i) ) : ?><p><?php echo esc_html( get_theme_mod('lawn_gardner_slider_text'.$i) ); ?></p><?php endif; ?>
                        <div class="main-slider-button">
                            <?php if ( get_theme_mod('lawn_gardner_slider_button1_link'.$i) ||  get_theme_mod('lawn_gardner_slider_button1_text'.$i )) : ?><a href="<?php echo esc_url( get_theme_mod('lawn_gardner_slider_button1_link'.$i) ); ?>"><?php echo esc_html( get_theme_mod('lawn_gardner_slider_button1_text'.$i) ); ?></a><?php endif; ?>
                        </div>
                    </div>
                <?php endif; ?>
            </div>
        <?php } ?>
    </div>
</section>

<?php } ?>

<?php 
$lawn_gardner_main_expert_wrap = absint(get_theme_mod('lawn_gardner_enable_project', 0));
if($lawn_gardner_main_expert_wrap == 1){ 
?>

<section id="main-expert-wrap">
    <div class="container">
        <div class="main-expert-heading">
            <?php if ( get_theme_mod('lawn_gardner_project_heading') ) : ?><h3><?php echo esc_html( get_theme_mod('lawn_gardner_project_heading') ); ?></h3><?php endif; ?>
        </div>

        <div class="tabs">
            <?php if ( get_theme_mod('lawn_gardner_project_tab1') ) : ?><div class="tab text-green-600" data-tab="tab1"><?php echo esc_html( get_theme_mod('lawn_gardner_project_tab1') ); ?></h3></div><?php endif; ?>
            <?php if ( get_theme_mod('lawn_gardner_project_tab2') ) : ?><div class="tab text-green-600" data-tab="tab2"><?php echo esc_html( get_theme_mod('lawn_gardner_project_tab2') ); ?></h3></div><?php endif; ?>
            <?php if ( get_theme_mod('lawn_gardner_project_tab3') ) : ?><div class="tab text-green-600" data-tab="tab3"><?php echo esc_html( get_theme_mod('lawn_gardner_project_tab3') ); ?></h3></div><?php endif; ?>
        </div>
        <div class="content-box">
            <?php if ( get_theme_mod('lawn_gardner_project_tab1') ) { ?>
            <div id="tab1" class="content"> 
                <?php for ($i=1; $i <= 3; $i++) { ?>
                    <div class="tab-content mt-4">
                        <div class="rel-post-wrapp">
                            <div class="box rel-card-item">
                                <?php if ( get_theme_mod('lawn_gardner_project_image_tab1'.$i) ) : ?><img src="<?php echo esc_url( get_theme_mod('lawn_gardner_project_image_tab1'.$i) ); ?>"><?php endif; ?>
                                <div class="box-content">
                                    <?php if ( get_theme_mod('lawn_gardner_project_box_heading_tab1'.$i) ) : ?><h4><?php echo esc_html( get_theme_mod('lawn_gardner_project_box_heading_tab1'.$i) ); ?></h4><?php endif; ?>
                                    <?php if ( get_theme_mod('lawn_gardner_project_box_content_tab1'.$i) ) : ?><p><?php echo esc_html( get_theme_mod('lawn_gardner_project_box_content_tab1'.$i) ); ?></p><hr><?php endif; ?>
                                    <?php if ( get_theme_mod('lawn_gardner_project_box_text_tab1'.$i) ) : ?><p><?php echo esc_html( get_theme_mod('lawn_gardner_project_box_text_tab1'.$i) ); ?></p><?php endif; ?>
                                </div>
                            </div>
                        </div>
                    </div>
                <?php } ?>
            </div>
            <?php } ?>
            <?php if ( get_theme_mod('lawn_gardner_project_tab2') ) { ?>
            <div id="tab2" class="content">
                <?php for ($i=1; $i <= 3; $i++) { ?>
                    <div class="tab-content mt-4">
                         <div class="rel-post-wrapp">
                            <div class="box rel-card-item">
                                <?php if ( get_theme_mod('lawn_gardner_project_image_tab2'.$i) ) : ?><img src="<?php echo esc_url( get_theme_mod('lawn_gardner_project_image_tab2'.$i) ); ?>"><?php endif; ?>
                                <div class="box-content">
                                    <?php if ( get_theme_mod('lawn_gardner_project_box_heading_tab2'.$i) ) : ?><h4><?php echo esc_html( get_theme_mod('lawn_gardner_project_box_heading_tab2'.$i) ); ?></h4><?php endif; ?>
                                    <?php if ( get_theme_mod('lawn_gardner_project_box_content_tab2'.$i) ) : ?><p class="text"><?php echo esc_html( get_theme_mod('lawn_gardner_project_box_content_tab2'.$i) ); ?></p><hr><?php endif; ?>
                                    <?php if ( get_theme_mod('lawn_gardner_project_box_text_tab2'.$i) ) : ?><p><?php echo esc_html( get_theme_mod('lawn_gardner_project_box_text_tab2'.$i) ); ?></p><?php endif; ?>
                                </div>
                            </div>
                        </div>
                    </div>
                <?php } ?>
            </div>
            <?php } ?>
            <?php if ( get_theme_mod('lawn_gardner_project_tab3') ) { ?>
            <div id="tab3" class="content">
                <?php for ($i=1; $i <= 3; $i++) { ?>
                    <div class="tab-content mt-4">
                        <div class="rel-post-wrapp">
                            <div class="box rel-card-item">
                                <?php if ( get_theme_mod('lawn_gardner_project_image_tab3'.$i) ) : ?><img src="<?php echo esc_url( get_theme_mod('lawn_gardner_project_image_tab3'.$i) ); ?>"><?php endif; ?>
                                <div class="box-content">
                                    <?php if ( get_theme_mod('lawn_gardner_project_box_heading_tab3'.$i) ) : ?><h4 class=""><?php echo esc_html( get_theme_mod('lawn_gardner_project_box_heading_tab3'.$i) ); ?></h4><?php endif; ?>
                                    <?php if ( get_theme_mod('lawn_gardner_project_box_content_tab3'.$i) ) : ?><p class=""><?php echo esc_html( get_theme_mod('lawn_gardner_project_box_content_tab3'.$i) ); ?></p><hr><?php endif; ?>
                                    <?php if ( get_theme_mod('lawn_gardner_project_box_text_tab3'.$i) ) : ?><p><?php echo esc_html( get_theme_mod('lawn_gardner_project_box_text_tab3'.$i) ); ?></p><?php endif; ?>
                                </div>
                            </div>
                        </div>
                    </div>
                <?php } ?>
            </div>
            <?php } ?>
        </div>
    </div>
</section>

<?php } ?>

<?php
get_footer();