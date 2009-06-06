$(document).ready(function(){

    /********************************************************************************/
    /*
    Static events handlers
    */
    /********************************************************************************/
    /* handles tabs clicks */
    function trigger_tab_click(jquery_obj)
    {
        $(".tab-contents .tab").addClass("hidden");
        $("#" + jquery_obj.attr("rel")).removeClass("hidden");

        $(".tab-links a").removeClass("active");
        jquery_obj.addClass("active");

        return false;
    }

    $(".tab-links a.page_nav").live("click",function(){
        return trigger_tab_click($(this));;
    });

    /* make page contents sortable */
    //$(".tab").sortable();


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
        $(".tab-contents .tab:last").clone().appendTo(".tab-contents").attr("id",tab_prefix + new_tab_id).html("");

        widget.layout_list();

        return trigger_tab_click($(".tab-links a:last"));
    });

    /* add templates to page */
    $("#add-layout").click(function(){

        widget.layout_list();

        return false;
    });

    /*
    this is where we save pages
    this is important stuff
    */

    $("#story-save-pages").click(function(){
        var pages = $(".edit-story-tabs .tab-contents .tab");

        $("#save-page-form textarea:not(:first)").remove();
        content_field = $("#save-page-form textarea:first").val("");

        $("#save-page-form input[type=text]:not(:first)").remove();
        pagenum_field = $("#save-page-form input[type=text]:first").val("");

        //$("#id_form-TOTAL_FORMS").val(pages.length);

        var post_vars = { "form-TOTAL_FORMS" : pages.length, "form-INITIAL_FORMS" : 0 }

        /* cycle each page in html */
        $.each(pages,function(i,val){
            post_vars[content_field.attr("name").replace("0",i)] = $(val).html();
            post_vars[pagenum_field.attr("name").replace("0",i)] = i+1;
        });

        $.post($("#save-page-form").attr("action"),post_vars);
    });



    /********************************************************************************/
    /*
    GLOBAL block event handlers
    */
    /********************************************************************************/
    // text widget events
    $(".widget-text-block").live("click",function(){
        var widget_obj = $(this);
        widget.text_edit(widget_obj);
        return false;
    });

    // media widget events
    $(".widget-image-block").live("click",function(){
        var widget_obj = $(this);
        widget.image_change(widget_obj);
        return false;
    });

    /* add a template to story */
    $(".layout-add").live("click",function(){
        var widget_block = $(this).parent().children(".layout-html");
        var story_content = $(".tab-contents .tab:not(.hidden)").html();

        story_content += widget_block.html();

        $(".tab-contents .tab:not(.hidden)").html(story_content);

        tb_remove();
        return false;
    });


});

