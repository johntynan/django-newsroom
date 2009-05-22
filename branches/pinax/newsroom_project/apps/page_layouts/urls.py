from django.conf.urls.defaults import *
from page_layouts import views

urlpatterns = patterns('',
        url(r'^$',
            views.page_layout_list,
            name='page_layout_list'),
        url(r'^(?P<id>\d+)/$', 
            views.page_layout_detail,
            name='page_layout_detail'),
        url('index.json',
            views.page_layout_list_json,
            name='page_layout_list_json'),
        url(r'^(?P<id>\d+).json', 
            views.page_layout_detail_json,
            name='page_layout_detail_json'),
)

"""

"""            

