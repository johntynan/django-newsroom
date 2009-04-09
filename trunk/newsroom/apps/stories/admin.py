from django.contrib import admin
from stories.models import Story,Page

class StoryAdmin(admin.ModelAdmin):
    search_fields = ['headline','slug','summary']
    prepopulated_fields = {'slug': ('headline',)}

admin.site.register(Story,StoryAdmin)
admin.site.register(Page)


