from django.conf.urls.defaults import *

urlpatterns = patterns('flash.views',
    #url(r'^$',
    #    'flash_list',
    #    name="flash_flashproject_list"),
    url(r'^(?P<id>\d+)/$', 
        'flashproject_detail',
        name='flash_flashproject_detail'),
    url(r'^add/$',
        'flashproject_add_edit',
        name='flash_flashproject_add'),
    url(r'^(?P<id>\d+)/edit/$', 
        'flashproject_add_edit',
        name='flash_flashproject_edit'),
)
