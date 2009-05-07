$(document).ready(function(){

/* reusable function to handle tab clicks */
function tab_click()
{
    $(".tab-contents .tab").addClass("hidden");
    $("#" + $(this).attr("rel")).removeClass("hidden");

    $(".tab-links a").removeClass("active");
    $(this).addClass("active");
    return false;
}

/* handle tab clicks */
$(".tab-links a").click(tab_click);

/* make page contents sortable */
$(".tab").sortable();;

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

    new_tab.bind("click",tab_click);

    return false;
});



});

