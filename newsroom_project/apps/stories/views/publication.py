# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, Template, Context
from django.contrib.auth.decorators import login_required

from stories.models import Story




@login_required
def story(request,slug):
    story = get_object_or_404(Story,slug=slug)
    pagenum = request.GET.get('p',1)
    page = story.get_page(1)

    #render the page content so that media tags are handled
    template = Template("{%% load media_tags %%}%s" %  page.content)
    content = template.render(Context())

    #TODO: get the template to use from the story

    #TODO: handle column breaks
    return render_to_response('stories/display_page_content.html',
                              locals(),
                              context_instance=RequestContext(request))

#TODO: add authentication check decorators

def stories_show(request):
    stories = Story.objects.published()
    return render_to_response('stories/stories_show.html',locals(),context_instance=RequestContext(request))

