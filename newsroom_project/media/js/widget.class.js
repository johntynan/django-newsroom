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

    bind_options : function(){
        var obj = $(".tab-contents .widget-block");
        obj.bind("mouseover",widget.show_options);
        obj.bind("mouseout",widget.hide_options);
        obj.children(".widget-options").children(".widget-remove").bind("click", widget.block_remove);
        obj.children(".widget-options").children(".widget-move_up").bind("click", widget.block_move_up);
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
        $(".tab-contents .tab:not(.hidden)").append(data);
        widget.bind_options();
        return false;
    },
}