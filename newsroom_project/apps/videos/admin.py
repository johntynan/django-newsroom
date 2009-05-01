from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from videos.models import Video

class VideoAdmin(admin.ModelAdmin):
	list_display = ('title', 'pub_date', 'site', 'video', 'status','created_by', 'modified_by')
	list_filter = ('pub_date', 'site', 'status',)
	search_fields = ['title','summary']
	date_hierarchy = 'pub_date'
	prepopulated_fields = {'slug': ('title',)}
	
admin.site.register(Video, VideoAdmin)
