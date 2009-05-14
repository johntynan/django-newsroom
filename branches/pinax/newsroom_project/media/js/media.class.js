// class widget.image
widget.media = new Object();

widget.media.jquery_obj = '';


widget.media.id = function(value){if (value)this.__media_id = value;return this.__media_id; }
widget.media.__id = '';

widget.media.caption = function(value){if (value)this.__caption = value;return this.__caption; }
widget.media.__caption = '';

widget.media.classes = function(value){if (value)this.__classes = value;return this.__classes; }
widget.media.__classes = '';

/* template tag */
widget.media.template_tag = function(){
    return '{% media_insert '+ widget.media.id() + ' "'+ widget.media.caption() +'" "'+ widget.media.classes() +'" %}'
}

widget.media.load = function(jquery_obj)
{
    widget.media.jquery_obj = jquery_obj;
    widget.media.template_tag(widget.media.jquery_obj.children(".widget-code").text());

    /* get caption */
    re = new RegExp('{% media_insert ([0-9]{0,}) "([a-zA-Z]{0,})" "([a-zA-Z-_]{0,})" %}');
    var matches = widget.media.jquery_obj.children(".widget-code").text().match(re);
    widget.media.id(matches[1]);
    widget.media.caption(matches[2]);
    widget.media.classes(matches[3]);
};

// method
widget.media.edit = function()
{
    var url = widget.media.jquery_obj.children(".widget-options").children(".widget-edit").attr("href");
    widget.lightbox(url,widget.media.edit_callback);
    return false;
};

widget.media.check_align = function()
{
    $("#image-align option[value="+ widget.media.classes()+"]").attr("selected","selected");
};

widget.media.edit_callback = function()
{
    widget.media.jquery_obj.clone().appendTo("#image-tag");

    $("#widget-media-caption").val(widget.media.caption());
    $("#template-tag").val(widget.media.template_tag());

    widget.media.check_align();

    $("#image-align").change(function(){
        widget.media.classes($(this).children("option:selected").val());
        $("#template-tag").val(widget.media.template_tag());
    });

    /* change caption on template tag keyup event */
    $("#widget-media-caption").keyup(function(){
        widget.media.caption($(this).val());
        $("#template-tag").val(widget.media.template_tag());
    });

    $("#lb-block-save").click(function(){
        var img_src = $("#image-tag .widget-image-block img").attr("src");
        var img_tag = $("#image-tag .widget-code").text();

        widget.media.jquery_obj.children("img").attr("src",img_src);
        widget.media.jquery_obj.children(".widget-code").text(widget.media.template_tag());

        var class_options = $("#image-align option");

        $.each(class_options,function(i,val){
            widget.media.jquery_obj.removeClass($(val).val());
        });

        widget.media.jquery_obj.addClass(widget.media.classes());

        tb_remove();
    });

};