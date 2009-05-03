 $(document).ready(function(){

    $(".tab-links a").click(function(){
        $(".tab-contents .tab").addClass("hidden");
        $("#" + $(this).attr("rel")).removeClass("hidden");

        $(".actions-block").addClass("hidden");
        $("#" + $(this).attr("rel") + "-actions").removeClass("hidden");

        $(".tab-links a").removeClass("active");
        $(this).addClass("active");
        return false;
    });

    $("#story-content").sortable();



 });

