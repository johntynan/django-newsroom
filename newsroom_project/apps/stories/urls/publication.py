# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('stories.views.publication',
    #- PUBLIC  -
    #diplay story
    url('^(?P<story_id>[\d+])/(?P<slug>[\d\w-]+)/$','story',name="stories_show_story"),
    url('^$','stories_show',name="stories_show_story"),
)

