from django.conf.urls.defaults import *
from billboards.models import Billboard

urlpatterns = patterns('billboards.views',
    url(r'^$',
        'billboard_list',
        name="billboards_billboard_list"),
    url(r'^(?P<id>\d+)/$', 
        'billboard_detail',
        name='billboards_billboard_detail'),
    url(r'^add/$',
        'billboard_add',
        name='billboards_billboard_add'),
)
