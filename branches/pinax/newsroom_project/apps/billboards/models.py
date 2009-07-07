from django.db import models
from promos.models import Promo

BILLBOARD_TYPE = (
    ('0', 'Billboard with Text Overlay'),
    ('1', 'Billboard with Text Below'),
    ('2', 'Composite Photo'),
)

HEADLINE_COLORS = (
    ('FFFFFF', 'White'),
    ('000000', 'Black'),
    ('C0C0C0', 'Grey'),
)

HEADLINE_ALIGN = (
    ('left', 'Left'),
    ('center', 'Center'),
    ('right', 'Right'),
)

class Billboard(models.Model):
    title = models.CharField(
                "Campaign",
                max_length=255)

    billboard_type = models.CharField(max_length=6, choices=BILLBOARD_TYPE)

    headline = models.CharField(max_length=225)

    headline_position_horizontal = models.CharField(max_length=4)

    headline_position_vertical = models.CharField(max_length=4)

    headline_width = models.CharField(max_length=4)

    headline_alignment = models.CharField(max_length=25, choices=HEADLINE_ALIGN)

    headline_color = models.CharField(max_length=6, choices=HEADLINE_COLORS)

    start_date = models.DateField(
                        "Billboard start date",
                        blank=True,
                        null=True,
                        help_text="Start Date for use on home page.")

    supporting_text = models.TextField(blank=True)

    supporting_text_position_horizontal = models.CharField(max_length=4)

    supporting_text_position_vertical = models.CharField(max_length=4)

    supporting_text_width = models.CharField(max_length=4)

    supporting_text_alignment = models.CharField(max_length=25, choices=HEADLINE_ALIGN)

    supporting_text_color = models.CharField(max_length=6, choices=HEADLINE_COLORS)

    announcement = models.TextField(blank=True)

    main_promo = models.ForeignKey(
                Promo,
                help_text="Promo to be displayed in the main area.",)

    def __unicode__(self):
        return self.title

