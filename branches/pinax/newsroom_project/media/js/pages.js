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

    /* handling media blocks links */
    $("#page-media-blocks a").click(function(){

        $.get($(this).attr("href"),function(data){
            var new_widget = $(data).appendTo(".tab-contents .tab:not(.hidden)");
            widget.image_edit(new_widget);
        });

        return false;
    });



    /********************************************************************************/
    /*
    GLOBAL block event handlers
    */
    /********************************************************************************/
    // mouseover on widgets
    $(".tab-contents .widget-block").live("mouseover",function(){
        $(this).children(".widget-options").removeClass("hidden");
    });
    // mouseout on widgets
    $(".tab-contents .widget-block").live("mouseout",function(){
        $(this).children(".widget-options").addClass("hidden");
    });

    // text widget events
    $(".widget-text-block .widget-edit").live("click",function(){
            widget.text_edit($(this).parent().parent());
            return false;
    });


});

