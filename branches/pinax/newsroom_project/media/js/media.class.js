// class widget.media
widget.media = new Object();

widget.media.__jquery_obj = '';


widget.media.id = function(value){if (value)this.__media_id = value;return this.__media_id; }
widget.media.__id = '';

widget.media.caption = function(value){if (value)this.__caption = value;return this.__caption; }
widget.media.__caption = '';

widget.media.classes = function(value){if (value != undefined)this.__classes = value;return this.__classes; }
widget.media.__classes = '';

widget.media.template_tag = function(){
    return '{% media_insert '+ widget.media.id() + ' "'+ widget.media.caption() +'" "'+ widget.media.classes() +'" %}'
}


/* loads properties from jquery_obj html block */
widget.media.load = function(jquery_obj)
{
    widget.media.__jquery_obj = jquery_obj;
    widget.media.template_tag(widget.media.__jquery_obj.children(".widget-code").text());

    $.each($("#media-align option"),function(i,val){
        $("#media-tag .widget-block").removeClass($(val).val());
    });

    /* get caption */
    re = new RegExp('{% media_insert ([0-9]{0,}) "([a-zA-Z]{0,})" "([a-zA-Z-_]{0,})" %}');
    var matches = widget.media.__jquery_obj.children(".widget-code").text().match(re);
    widget.media.id(matches[1]);
    widget.media.caption(matches[2]);
    widget.media.classes(matches[3]);
};


/* public call to bring up the editor screen */
widget.media.edit = function()
{
    var url = widget.media.__jquery_obj.children(".widget-options").children(".widget-edit").attr("href");
    widget.lightbox(url,widget.media.__edit_callback);
    return false;
};

/* returns selected option from align select box */
widget.media.__check_align = function()
{
    $("#media-align option[value="+ widget.media.classes()+"]").attr("selected","selected");
};



/*
callback for when media editor pop'ups
handles option clicks and save button
*/
widget.media.__edit_callback = function()
{
    widget.media.__jquery_obj.clone().appendTo("#media-tag");

    $("#widget-media-caption").val(widget.media.caption());
    $("#template-tag").val(widget.media.template_tag());

    widget.media.__check_align();

    $("#media-align").change(function(){
        console.log('changed');
        widget.media.classes($(this).children("option:selected").val());
        $("#template-tag").val(widget.media.template_tag());
    });

    /* change caption on template tag keyup event */
    $("#widget-media-caption").keyup(function(){
        widget.media.caption($(this).val());
        $("#template-tag").val(widget.media.template_tag());
    });

    $("#lb-block-save").click(function(){
        var img_src = $("#media-tag .widget-media-block img").attr("src");
        var img_tag = $("#media-tag .widget-code").text();

        widget.media.__jquery_obj.children("img").attr("src",img_src);
        widget.media.__jquery_obj.children(".widget-code").text(widget.media.template_tag());

        $.each($("#media-align option"),function(i,val){
            widget.media.__jquery_obj.removeClass($(val).val());
        });

        widget.media.__jquery_obj.addClass(widget.media.classes());

        tb_remove();
    });

};