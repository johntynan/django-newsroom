from django.conf.urls.defaults import *
from geotags.models import Point
from geotags.forms import PointForm

from geotags.views import kml_feed, kml_feed_map, kml_feeds_map

urlpatterns = patterns('',

    # KML Feeds visualiser
    url(r'^all/$', kml_feeds_map,
        name="geotags-kml_feeds_map"),
    url(r'^all/(?P<content_type_name>[a-z]+)/$', kml_feeds_map,
        name="geotags-kml_feeds_map_per_contenttype"),
    url(r'^(?P<geotag_class_name>[a-z]+)/$', kml_feed_map,
        name="geotags-kml_feed_map"),
    url(r'^(?P<geotag_class_name>[a-z]+)/(?P<content_type_name>[a-z ]+)/$', kml_feed_map,
        name="geotags-kml_feed_map_per_contenttype"),

    # KML Feeds visualiser
    url(r'^kml_feeds_map/all/$', kml_feeds_map,
        name="geotags-kml_feeds_map"),
    url(r'^kml_feeds_map/all/(?P<content_type_name>[a-z]+)/$', kml_feeds_map,
        name="geotags-kml_feeds_map_per_contenttype"),

    url(r'^kml_feed_map/(?P<geotag_class_name>[a-z]+)/$', kml_feed_map,
        name="geotags-kml_feed_map"),
    url(r'^kml_feed_map/(?P<geotag_class_name>[a-z]+)/(?P<content_type_name>[a-z ]+)/$', kml_feed_map,
        name="geotags-kml_feed_map_per_contenttype"),
)
