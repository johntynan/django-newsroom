from django.conf.urls.defaults import *
from geotags.models import Point
from geotags.forms import PointForm

from maps.views import kml_feed_map_new, kml_feed_new

urlpatterns = patterns('',

    # KML feeds
    url(r'^kml_feed/(?P<geotag_class_name>[a-z]+)/(?P<content_type_name>[a-z ]+)/$',kml_feed_new,
        name="geotags-kml_feed_per_contenttype"),

    # KML Feeds visualiser
    url(r'^(?P<geotag_class_name>[a-z]+)/(?P<content_type_name>[a-z ]+)/$', kml_feed_map_new,
        name="geotags-kml_feed_map_per_contenttype"),

)
