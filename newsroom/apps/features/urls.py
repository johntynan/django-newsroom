from django.conf.urls.defaults import *
from django.contrib import admin

urlpatterns = patterns('',

    url(r'^$', 
        'features.views.feature_list',
        name="features_feature_list"),

    url(r'^add$', 
        'features.views.feature_add',
        name="features_feature_add"),

)
