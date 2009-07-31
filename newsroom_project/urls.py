from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.views.generic.simple import redirect_to, direct_to_template
from django.views.generic.list_detail import object_list

from promos.models import PromoBillboard

from account.openid_consumer import PinaxConsumer

from authsub import *

admin.autodiscover()

info_dict = {
    'queryset':PromoBillboard.objects.all().order_by('title'),
    "template_name":"dashboard.html",
    "extra_context" : {}

}

urlpatterns = patterns('',
    url('^$', redirect_to, {'url': '/promos/'}),
    url(r'^page/(?P<page>[0-9]+)/$', object_list, dict(info_dict)),
    url(r'^page/(?P<page>last)/$', object_list, dict(info_dict)),
    
    url(r'authsub_login/', direct_to_template, {"template": "authsub_login.html"}, name="authsub_login"),

    (r'^about/', include('about.urls')),
    (r'^account/', include('account.urls')),
    (r'^openid/(.*)', PinaxConsumer()),
    (r'^profiles/', include('basic_profiles.urls')),
    (r'^notices/', include('notification.urls')),
    (r'^announcements/', include('announcements.urls')),
#    (r'^projects/', include('projects.urls')),
#    (r'^bookmarks/', include('bookmarks.urls')),
    (r'^avatar/', include('avatar.urls')),
    (r'^promos/', include('promos.urls')),
    (r'^affiliates/', include('core.urls')),
    (r'^newsroom/',include('stories.urls.newsroom')),
    (r'^publication/',include('stories.urls.publication')),
    (r'^topics/',include('topics.urls')),
    (r'^videos/',include('videos.urls')),
    (r'^multimedia/',include('multimedia.urls')),
    (r'^page_layouts/',include('page_layouts.urls')),
    (r'^geotags/', include('geotags.urls')),
    (r'^feeds/', include('feeds.urls')),
    (r'^maps/', include('maps.urls')),
    (r'^flash/', include('flash.urls')),
    (r'^authsub/', include('authsub.urls')),
    
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),

    # handles /photos/ and /galleries/
    (r'', include('photologue.urls')),
)

if settings.SERVE_MEDIA:
    urlpatterns += patterns('', 
        (r'^site_media/(?P<path>.*)$', 'staticfiles.views.serve')
    )
