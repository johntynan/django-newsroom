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

    url(r'^(?P<promo_id>\d+)/image/$',
        'promo_image_list',
        name="promos_promo_image_list"),
    
    url(r'^(?P<promo_id>\d+)/link/$',
        'promo_link_list',
        name="promos_promo_link_list"),

    url(r'^(?P<promo_id>\d+)/link_add/$',
        'promo_link_add',
        name="promos_promo_link_add"),

    url(r'^(?P<promo_id>\d+)/date/$',
        'promo_date_list',
        name="promos_promo_date_list"),

    url(r'^(?P<promo_id>\d+)/date_add/$',
        'promo_date_add',
        name="promos_promo_date_add"),
            
    url(r'^(?P<promo_id>\d+)/point/$', 'promo_add_edit_geotag',
        {"form_class":PointForm, "geotag_class":Point,
         "template":"promos/promo_add_edit_point.html"}
        , name="promos_promo_add_edit_point"),

    url(r'^(?P<promo_id>\d+)/billboard/$',
        'promo_billboard_list',
        name="promos_promo_billboard_list"),

    url(r'^(?P<promo_id>\d+)/billboard_add/$',
        'promo_billboard_add',
        name="promos_promo_billboard_add"),

    url(r'^(?P<promo_id>\d+)/billboard_detail/(?P<billboard_id>\d+)$',
        'promo_billboard_detail',
        name="promos_promo_billboard_detail"),

    url(r'(?P<promo_id>\d+)/link/(?P<link_id>\d+)/edit/$',
        'promo_link_edit',
        name='promos_promo_link_edit'),

    url(r'(?P<promo_id>\d+)/image/(?P<image_id>\d+)/edit/$',
        'promo_image_edit',
        name='promos_promo_image_edit'),

    url(r'(?P<promo_id>\d+)/date/(?P<date_id>\d+)/edit/$',
        'promo_date_edit',
        name='promos_promo_date_edit'),

    url(r'(?P<promo_id>\d+)/billboard/(?P<billboard_id>\d+)/edit/$',
        'promo_billboard_edit',
        name='promos_promo_billboard_edit'),
    
    url(r'(?P<promo_id>\d+)/billboard/(?P<billboard_id>\d+)/delete/$',
        'promo_billboard_delete',
        name='promos_promo_billboard_delete'),

)

'''
    url(r'^delete/$', 
        'promo_delete',
        name="promos_promo_delete"),

    url(r'(?P<promo_id>\d+)/link/(?P<link_id>\d+)/delete/$',
        'promo_link_delete',
        name='promos_promo_link_delete'),

    url(r'(?P<promo_id>\d+)/image/(?P<image_id>\d+)/delete/$',
        'promo_image_delete',
        name='promos_promo_image_delete'),

    url(r'(?P<promo_id>\d+)/date/(?P<date_id>\d+)/dlete/$',
        'promo_date_delete',
        name='promos_promo_date_delete'),


'''
