from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from topics.models import TopicPath
from geotags.models import Point,Line, MultiLine, Polygon

"billboard", "small", "medium", "original"
IMAGE_KIND_BILLBOARD = 'B'
IMAGE_KIND_SMALL = 'S'
IMAGE_KIND_MEDIUM = 'M'
IMAGE_KIND_ORIGINAL = 'O'
IMAGE_KIND_CHOICES = (
    (IMAGE_KIND_BILLBOARD,'Billboard - 700px x 360px'),
    (IMAGE_KIND_MEDIUM, 'Medium - 400px x 205px'),
    (IMAGE_KIND_SMALL, 'Small - 120px x 100px'),
    (IMAGE_KIND_ORIGINAL, 'Original'),
)

BILLBOARD_TYPE = (
    ('0', 'Billboard with Text Overlay'),
    ('1', 'Billboard Image with Link (No Text)'),
)

COLOR_TABLE = (
    ('#F0F8FF','ALICEBLUE'),
    ('#FAEBD7','ANTIQUEWHITE'),
    ('#00FFFF','AQUA'),
    ('#7FFFD4','AQUAMARINE'),
    ('#F0FFFF','AZURE'),
    ('#F5F5DC','BEIGE'),
    ('#FFE4C4','BISQUE'),
    ('#000000','BLACK'),
    ('#FFEBCD','BLANCHEDALMOND'),
    ('#0000FF','BLUE'),
    ('#8A2BE2','BLUEVIOLET'),
    ('#A52A2A','BROWN'),
    ('#DEB887','BURLYWOOD'),
    ('#5F9EA0','CADETBLUE'),
    ('#7FFF00','CHARTREUSE'),
    ('#D2691E','CHOCOLATE'),
    ('#FF7F50','CORAL'),
    ('#6495ED','CORNFLOWERBLUE'),
    ('#FFF8DC','CORNSILK'),
    ('#DC143C','CRIMSON'),
    ('#00FFFF','CYAN'),
    ('#00008B','DARKBLUE'),
    ('#008B8B','DARKCYAN'),
    ('#B8860B','DARKGOLDENROD'),
    ('#A9A9A9','DARKGRAY'),
    ('#006400','DARKGREEN'),
    ('#BDB76B','DARKKHAKI'),
    ('#8B008B','DARKMAGENTA'),
    ('#556B2F','DARKOLIVEGREEN'),
    ('#FF8C00','DARKORANGE'),
    ('#9932CC','DARKORCHID'),
    ('#8B0000','DARKRED'),
    ('#E9967A','DARKSALMON'),
    ('#8FBC8F','DARKSEAGREEN'),
    ('#483D8B','DARKSLATEBLUE'),
    ('#2F4F4F','DARKSLATEGRAY'),
    ('#00CED1','DARKTURQUOISE'),
    ('#9400D3','DARKVIOLET'),
    ('#FF1493','DEEPPINK'),
    ('#00BFFF','DEEPSKYBLUE'),
    ('#696969','DIMGRAY'),
    ('#1E90FF','DODGERBLUE'),
    ('#B22222','FIREBRICK'),
    ('#FFFAF0','FLORALWHITE'),
    ('#228B22','FORESTGREEN'),
    ('#FF00FF','FUCHSIA'),
    ('#DCDCDC','GAINSBORO'),
    ('#F8F8FF','GHOSTWHITE'),
    ('#FFD700','GOLD'),
    ('#DAA520','GOLDENROD'),
    ('#BEBEBE','GRAY'),
    ('#008000','GREEN'),
    ('#ADFF2F','GREENYELLOW'),
    ('#F0FFF0','HONEYDEW'),
    ('#FF69B4','HOTPINK'),
    ('#CD5C5C','INDIANRED'),
    ('#4B0082','INDIGO'),
    ('#FFFFF0','IVORY'),
    ('#F0D58C','KHAKI'),
    ('#E6E6FA','LAVENDER'),
    ('#FFF0F5','LAVENDERBLUSH'),
    ('#7CFC00','LAWNGREEN'),
    ('#FFFACD','LEMONCHIFFON'),
    ('#ADD8E6','LIGHTBLUE'),
    ('#F08080','LIGHTCORAL'),
    ('#E0FFFF','LIGHTCYAN'),
    ('#FAFAD2','LIGHTGOLDENRODYELLOW'),
    ('#90EE90','LIGHTGREEN'),
    ('#D3D3D3','LIGHTGREY'),
    ('#FFB6C1','LIGHTPINK'),
    ('#FFA07A','LIGHTSALMON'),
    ('#20B2AA','LIGHTSEAGREEN'),
    ('#87CEFA','LIGHTSKYBLUE'),
    ('#778899','LIGHTSLATEGRAY'),
    ('#B0C4DE','LIGHTSTEELBLUE'),
    ('#FFFFE0','LIGHTYELLOW'),
    ('#00FF00','LIME'),
    ('#32CD32','LIMEGREEN'),
    ('#FAF0E6','LINEN'),
    ('#FF00FF','MAGENTA'),
    ('#800000','MAROON'),
    ('#66CDAA','MEDIUMAQUAMARINE'),
    ('#0000CD','MEDIUMBLUE'),
    ('#BA55D3','MEDIUMORCHID'),
    ('#9370DB','MEDIUMPURPLE'),
    ('#3CB371','MEDIUMSEAGREEN'),
    ('#7B68EE','MEDIUMSLATEBLUE'),
    ('#00FA9A','MEDIUMSPRINGGREEN'),
    ('#48D1CC','MEDIUMTURQUOISE'),
    ('#C71585','MEDIUMVIOLETRED'),
    ('#191970','MIDNIGHTBLUE'),
    ('#F5FFFA','MINTCREAM'),
    ('#FFE4E1','MISTYROSE'),
    ('#FFE4B5','MOCCASIN'),
    ('#FFDEAD','NAVAJOWHITE'),
    ('#000080','NAVY'),
    ('#FDF5E6','OLDLACE'),
    ('#808000','OLIVE'),
    ('#6B8E23','OLIVEDRAB'),
    ('#FFA500','ORANGE'),
    ('#FF4500','ORANGERED'),
    ('#DA70D6','ORCHID'),
    ('#EEE8AA','PALEGOLDENROD'),
    ('#98FB98','PALEGREEN'),
    ('#AFEEEE','PALETURQUOISE'),
    ('#DB7093','PALEVIOLETRED'),
    ('#FFEFD5','PAPAYAWHIP'),
    ('#FFDAB9','PEACHPUFF'),
    ('#CD853F','PERU'),
    ('#FFC0CB','PINK'),
    ('#DDA0DD','PLUM'),
    ('#B0E0E6','POWDERBLUE'),
    ('#800080','PURPLE'),
    ('#FF0000','RED'),
    ('#BC8F8F','ROSYBROWN'),
    ('#4169E1','ROYALBLUE'),
    ('#8B4513','SADDLEBROWN'),
    ('#FA8072','SALMON'),
    ('#F4A460','SANDYBROWN'),
    ('#2E8B57','SEAGREEN'),
    ('#FFF5EE','SEASHELL'),
    ('#A0522D','SIENNA'),
    ('#C0C0C0','SILVER'),
    ('#87CEEB','SKYBLUE'),
    ('#6A5ACD','SLATEBLUE'),
    ('#708090','SLATEGRAY'),
    ('#FFFAFA','SNOW'),
    ('#00FF7F','SPRINGGREEN'),
    ('#4682B4','STEELBLUE'),
    ('#D2B48C','TAN'),
    ('#008080','TEAL'),
    ('#D8BFD8','THISTLE'),
    ('#FF6347','TOMATO'),
    ('#40E0D0','TURQUOISE'),
    ('#EE82EE','VIOLET'),
    ('#F5DEB3','WHEAT'),
    ('#FFFFFF','WHITE'),
    ('#F5F5F5','WHITESMOKE'),
    ('#FFFF00','YELLOW'),
    ('#9ACD32','YELLOWGREEN'),
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
                help_text="City, State, Country or ZIP code, Country." )

    
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
    title = models.CharField("Relevancy / Description",max_length=200)
    description = models.TextField('Explanation',blank=True)
    start_date = models.DateField(
                        "Start Date",
                        help_text="Suggested start date for showcasing a promo on the home page.")
    end_date = models.DateField(
                        "End Date",
                        blank=True,
                        null=True,
                        help_text="Suggested end date for showcasing a promo on the home page.")
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
    desc = models.TextField('description',
            blank=True,
            help_text="Please provide any related links that might richly supplement the main package/story featured with this promo submission.  They could be from your incubator or another.")

    promo = models.ForeignKey(
                Promo,
                help_text='Related links might be a blog post or other information related to how the piece was built, "behind the scenes", or just links related to the same topic.')

    def __unicode__(self):
        return self.title

