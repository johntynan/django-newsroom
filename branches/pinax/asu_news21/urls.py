from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^asu_news21/', include('asu_news21.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    (r'^$', direct_to_template, {'template': 'front.html'}),
    (r'^stories/', include('stories.urls')),
    (r'^profiles/', include('basic_profiles.urls')),
    (r'^topics/',include('topics.urls')),
    (r'^account/', include('account.urls')),
    (r'^photos/',include('photos.urls')),
    (r'^videos/',include('videos.urls')),
)

if settings.SERVE_MEDIA:
    urlpatterns += patterns('', 
        (r'^site_media/(?P<path>.*)$', 'staticfiles.views.serve')
    )
