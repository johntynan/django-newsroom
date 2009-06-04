from django.conf.urls.defaults import *
from geotags.models import Point
from geotags.forms import PointForm

from geotags.views import kml_feed, kml_feed_map, kml_feeds_map

urlpatterns = patterns('',

    # KML feeds
    url(r'(?P<geotag_class_name>[a-z]+)/(?P<content_type_name>[a-z ]+).kml',kml_feed,
        name="geotags-kml_feed_per_contenttype"),
)
