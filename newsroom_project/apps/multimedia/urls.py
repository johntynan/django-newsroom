from django.conf.urls.defaults import *

urlpatterns = patterns('multimedia.views',
    url(r'^(?P<media_id>\d+)/(?P<slug>[\w-]+)/$','detail',name='multimedia_detail'),
    # also serve requests that only provide the media id
    (r'^(?P<media_id>\d+)/$','detail',),
    url(r'^browse/$','browse',name='multimedia_browse'),
    url(r'^(?P<media_type>\w+)/browse/$','browse_by_type',name='multimedia_browse_type'),
    url(r'^(?P<media_type>\w+)/add/$','add_by_type',name='multimedia_add'),
)

