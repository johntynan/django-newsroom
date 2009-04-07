from django.conf.urls.defaults import *

urlpatterns = patterns('stories.views',
    url('^story/add/$','add_story',name='stories_add_story'),
    url('^story/(?P<story_id>\d+)/edit/$','story_detail',name='stories_story_detail'),
    
    url('^(?P<slug>[\d\w-]+)/$','show_story',name="stories_show_story"),
)

