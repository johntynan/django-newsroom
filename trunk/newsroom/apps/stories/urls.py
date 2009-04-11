from django.conf.urls.defaults import *

urlpatterns = patterns('stories.views',
    
    #- EDITIING -
    #list stories
    url('^$','story_list',name='stories_story_list'),
    #add story
    url('^story/add/$','add_story',name='stories_add_story'),
    #edit story
    url('^story/(?P<story_id>\d+)/edit/$','edit_story',name='stories_edit_story'),
    #story overview (page list)
    url('^story/(?P<story_id>\d+)/pages/$','story_pages',name='stories_story_pages'),
    #add page
    url(r'^story/(?P<story_id>\d+)/page/add/$','add_page',name='stories_add_page'),
    #edit page
    url(r'^story/page/(?P<page_id>\d+)/edit/$','edit_page',name='stories_edit_page'),
    #add media
    url(r'^story/(?P<story_id>\d+)/media/add/$','story_add_media',name='stories_story_add_media'),
    
    #- PUBLIC  -
    #diplay story
    url('^(?P<slug>[\d\w-]+)/$','story',name="stories_show_story"),
)

