var widget = {

    edit_html : '<div class="w21-options"><a href="" class="w21-move">edit</a> | <a href="" class="w21-move">move</a></div>',

    page_break : function(){
        var html = '<li class="w21-page_break clear"><span class="float-left">PAGE BREAK</span><div class="widget-options"><a href="" class="widget-edit">Edit</a><a href="" class="widget-move_up">Move up</a><a href="" class="widget-move_down">Move down</a><a href="" class="widget-remove">Remove</a></div></li>';
        return html;
    },

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

    add_to_story : function(){

        $(".widget-add").click(function(){
            var widget_block = $(this).parent().children(".widget-html");
            var story_content = $("#story-content").html();

            if (widget_block.hasClass("widget-page_template") && story_content != "")
            {
                story_content += widget.page_break();
            }

            story_content += widget_block.html();

            $("#story-content").html(story_content);

            var block_list = $("#story-content .widget-block.unbinded");
            $.each(block_list,function(i,val){
                $(val).children(".widget-options").children(".widget-remove").bind("click", widget.block_remove);
                $(val).children(".widget-options").children(".widget-move_up").bind("click", widget.block_move_up);
                $(val).removeClass("unbinded");
            });

            return false;
        });
    },
}