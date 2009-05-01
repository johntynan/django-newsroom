from django.contrib import admin
from topics.models import Topic
from topics.models import TopicPath

admin.site.register(Topic)
admin.site.register(TopicPath)
