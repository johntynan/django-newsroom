from datetime import date
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.html import conditional_escape as esc
from django.utils.safestring import mark_safe
from django.contrib.flatpages.models import FlatPage

from django.contrib.syndication.feeds import Feed
from django.utils import feedgenerator

from promos.forms import *
from promos.models import *

from promos.models import Promo
from topics.models import Topic, TopicPath, TopicImage

def promo_billboard_homepage(request):
    """
    Send ONLY the latest billboard to the homepage whose start date is less than or equal to today 
    """
    today = date.today()
    # billboards = PromoBillboard.objects.filter(start_date__lte=date.today()).order_by('?')[:1]
    billboards = PromoBillboard.objects.filter(start_date__lte=date.today()).order_by('-start_date')[:1]

    home1 = []
    home2 = []
    home3 = []
    status = []
    about_text = []
    flatpages = FlatPage.objects.all()
    for x in flatpages:
        if x.url == '/home1/':
            home1.append(x)
        elif x.url == '/home2/':
            home2.append(x)
        elif x.url == '/home3/':
            home3.append(x)
        elif x.url == '/status/':
            status.append(x)
        elif x.url == '/abouttext/':
            about_text.append(x)

    return render_to_response(
            'promo_billboard_homepage.html',{
            'billboards': billboards,
            'home1': home1,
            'home2': home2,
            'home3': home3,
            'status': status,
            'about_text':about_text,
             },
              context_instance=RequestContext(request))


def topics_list(request):
    topics_list = Topic.objects.all()
    return render_to_response(
            'topics_list.html',
            {'topics_list': topics_list},              
            context_instance=RequestContext(request))

def topic_detail(request, id):
    topics_list = Topic.objects.all()
    topic_detail = Topic.objects.get(id=id)
    topic_slug = topic_detail.slug
    sec_paths = TopicPath.objects.filter(topic__slug=topic_slug)
    promos = Promo.objects.filter(topic_path__in=sec_paths).distinct()
    topic_image = TopicImage.objects.filter(topic=id)
    
    return render_to_response(
            'topic_detail.html',{
                'topics_list': topics_list,
                'topic': topic_detail,
                'sec_paths': sec_paths,
                'promos': promos,
                'topic_image': topic_image
             }, context_instance=RequestContext(request))

def topic_feed(request, id):
    topics_list = Topic.objects.all()
    topic_detail = Topic.objects.get(id=id)
    topic_slug = topic_detail.slug
    sec_paths = TopicPath.objects.filter(topic__slug=topic_slug)
    promos = Promo.objects.filter(topic_path__in=sec_paths).distinct()
    topic_image = TopicImage.objects.filter(topic=id)

    feed_title = 'News21.com topic feed: ' + topic_detail.slug
    feed_link = 'http://news21.com/topic_detail/' + topic_detail.slug + '/'
    feed_description = topic_detail.slug
    
    return render_to_response(
            'topic_feed.rss',{
                'topic': topic_detail,
                'sec_paths': sec_paths,
                'promos': promos,
                'topic_image': topic_image,
                'feed_title': feed_title,
                'feed_link': feed_link,
                'feed_description': feed_description
             }, context_instance=RequestContext(request))
