from django.conf.urls.defaults import *
from billboards.models import Billboard

urlpatterns = patterns('billboard.views',
    url(r'^$',
        'billboard_list',
        name="billboard_billboard_list"),
    url(r'^(?P<id>\d+)/$', 
        'billboard_detail',
        name='billboard_billboard_detail'),
    url(r'^add/$',
        'billboard_add',
        name='billboard_billboard_add'),
)
