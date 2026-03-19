jQuery(document).ready(function ($) {
    /*
    ** ### Back to top function
    */
    

    /* -----------------------------------------
    Preloader
    ----------------------------------------- */
    jQuery('#preloader').delay(1500).fadeOut();
    jQuery('#loader').delay(1500).fadeOut("slow");

    if ($('.go-to-top').length) {
        var scrollTrigger = $('body').position(); // px
        goToTop = function () {

            var scrollTop = $(window).scrollTop();
            if (scrollTop > 150) {
                $('.footer-go-to-top').addClass('show');
            } else {
                $('.footer-go-to-top').removeClass('show');
            }
        };
        goToTop();
        $(window).on('scroll', function () {
            goToTop();
        });
        $('.go-to-top').on('click', function (e) {
            e.preventDefault();
            $('html,body').animate({
                scrollTop: scrollTrigger.top
            }, 700);
        });
    }

    // Mobile Menu Focus
    var width = $(window).width();
    if (width < 992) {
        $('.main-navigation').on('keydown', function (e) {
            if ($('.main-navigation').hasClass('toggled')) {
                var focusableEls = $('.main-navigation a[href]:not([disabled]), .main-navigation button');
                var firstFocusableEl = focusableEls[0];
                var lastFocusableEl = focusableEls[focusableEls.length - 1];
                var KEYCODE_TAB = 9;
                var KEYCODE_ESC = 27;
                if (e.key === 'Tab' || e.keyCode === KEYCODE_TAB) {
                    if (e.shiftKey) /* shift + tab */ {
                        if (document.activeElement === firstFocusableEl) {
                            lastFocusableEl.focus();
                            e.preventDefault();
                        }
                    }
                    else /* tab */ {
                        if (document.activeElement === lastFocusableEl) {
                            firstFocusableEl.focus();
                            e.preventDefault();
                        }
                    }
                }

                if (e.keyCode === KEYCODE_ESC) {
                    console.log(e.keyCode);
                    $('.main-navigation').removeClass('toggled');
                    return;
                }
            }
            
        });
    }

    var owl = jQuery('#main-slider-wrap .owl-carousel');
    owl.owlCarousel({
        margin:20,
        nav: true,
        autoplay : false,
        lazyLoad: false,
        autoplayTimeout: 2000,
        loop: true,
        rtl: $('html').attr('dir') === 'rtl',  // Set RTL based on HTML direction
        dots: false,
        navText : ['<i class="fas fa-arrow-left"></i>','<i class="fas fa-arrow-right"></i> '],
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 1
            },
            1000: {
                items: 1
            }
        },
        autoplayHoverPause : true,
        mouseDrag: true
    });

        jQuery('.search-box span a').click(function(){
        jQuery(".serach_outer").slideDown(1000);
        (jQuery('.serach_outer'));
    });

    jQuery('.closepop a').click(function(){
        jQuery(".serach_outer").slideUp(1000);
    });
    
    const tabs = document.querySelectorAll('.tab');
    const contents = document.querySelectorAll('.content');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const activeTab = tab.getAttribute('data-tab');
            contents.forEach(content => {
                if (content.id === activeTab) {
                    content.classList.remove('hidden');
                } else {
                    content.classList.add('hidden');
                }
            });
        });
    });
    var selector = '.tab';

    $(selector).on('click', function(){
        $(selector).removeClass('active');
        $(this).addClass('active');
    });
    // console.log('asds', jQuery('.tabs').find('[data-tab=tab1]'))
    jQuery('.tabs').find('[data-tab=tab1]').addClass('active')
    jQuery('#tab2').addClass('hidden')
    jQuery('#tab3').addClass('hidden')
});

jQuery(function($) {
    $('#myTabs a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const header = document.querySelector('.sticky-header');
    if (header) { // Check if header exists
        window.addEventListener('scroll', function() {
        if (window.scrollY > 0) {
            header.classList.add('stickyon');
        } else {
            header.classList.remove('stickyon');
        }
        });
    }
});