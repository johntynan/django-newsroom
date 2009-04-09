from django.conf.urls.defaults import *

urlpatterns = patterns('multimedia.views',
    url(r'^(?P<media_type>\w+)/browse/$','browse_by_type',name='multimedia_browse'),
)

