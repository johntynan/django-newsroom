var widget = {

    edit_html : '<div class="w21-options"><a href="" class="w21-move">edit</a> | <a href="" class="w21-move">move</a></div>',

    block_remove : function(){
        //$(this).append(widget.edit_html);
        $(this).parent().parent().remove();
        return false;
    },

    block_move_up : function(){
        $(this).parent().parent().prev().attr("id","insertBefore");
        $(this).parent().parent().insertBefore("#insertBefore");
        $("#insertBefore").attr("id","");
        //$(this).parent().parent().remove();
        return false;
    },

    show_options : function(){
        $(this).children(".widget-options").removeClass("hidden");
    },

    hide_options : function(){
        $(this).children(".widget-options").addClass("hidden");
    },

    tb_show : function() {
        tb_show(null,this.href,false);
        this.blur();
        return false;
    },

    bind_options : function(){
        var obj = $(".tab-contents .widget-block");
        obj.bind("mouseover",widget.show_options);
        obj.bind("mouseout",widget.hide_options);
        obj.children(".widget-options").children(".widget-remove").bind("click", widget.block_remove);
        obj.children(".widget-options").children(".widget-move_up").bind("click", widget.block_move_up);
        obj.children(".widget-options").children(".widget-edit").bind("click", widget.tb_show);
        obj.removeClass("unbinded");
    },

    /* add a template to story */
    add_to_story : function(){

        $(".widget-add").click(function(){
            var widget_block = $(this).parent().children(".widget-html");
            var story_content = $(".tab-contents .tab:not(.hidden)").html();

            story_content += widget_block.html();

            $(".tab-contents .tab:not(.hidden)").html(story_content);

            widget.bind_options();

            return false;
        });
    },

    /* add a template to story */
    add_to_page : function(data){
        var new_widget = $(data).appendTo(".tab-contents .tab:not(.hidden)").addClass("editing-mode");
        widget.bind_options();

        var url = new_widget.children(".widget-options").children(".widget-edit").attr("href");

        tb_show(null,url,false,function(){
            $("#textarea-editor").val(new_widget.children(".widget-content").html());
            widget.initMCE();
        });

        return false;
    },

    save_text_editor : function(){
        var content = $("#textarea-editor_ifr").contents().find("body").html();
        $(".editing-mode").removeClass("editing-mode").children(".widget-content").html(content);
        tb_remove();
    },


    initMCE : function(){

        // O2k7 skin (silver)
        tinyMCE.init({
            // General options
            mode : "exact",
            elements : "textarea-editor",
            theme : "advanced",
            skin : "o2k7",
            skin_variant : "black",
            plugins : "safari,pagebreak,style,layer,table,save,advhr,advimage,advlink,emotions,iespell,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template,inlinepopups",

            // Theme options
            theme_advanced_buttons1 : "save,newdocument,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,formatselect,fontsizeselect",
            theme_advanced_buttons2 : "cut,copy,paste,pastetext,pasteword,|,search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,cleanup,help,code",
            theme_advanced_buttons3 : "tablecontrols,|,hr,removeformat,visualaid,|,fullscreen",
            theme_advanced_toolbar_location : "top",
            theme_advanced_toolbar_align : "left",
            theme_advanced_statusbar_location : "bottom",
            theme_advanced_resizing : true,

            save_callback : "widget.save_text_editor",


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
            // Replace values for the template plugin
            template_replace_values : {
                username : "Some User",
                staffid : "991234"
            }

        });
    }
};