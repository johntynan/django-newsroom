from django.conf.urls.defaults import *
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'features.views.front'),
    url(r'^add$', 
        'features.views.feature_add',
        name="features_feature_add"),
)
