from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from topics.models import TopicPath
from geotags.models import Point,Line, MultiLine, Polygon

"billboard", "thumbnail", "medium billboard", "original"
IMAGE_KIND_BILLBOARD = 'B'
IMAGE_KIND_THUMBNAIL = 'T'
IMAGE_KIND_MEDIUM = 'M'
IMAGE_KIND_ORIGINAL = 'O'
IMAGE_KIND_CHOICES = (
    (IMAGE_KIND_BILLBOARD,'Billboard'),
    (IMAGE_KIND_THUMBNAIL, 'Thumbnail'),
    (IMAGE_KIND_MEDIUM, 'Medium'),
    (IMAGE_KIND_ORIGINAL, 'Original'),
)

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

class Promo(models.Model):
    """
    A promo is use to define what will appear on the front page of the site
    for some period of time.

    When affiliates want a story or project syndicated through this site
    they submit a promo.  This is where some data gets saved for the 
    editor to sift through later and contruct a home page.
    """

    headline =  models.CharField(max_length=255)

    permalink = models.URLField(
                    "URL",
                    help_text="This should be the published link for the story or project you want promoted on news21.com. <br />e.g. http://newsinitiative.org/story/2007/06/18/drums_draw_strangers_to_bahai/")

    description = models.TextField(
                      "Summary / Nut Graph",
                      blank=True,
                      help_text="A short paragraph to describe the promo.",)
    # project = models.ManyToManyField(Project, blank=True)
    
    submitter = models.ForeignKey(
                    User,
                    related_name='promos_submitted',)
    authors = models.ManyToManyField(
                User,
                related_name='promos_authored',
                blank=True,
                help_text="The authors of the published work.")

    other_credits = models.TextField(
                      blank=True,
                      help_text="If the authors are not available in the list above please include their names here.")

    location = models.CharField(
                max_length=256,
                blank=True,
                help_text="City, State Country or Zipcode, Country." )

    
    topic_path = models.ManyToManyField(TopicPath, blank=True)

    relevance_begins = models.DateField(
                        "Suggested Relevance Begins",
                        blank=True,
                        null=True,
                        help_text="Start Date for use on home page.")
    relevance_ends = models.DateField(
                        "Relevance Ends",
                        blank=True,
                        null=True,
                        help_text="End Date for use on home page.")

    # last_promod is not editable and is managed by the front page
    # view code.
    last_promod = models.DateTimeField(
                        editable=False,
                        blank=True,
                        null=True)
    
    def __unicode__(self):
       return self.headline

    def get_absolute_url(self):
        return ('promos_promo_detail', 
                (), 
                { 'id': self.id })
    get_absolute_url = models.permalink(get_absolute_url)

    def get_geotags(self):
        geo_dict = {}
        geo_dict['point'] = Point.objects.filter(content_type=ContentType.objects.get_for_model(self.__class__()), object_id=self.id)
        geo_dict['line'] = Line.objects.filter(content_type=ContentType.objects.get_for_model(self.__class__()), object_id=self.id)
        geo_dict['multiline'] = MultiLine.objects.filter(content_type=ContentType.objects.get_for_model(self.__class__()), object_id=self.id)
        geo_dict['polygon'] = Polygon.objects.filter(content_type=ContentType.objects.get_for_model(self.__class__()), object_id=self.id)
        return geo_dict


class PromoDate(models.Model):
    """
    Links related to promo submissions.
    """
    title = models.CharField(max_length=200)
    desc = models.TextField('description',blank=True)
    promo_date = models.DateField(
                        "Promo Date",
                        help_text="Suggested date for showcasing a promo on the home page.")
    promo = models.ForeignKey(
                Promo,
                help_text='Suggested date for showcasing a promo on the home page.')

    def __unicode__(self):
        return self.title
    
class PromoLink(models.Model):
    """
    Links related to promo submissions.
    """
    title = models.CharField(max_length=200)
    url = models.URLField(verify_exists=False)
    desc = models.TextField('description',blank=True)
    promo = models.ForeignKey(
                Promo,
                help_text='Related links might be a blog post or other information related to how the piece was built, "behind the scenes", or just links related to the same topic.')

    def __unicode__(self):
        return self.title

class PromoImage(models.Model):
    attribution = models.CharField(_('attibution'), max_length=100)
    caption = models.CharField(_('caption'), max_length=100)
    image_kind =models.CharField(_('Image kind'),
        max_length=1,
        choices=IMAGE_KIND_CHOICES,
        default=IMAGE_KIND_BILLBOARD)
    image = models.ImageField(_('image'),
        upload_to='uploads/promos/%Y/%m/%d',
        max_length=255)
    promo = models.ForeignKey(
                Promo,
                help_text="Photos to help with featuring the piece.  The photos ideally are 16:9 or 4:3 aspect ratio and 1000px wide.  Scaling and thumbnails are handled automatically.")

    def __unicode__(self):
        return self.caption

class PromoBillboard(models.Model):
    title = models.CharField(
                "Campaign",
                max_length=255)

    billboard_type = models.CharField(max_length=6, choices=BILLBOARD_TYPE)

    headline = models.CharField(max_length=225)

    headline_position_horizontal = models.CharField(default=0,max_length=4)

    headline_position_vertical = models.CharField(default=0,max_length=4)

    headline_width = models.CharField(default=300,max_length=4)

    headline_alignment = models.CharField(max_length=25, choices=HEADLINE_ALIGN, default='Left')

    headline_color = models.CharField(max_length=6, choices=HEADLINE_COLORS, default='White')

    supporting_text = models.TextField(blank=True)

    supporting_text_position_horizontal = models.CharField(default=0, max_length=4)

    supporting_text_position_vertical = models.CharField(default=0, max_length=4)

    supporting_text_width = models.CharField(default=300, max_length=4)

    supporting_text_alignment = models.CharField(max_length=25, choices=HEADLINE_ALIGN, default='Right')

    supporting_text_color = models.CharField(max_length=6, choices=HEADLINE_COLORS, default='White')

    link = models.ManyToManyField(
                PromoLink,
                related_name='billboard_url',
                blank=True,
                help_text="Link to the story, related story or project that this billboard is promoting.  If blank, the main url that you submitted with your pitch will be promoted. ")

    image = models.ManyToManyField(
                PromoImage,
                blank=False,
                help_text="Image to appear on the home page.")

    promo = models.ForeignKey(
                Promo,
                help_text="Promo that this billboard is promoting.")


    start_date = models.DateField(
                        "Billboard start date",
                        blank=True,
                        null=True,
                        help_text="Start Date for use on home page.")


    def __unicode__(self):
        return self.title

