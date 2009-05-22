# -*- coding: utf-8 -*-
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, Template, Context
from django.contrib.auth.decorators import login_required
from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse

from stories.models import Story, Page
from stories.constants import STORY_STATUS_DRAFT


def story_detail(request, story_id, slug=None):
    """
    Support URL /stories/<id>/ and /stories/<id>/<slug>/
    Our permalinks must specific a page, since stories always have pages.
    So this always redirects to page detail url.
    """

    story = get_object_or_404(Story,id=story_id)
    return HttpResponsePermanentRedirect(
                reverse('stories_page_detail_pub',
                        args=[story.id, story.slug, 1]))

def story_preview(request, story_id, token):
    """
    Support URL /stories/<id>/<TOKEN>
    """
    print  "coucou we are in"

    story = get_object_or_404(Story,id=story_id)
    page=1
    if not (story.token == token and story.status == STORY_STATUS_DRAFT):
        raise Http404

    return render_to_response(
                'stories/publication/page_detail.html',
                {'page':page,
                'story':story,},
                context_instance=RequestContext(request))


def page_detail(request, story_id, slug, pagenum):
    """
    Each page has a permalink.
    """

    story = get_object_or_404(Story,id=story_id)
    page = get_object_or_404(Page, story=story, pagenum=pagenum)

    if slug != story.slug:
        return HttpResponsePermanentRedirect(
                    reverse('stories_page_detail_pub',
                            args=[story.id, story.slug, pagenum]))
        
    return render_to_response(
                'stories/publication/page_detail.html',
                {'page':page,
                'story':story,},
                context_instance=RequestContext(request))

def story_list(request):
    stories = Story.objects.published()
    return render_to_response(
                'stories/publication/story_list.html',
                locals(),
                context_instance=RequestContext(request))

