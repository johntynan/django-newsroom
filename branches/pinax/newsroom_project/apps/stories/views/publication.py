# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, Template, Context
from django.contrib.auth.decorators import login_required
from django.http import HttpResponsePermanentRedirect, HttpResponseNotFound
from django.core.urlresolvers import reverse

from stories.models import Story, Page
from stories.constants import STORY_STATUS_DRAFT, STORY_STATUS_PUBLISHED


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
    Support URL /stories/<id>/<token>/
    """
    story = get_object_or_404(Story,id=story_id)
    return HttpResponsePermanentRedirect(
                reverse('stories_page_preview_pub',
                        args=[story.id, story.slug, 1, token]))

def page_detail(request, story_id, slug, pagenum, token=None):
    """
    Render a page of the story.  Also supports preview via a token.
    """

    try:
        story = Story.on_site.get(pk=story_id)
        if token and token == story.token:
            # also redirect people using a token on a published page
            if story.is_published():
                return HttpResponsePermanentRedirect(
                        reverse('stories_page_detail_pub',
                                args=[story.id, story.slug, pagenum]))
        else:
            story = Story.on_site.get(
                        pk=story_id, 
                        status=STORY_STATUS_PUBLISHED)

    except Story.DoesNotExist:
        return HttpResponseNotFound()

    page = get_object_or_404(Page, story=story, pagenum=pagenum)

    # check that slug is not outdated
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

