from django.conf.urls.defaults import *
from flash.models import Flash, FlashArchive
from flash.forms import FlashForm, FlashArchiveForm

urlpatterns = patterns('flash.views',
    url(r'^$',
        'flash_list',
        name="flash_flash_list"),
    url(r'^(?P<id>\d+)/$', 
        'flash_detail',
        name='flash_flash_detail'),
    url(r'^add/$',
        'flash_add',
        name='flash_flash_add'),
    url(r'^archive_add/$', 
        'flash_archive_add',
        name="flash_flash_archive_add"), 
)
