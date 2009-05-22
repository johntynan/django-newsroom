# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

# Public Views

urlpatterns = patterns('stories.views.publication',

    ('^(?P<story_id>[\d+])/$','story_detail'),

    url('^(?P<story_id>[\d+])/(?P<slug>[\d\w-]+)/$',
        'story_detail',
        name="stories_story_detail_pub"),

    url('^(?P<story_id>[\d+])/(?P<slug>[\d\w-]+)/page/(?P<pagenum>[\d+])/$',
        'page_detail',
        name="stories_page_detail_pub"),
    
    url('^$','story_list',name="stories_story_list_pub"),

)

