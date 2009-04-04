from django.conf.urls.defaults import *

urlpatterns = patterns('newsroom.views',
    url('^story/add/$','add_story',name='stories_add_story'),
    url('^story/edit/$','add_story',name='stories_story_detail'),
)

