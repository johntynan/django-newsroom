"""
Constants for the multimedia app
"""

MEDIA_TYPE_IMAGE = 'image'
MEDIA_TYPE_VIDEO = 'video'

MEDIA_TYPES = (
    (MEDIA_TYPE_IMAGE,'Image',),
    (MEDIA_TYPE_VIDEO,'Video',),
)

MEDIA_STATUS_DRAFT = 'D'
MEDIA_STATUS_PUBLISHED = 'P'
MEDIA_STATUS_ARCHIVED = 'A'
MEDIA_STATUS_CHOICES = (
    (MEDIA_STATUS_DRAFT,'Draft',),
    (MEDIA_STATUS_PUBLISHED,'Published',),
    (MEDIA_STATUS_ARCHIVED,'Archived',),
)