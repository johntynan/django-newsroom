from django.conf.urls.defaults import *

urlpatterns = patterns('stories.views',
    
    url('^$','story_list',name='stories_story_list'),
    url('^story/add/$','add_story',name='stories_add_story'),
    url('^story/(?P<story_id>\d+)/edit/$','edit_story',name='stories_edit_story'),
    
    url(r'^story/page/(?P<page_id>\d+)/edit/$','edit_page',name='stories_edit_page'),
    url(r'^story/page/(?P<page_id>\d+)/media/add/$','story_add_media',name='stories_story_add_media'),
    url('^(?P<slug>[\d\w-]+)/$','show_story',name="stories_show_story"),
)

