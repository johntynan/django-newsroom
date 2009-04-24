from django.conf.urls.defaults import *
from django.contrib.auth.models import User
from core import views

urlpatterns = patterns('',

    url('^$',
        views.affiliate_list,
        name='affiliate_list'),
       
    url(r'^add/$', 
        views.affiliate_add,
        name="affiliate_add"),

    url(r'^(?P<id>\d+)/edit/$',
        views.affiliate_edit,
        name='affiliate_edit'),

    url(r'^(?P<id>\d+)/$', 
        views.affiliate_detail,
        name="affiliate_detail"),

)

