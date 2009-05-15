$(document).ready(function(){

    /********************************************************************************/
    /*
    Static events handlers
    */
    /********************************************************************************/
    /* handles tabs clicks */
    $(".tab-links a").live("click",function(){
        $(".tab-contents .tab").addClass("hidden");
        $("#" + $(this).attr("rel")).removeClass("hidden");

        $(".tab-links a").removeClass("active");
        $(this).addClass("active");
        return false;

    });

    /* make page contents sortable */
    $(".tab").sortable();

    /* add pages to story */
    $("#add-story-page").click(function(){

        var tab_prefix = "story-content-";
        var last_tab_id = $(".tab-links a:last").attr("rel").replace(tab_prefix,"");
        var new_tab_id = (parseInt(last_tab_id) + 1);

        /* create a new tab */
        var new_tab = $(".tab-links a:last").clone().insertAfter(".tab-links a:last");
        new_tab.removeClass("active").attr("rel",new_tab.attr("rel").replace(tab_prefix + last_tab_id, tab_prefix + new_tab_id));
        new_tab.text(new_tab.text().replace(last_tab_id,new_tab_id));

        /* create a new content area */
        $(".tab-contents .tab:last").clone().sortable().appendTo(".tab-contents").attr("id",tab_prefix + new_tab_id).html("");

        return false;
    });

    /* handling text blocks links */
    $("#page-text-blocks a").click(function(){

        $.get($(this).attr("href"),function(data){
            var new_widget = $(data).appendTo(".tab-contents .tab:not(.hidden)");
            widget.text_edit(new_widget);
        });

        return false;
    });


    /*
    this is where we save pages
    this is important stuff
    */
    $("#story-save-pages").click(function(){
        var pages = $(".edit-story-tabs .tab-contents .tab");

        $.each(pages,function(i,val){

            $("#story-prepare").html($(val).html());
            var blocks = $("#story-prepare .widget-block");

            $.each(blocks,function(i,val){

                var block = $(val);
                block.children(".widget-options").remove();
                if (block.hasClass("widget-media-block"))
                {
                    var code = block.children(".widget-code");
                    block.after(code.html());
                    block.remove();
                }

            });

            console.log(i);
            console.log($("#story-prepare").html());
            /* save url is defined in story_past_list.html by django */
            $.post(save_url,{ content: $("#story-prepare").html(), pagenum: (i+1), pagecount: pages.length });
        });
    });

    /* handling media blocks links */
    $("#page-media-blocks a").click(function(){

        $.get($(this).attr("href"),function(data){
            var new_widget = $(data).appendTo(".tab-contents .tab:not(.hidden)");

            widget.media.load(new_widget);
            widget.media.edit();
        });

        return false;
    });



    /********************************************************************************/
    /*
    GLOBAL block event handlers
    */
    /********************************************************************************/
    // mouseover on media widgets
    $(".tab-contents .widget-media-block").live("mouseover",function(){
        $("#widget-media-options").appendTo($(this));
    });
    // mouseout on media widgets
    /*
    $(".tab-contents .widget-media-block").live("mouseout",function(){
        $("#widget-media-options").appendTo($("#widget-options"));
    });
    */
    // mouseover on text widgets
    $(".tab-contents .widget-text-block").live("mouseover",function(){
        $("#widget-text-options").appendTo($(this));
    });
    // mouseout ontext  widgets
    /*
    $(".tab-contents .widget-text-block").live("mouseout",function(){
        $("#widget-text-options").appendTo($("#widget-options"));
    });
    */
    /*
    $(".tab-contents").mouseout(function(){
        $("#widget-text-options").appendTo($("#widget-options"));
        $("#widget-media-options").appendTo($("#widget-options"));
    });
    */

    // text widget events
    $("#widget-text-options .widget-edit").bind("click",function(){
            var widget_obj = $(this).parent().parent();
            widget.text_edit(widget_obj);
            return false;
    });

    // text widget events
    $("#widget-media-options .widget-edit").bind("click",function(){
            var widget_obj = $(this).parent().parent();
            widget.media.load(widget_obj);
            widget.media.edit();
            return false;
    });


});

