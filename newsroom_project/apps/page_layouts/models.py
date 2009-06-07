# -*- coding: utf-8 -*-
from django.db import models
from photos.models import Photo

from django_inlines import inlines
from django.conf import settings

class PageLayout(models.Model):
    """
    PageLayouts are...

    """
    title = models.CharField(max_length=256)
    html = models.TextField()
    description = models.TextField()
    image = models.ImageField(upload_to="page_layouts")

    def __unicode__(self):
        return self.title


class TextWidget(models.Model):
    """
    This provides pre-formated texts to add to layouts
    """
    title = models.CharField(max_length=256)
    html = models.TextField()

    def __unicode__(self):
        return self.title



class ImageInline(inlines.TemplateInline):
    """
An inline that takes an image URL and returns the proper embed.

Examples::

<% image_widget http://www.news21.com/images/image37.png %>

The inluded template supports width and height arguments::

<% image_widget http://www.news21.com/images/image37.png width=300 height=150 %>

"""
    help_text = "takes an image URL and returns the proper embed.: http://www.news21.com/images/image37.png"
    inline_args = [
        dict(name='height', help_text="In pixels"),
        dict(name='width', help_text="In pixels"),
        ]

    def get_context(self):
        image_url = "%simages/widgets/blank.jpg" % settings.MEDIA_URL
        return { 'image_url': image_url }


inlines.registry.register('text_widget', inlines.inline_for_model(TextWidget))
inlines.registry.register('image_widget', ImageInline)