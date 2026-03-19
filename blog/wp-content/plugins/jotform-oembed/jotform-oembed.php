<?php
/*
    Plugin Name: Jotform oEmbed
    Plugin URI: http://www.jotform.com/labs/wordpress
    Description: Adding a web form to your blog post is now very easy using Jotform’s oEmbed plugin. When you install it, WordPress will be aware of Jotform form URLs, and easily embed them to your blog posts.
    Version: 1.3.3
    Author: Jotform.com
    Author URI: http://www.jotform.com
    License: GNU General Public License v3
*/

class JotFormOEmbed {
    public function __construct() {
        wp_oembed_add_provider('#https?://(secure\.|www\.|form\.|app\.)?(my)?jotform(pro|eu|z)?\.(com|net|us|ca|me|co)(/form|/app|/agent)?/[0-9a-z]*#i', 'https://www.jotform.com/oembed/', true);

        add_action('admin_notices', array($this, 'showNewPluginNotification'));
        add_action('wp_ajax_jotform-ai-chatbot_dismiss_notice', array($this, 'dismissNewPluginNotification'));
    }

    public function showNewPluginNotification() {
        if (!current_user_can('manage_options')) {
            return;
        }
    
        if (get_option('jotform-ai-chatbot_admin_notice_dismissed')) {
            return;
        }
    
        $plugin_slug = 'jotform-ai-chatbot';
        $plugin_url = esc_url("plugin-install.php?tab=plugin-information&plugin=$plugin_slug&TB_iframe=true&width=600&height=550");
    
        ?>
        <div class="notice notice-info is-dismissible" id="jotform-ai-chatbot-admin-notice">
            <p>🚀 <strong>Meet Jotform AI Chatbot!</strong> Automate support, boost engagement & generate leads. No coding needed. <a href="<?php echo $plugin_url; ?>" class="thickbox">Try it now!</a> 🤖✨</p>    
        </div>
        <?php
        
        add_thickbox();

        ?>
        <script>
        jQuery(document).on('click', '#jotform-ai-chatbot-admin-notice .notice-dismiss', function () {
            jQuery.post(ajaxurl, {
                action: 'jotform-ai-chatbot_dismiss_notice'
            });
        });
        </script>
        <?php
    }

    public function dismissNewPluginNotification() {
        update_option('jotform-ai-chatbot_admin_notice_dismissed', true);
        wp_die();
    }
} 

$jotformOEmbed = new JotFormOEmbed();

?>