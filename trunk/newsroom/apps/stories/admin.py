from django.contrib import admin
from newsroom.stories.models import Story,Page,Media

admin.site.register(Story)
admin.site.register(Page)
admin.site.register(Media)

