var widget = {

    layout_list : function(){

        function callback_init()
        {
            $("#page-layout-list").load("/page_layouts/snippet.html");
        }

        var url = $("#add-story-page").attr("href");
        // add ? to the url, because of the random parameter added by thickbox
        url += '?height=450px';

        widget.lightbox(url,callback_init);

        return false;
    },

    text_edit : function(widget_obj){

        function callback_init()
        {
            $("#textarea-editor").val(widget_obj.children(".widget-content").html());
            widget.init_editor();

            if (widget_obj.hasClass("clear"))
                $("input[value='clear']").attr("checked","checked");
            else
                $("input[value='']").attr("checked","checked");

            $("#lb-block-save").click(function(){
                var content = $("#textarea-editor_ifr").contents().find("body").html();
                var clear_opt = $("input[name='wrap_text']:checked").val();
                if (clear_opt)
                    widget_obj.addClass("clear");
                else
                    widget_obj.removeClass("clear");
                widget_obj.children(".widget-content").html(content);
                tb_remove();
            });

        };

        widget.lightbox(page_text_editor_url,callback_init);
        return false;
    },

    image_change : function(widget_obj){

        function callback_init()
        {
            /*** 
            Calls view at /newsroom/story/2/media/ via ajax and renders
            templates/stories/story_media_list_ajax.html which loops through
            story.get_relatedcontent, a dict of related media, like: {'photo':
            [<Photo: green dragons>, <Photo: squirrel>]} 
            ***/
            $("#ajax-media-list").load(page_media_source_url,function(){
                $("#ajax-media-list .media-item").click(function(){
                    var media_url = $(this).attr("href");
                    widget_obj.children("img").attr("src",media_url);
                    widget.remove_lightbox();
                    return false;
                });

            });
            return true;
        };
	    // load the greybox content from 
        // /newsroom/template/media_list/?width=750&height=500
        widget.lightbox(page_media_list_url,callback_init);
        return false;
    },


    popup_set : function(widget_obj){

        function callback_init(){
            $("#ajax-media-list").load(page_media_source_url,function(){
                $("#ajax-media-list .media-item").click(function(){
                    var media_url = $(this).attr("href");
                    var popup_url = $(this).siblings('.popup-url').attr('href');
                    widget_obj.css("background-image", "url("+media_url+")");
                    //console.log(popup_url);
                    //console.log(widget_obj.height());
                    //widget_obj.attr('height',widget_obj.height());
                    //console.log(widget_obj.children(".thickbox"));
                    widget_obj.children(".thickbox").attr("href", popup_url);
                    //console.log(widget_obj.children("img"));
                    //.removeAttr("width");
                    widget.remove_lightbox();
                    return false;
                });
            });
            return true;
        }

        widget.lightbox(page_media_list_url, callback_init);
        return false;
    },

    flash_set : function(widget_obj){

        function callback_init(){
            $("#ajax-media-list").load(page_media_source_url,function(){
                $("#ajax-media-list .media-item").click(function(){
                    var render_url = $(this).siblings('.render-url').attr('href');
                    widget_obj.load(render_url);
                    widget.remove_lightbox();
                    return false;
                });
            });
            return true;
        }

        widget.lightbox(page_media_list_url, callback_init);
        return false;
    },

    video_set : function(widget_obj){

        function callback_init(){
            $("#ajax-media-list").load(page_media_source_url,function(){
                $("#ajax-media-list .media-item").click(function(){
                    var render_url = $(this).siblings('.render-url').attr('href');
                    console.log(render_url);
                    widget_obj.load(render_url);
                    //console.log(widget_obj.height());
                    //widget_obj.attr('height',widget_obj.height());
                    //console.log(widget_obj.children(".thickbox"));
                    //widget_obj.children(".thickbox").attr("href", popup_url);
                    //console.log(widget_obj.children("img"));
                    //.removeAttr("width");
                    widget.remove_lightbox();
                    return false;
                });
            });
            return true;
        }

        widget.lightbox(page_media_list_url, callback_init);
        return false;
    },
    /* show a generic lightbox with a callback_init function as parameter */
    lightbox : function(url,callback_init) {

        tb_show(null,url,false,callback_init);
        return false;
    },

    /* remove the lightbox */
    remove_lightbox: function() {
        tb_remove();
    },

    /* init Rich Text Editor */
    init_editor : function(){

        // O2k7 skin (silver)
        tinyMCE.init({
            // General options
            mode : "exact",
            elements : "textarea-editor",
            theme : "advanced",
            skin : "o2k7",
            skin_variant : "black",
            width : "725",
            height :"350",
            plugins : "safari,pagebreak,style,layer,table,save,advhr,advimage,advlink,emotions,iespell,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template,inlinepopups",

            // Theme options
            //theme_advanced_buttons1 : "newdocument,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,formatselect,fontsizeselect",
            theme_advanced_buttons1 : "bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,formatselect,fontsizeselect",
            theme_advanced_buttons2 : "cut,copy,paste,pastetext,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,code",
            //theme_advanced_buttons2 : "cut,copy,paste,pastetext,pasteword,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,cleanup,help,code",
            //theme_advanced_buttons2 : "",
            theme_advanced_buttons3 : "tablecontrols,|,hr,removeformat,visualaid,|,fullscreen",
            // theme_advanced_buttons3 : "",
            theme_advanced_toolbar_location : "top",
            theme_advanced_toolbar_align : "left",
            theme_advanced_statusbar_location : "bottom",
            theme_advanced_resizing : false,
            invalid_elements: "",
            extended_valid_elements : "object,applet,script,iframe[src|width|height]",
            /*
            save_callback : "widget.save_text_editor",
            */


            // Example content CSS (should be your site CSS)
            /*
            content_css : "css/content.css",
            */

            // Drop lists for link/image/media/template dialogs
            /*
            template_external_list_url : "lists/template_list.js",
            external_link_list_url : "lists/link_list.js",
            external_image_list_url : "lists/image_list.js",
            media_external_list_url : "lists/media_list.js",
            */

        });
    }
};
