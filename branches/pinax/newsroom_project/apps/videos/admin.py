from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from videos.models import Video, VideoFrame

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_thumbnail_view', 'pub_date', 'video', 'created_by', 'modified_by',)
    list_filter = ('pub_date', )
    search_fields = ['title','summary']
    date_hierarchy = 'pub_date'
    prepopulated_fields = {'slug': ('title',)}

    def get_thumbnail_view(self, obj):
        return obj.frame.admin_thumbnail_view()
    get_thumbnail_view.allow_tags = True
    get_thumbnail_view.short_description = _('Thumbnail')


class VideoFrameAdmin(admin.ModelAdmin):
    list_display = ('image', 'admin_thumbnail_view')
    list_per_page = 10

admin.site.register(Video, VideoAdmin)
admin.site.register(VideoFrame, VideoFrameAdmin)

