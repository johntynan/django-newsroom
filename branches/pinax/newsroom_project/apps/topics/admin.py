from django.contrib import admin
from topics.models import Topic
from topics.models import TopicPath
from topics.models import TopicImage

admin.site.register(Topic)
admin.site.register(TopicPath)
admin.site.register(TopicImage)