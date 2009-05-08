from django.conf.urls.defaults import *

urlpatterns = patterns('multimedia.views',
    # also serve requests that only provide the media id
    (r'^(?P<media_id>\d+)/$','detail',),
    url(r'^(?P<media_id>\d+)/edit/$','edit',name='multimedia_edit'),
    url(r'^(?P<media_id>\d+)/preview/$','preview',name='multimedia_preview'),
    url(r'^(?P<media_id>\d+)/(?P<slug>[\w-]+)/$','detail',name='multimedia_detail'),
    url(r'^browse/$','browse',name='multimedia_browse'),
    url(r'^(?P<media_type>\w+)/browse/$','browse_by_type',name='multimedia_browse_type'),
    url(r'^(?P<media_type>\w+)/add/$','add_by_type',name='multimedia_add'),
)

