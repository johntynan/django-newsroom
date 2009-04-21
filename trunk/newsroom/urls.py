from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^newsroom/', include('newsroom.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #(r'^admin/', include(admin.site.urls)),
    (r'^admin/(.*)', admin.site.root),
    (r'^people/', include('my_profiles.urls')),
    url(r'^$', 'features.views.front', name="features_front"),
    (r'^features/', include('features.urls')),

    url(r'^accounts/register/$',
        'my_profiles.views.register',
        name='my_profiles_register'),

    url(r'^accounts/password/reset/$',
        'my_profiles.views.password_reset',
        name='my_profiles_password_reset'),

    url(r'^activate/(?P<activation_key>\w+)/$',
        'my_profiles.views.activate',
        name='my_profiles_activate'),

    (r'^accounts/', include('registration.urls')),

    # redirect /users/ so user.get_absolute_url() still works if we need it
    ( r'^users/(?P<user>\w+)/$', 
      'django.views.generic.simple.redirect_to', 
      {'url':'/people/%(user)s/'} ),
    
    (r'^stories/',include('stories.urls')),

    (r'^sections/',include('sections.urls')),

    (r'^videos/',include('videos.urls')),

    (r'^multimedia/',include('multimedia.urls')),
    
    (r'', include('photologue.urls')),
    
    (r'^features/', include('features.urls')),

    (r'^comments/', include('django.contrib.comments.urls')), 
    
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (
            r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}
        ),
    )