class PromoImage(models.Model):
    attribution = models.CharField(_('Credit'), max_length=100)
    caption = models.CharField(_('Description / Alt Tag'), max_length=100)
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

    headline_position_horizontal = models.CharField(default=100,max_length=4)

    headline_position_vertical = models.CharField(
                            default=100,
                            max_length=4,
                            help_text="Headlines are relative from the the top left of the image.")

    headline_width = models.CharField(default=300,max_length=4)

    headline_alignment = models.CharField(max_length=25, choices=HEADLINE_ALIGN, default='Left')

    headline_color = models.CharField(max_length=25, choices=COLOR_TABLE, default='#FFFFFF')

    supporting_text = models.TextField(blank=True)

    supporting_text_position_horizontal = models.CharField(default=0, max_length=4)

    supporting_text_position_vertical = models.CharField(
                            default=-200,
                            max_length=4,
                            help_text="Supporting text is relative from the the bottom left of the image.")

    supporting_text_width = models.CharField(default=300, max_length=4)

    supporting_text_alignment = models.CharField(max_length=25, choices=HEADLINE_ALIGN, default='Left')

    supporting_text_color = models.CharField(max_length=25, choices=COLOR_TABLE, default='#FFFFFF')

    link = models.ForeignKey(
                PromoLink,
                related_name='billboard_url',
                blank=True,
                null=True,
                help_text="Link to the story, related story or project that this billboard is promoting.  If blank, the main url that you submitted with your pitch will be promoted. ")

    image = models.ForeignKey(
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
    
    def get_absolute_url(self):
        return ('promos_promo_billboard_detail', 
                (), 
                {'promo_id': self.promo.id,
                 'billboard_id': self.id })
    get_absolute_url = models.permalink(get_absolute_url)


