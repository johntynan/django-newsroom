from django.conf.urls.defaults import *
from geotags.models import Point
from geotags.forms import PointForm

from geotags.views import kml_feed, kml_feed_map, kml_feeds_map

urlpatterns = patterns('promos.views',

    url(r'^$',
        'promo_list',
        name="promos_promo_list"),

    url(r'^add/$', 
        'promo_add',
        name="promos_promo_add"),

    url(r'^(?P<promo_id>\d+)/edit/$',
        'promo_edit',
        name='promos_promo_edit'),

    url(r'^(?P<promo_id>\d+)/$',
        'promo_detail',
        name="promos_promo_detail"),
    
    url(r'^(?P<promo_id>\d+)/image_add/$',
        'promo_image_add',
        name="promos_promo_image_add"),    

    url(r'^(?P<promo_id>\d+)/link_add/$',
        'promo_link_add',
        name="promos_promo_link_add"),
    url(r'^(?P<promo_id>\d+)/point/$', 'promo_add_edit_geotag',
        {"form_class":PointForm, "geotag_class":Point,
         "template":"promos/promo_add_edit_point.html"}
        , name="promos_promo_add_edit_point"),
    
    
)
