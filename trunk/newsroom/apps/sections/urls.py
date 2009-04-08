from django.conf.urls.defaults import *
from sections import views

urlpatterns = patterns('',
        url(r'^$',
            views.sections_list,
            name='sections_sections_list'),
        url(r'^(?P<id>\d+)/$', 
            views.section_detail,
            name='sections_section_detail'),
        url(r'^sections/add/$',
            views.add_section,
            name='sections_add_section'),
        url(r'^sections/edit/$',
            views.edit_section,
            name='sections_edit_section'),
)

