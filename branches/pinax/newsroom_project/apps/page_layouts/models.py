# -*- coding: utf-8 -*-
from django.db import models
from photos.models import Photo

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


class ImageWidget(models.Model):
    """
    This provides specific image sizes to add to layouts
    """
    title = models.CharField(max_length=256)
    image = models.ImageField(upload_to="page_layouts/widgets")

    def __unicode__(self):
        return self.title

