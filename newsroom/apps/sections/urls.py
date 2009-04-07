from django.conf.urls.defaults import *

urlpatterns = patterns('stories.views',
    url('^section/add/$','add_section',name='stories_add_section'),
    url('^section/(?P<section_id>\d+)/edit/$','section_detail',name='sections_section_detail'),
)

