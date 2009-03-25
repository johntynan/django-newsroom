from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Feature(models.Model):
    """
    A feature is use to define an object that will appear on the front
    page of the site for some period of time.

    last_featured is not editable and is managed by the front page
    view code.
    """
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    last_featured = models.DateTimeField(
                        editable=False,
                        blank=True,)
    expires = models.DateTimeField(blank=True,)
