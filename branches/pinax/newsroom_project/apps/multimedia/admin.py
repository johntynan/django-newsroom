from django.contrib import admin
from multimedia.models import Media

class MediaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Media, MediaAdmin)
