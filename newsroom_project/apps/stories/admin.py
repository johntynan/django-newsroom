from django.contrib import admin
from stories.models import Story, RelatedContent, Page

class RelatedContentInline(admin.StackedInline):
    model = RelatedContent

class PageInline(admin.StackedInline):
    model = Page

class StoryAdmin(admin.ModelAdmin):
    search_fields = ['headline','slug','summary']
    prepopulated_fields = {'slug': ('headline',)}

    list_display = ('headline','creation_date',
        'modification_date' )
    list_display_links = ('headline',)
    list_filter = ('status',)
    filter_horzontal = ('sites',)

    inlines = (RelatedContentInline, PageInline)

admin.site.register(Story,StoryAdmin)


