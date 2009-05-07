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

    add_to_story : function(){

        $(".widget-add").click(function(){
            var widget_block = $(this).parent().children(".widget-html");
            var story_content = $(".tab-contents .tab:not(.hidden)").html();

            story_content += widget_block.html();

            $(".tab-contents .tab:not(.hidden)").html(story_content);

            var block_list = $(".tab-contents .widget-block.unbinded");
            $.each(block_list,function(i,val){
                $(val).children(".widget-options").children(".widget-remove").bind("click", widget.block_remove);
                $(val).children(".widget-options").children(".widget-move_up").bind("click", widget.block_move_up);
                $(val).removeClass("unbinded");
            });

            return false;
        });
    },
}