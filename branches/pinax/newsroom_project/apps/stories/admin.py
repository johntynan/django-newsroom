from django.contrib import admin
from stories.models import Story, RelatedContent, Page

class RelatedContentInline(admin.TabularInline):
    model = RelatedContent
    extra = 1

class PageInline(admin.StackedInline):
    model = Page
    extra = 2

class StoryAdmin(admin.ModelAdmin):
    search_fields = ['headline','slug','summary']
    prepopulated_fields = {'slug': ('headline',)}

    list_display = ('headline','creation_date',
        'modification_date' )
    list_display_links = ('headline',)
    list_filter = ('status', 'modification_date')
    filter_horizontal = ('sites',)

    inlines = (PageInline, RelatedContentInline)

admin.site.register(Story,StoryAdmin)


