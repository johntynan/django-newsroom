from django.conf.urls.defaults import *
from django.contrib import admin
from features import views

urlpatterns = patterns('',

    url(r'^$', 
        views.feature_list,
        name="features_feature_list"),

    url(r'^add/$', 
        views.feature_add_edit,
        name="features_feature_add"),

    url(r'^(?P<id>\d+)/edit/$',
        'features.views.feature_edit',
        name='features_feature_edit'),

    url(r'^(?P<id>\d+)/$', 
        views.feature_detail,
        name="features_feature_detail"),

    url(r'^(?P<id>\d+)/edit/$', 
        views.feature_add_edit,
        name="features_feature_edit"),

)
