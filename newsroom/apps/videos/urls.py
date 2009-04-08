from django.conf import settings
from django.conf.urls.defaults import *
from tagging.views import tagged_object_list
from videos.models import Video 
from videos import views as vid_views
from django.contrib.sites.models import Site

info_dict = {
    'queryset': Video.objects.published(site = Site.objects.get_current()),
    'date_field': 'pub_date',
}

urlpatterns = patterns ('',
    url(r'tag/(?P<tag>[^/]+)/$', tagged_object_list,
     dict(model = Video, paginate_by = 10, allow_empty = True),
     name='videos_tag_index'),
    (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$',
     'django.views.generic.date_based.object_detail', 
     dict (info_dict, slug_field = 'slug')),
    (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 
     'django.views.generic.date_based.archive_day', info_dict),
    (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 
     'django.views.generic.date_based.archive_month', 
     info_dict),
    (r'^(?P<year>\d{4})/$', 
      'django.views.generic.date_based.archive_year', 
      dict(info_dict, make_object_list=True)),
    (r'^today/$', 'django.views.generic.date_based.archive_today', info_dict),
    url( r'^$', 'django.views.generic.date_based.archive_index', 
        dict(info_dict, template_object_name='object_list'),
        name="videos_index",),

    url( '^video/(?P<video_id>\d+)/(?P<slug>[-\w]+)/$',
         vid_views.video_detail,
         name="videos_video_detail",),

    url( '^video/add/$',
         vid_views.add_video,
         name='videos_add_video'),

    url( '^video/(?P<video_id>\d+)/edit/$',
         vid_views.video_detail,
         name='videos_video_detail'),

)
