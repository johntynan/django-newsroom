from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.measure import D
from django.contrib.gis.shortcuts import render_to_kml
from django.contrib.gis.utils import GeoIP
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.simple import direct_to_template


from geotags.models import Point, Line, Polygon

def kml_feed(request, template="geotags/geotags.kml",
             geotag_class_name=None,content_type_name=None,
             object_id=None):
    """
    Return a KML feed of a particular geotag type : point, line, polygon
    This feed can be restricted by content_type and object_id.
    """
    geotag_class = ContentType.objects.get(name=geotag_class_name).model_class()
    if content_type_name:
        geotags = geotag_class.objects.filter(content_type__name=content_type_name)
    if object_id:
        geotags = geotags.filter(object_id=object_id)
    if object_id == None and content_type_name == None :
        geotags = geotag_class.objects.all()
    context = RequestContext(request, {
        'places' : geotags.kml(),
    })
    return render_to_kml(template,context_instance=context)


def kml_feed_map(request,template="geotags/view_kml_feed.html",
                 geotag_class_name=None, content_type_name=None):
    """
    Direct the user to a template with all the required parameters to render
    the KML feed on a google map.
    """
    if content_type_name:
        kml_feed = reverse("geotags-kml_feed_per_contenttype",
                           kwargs={
                            "geotag_class_name" : geotag_class_name,
                            "content_type_name" : content_type_name,
                            })
    else:
        kml_feed = reverse("geotags-kml_feed",kwargs={"geotag_class_name":geotag_class_name})


    extra_context = {
        "google_key" : settings.GOOGLE_MAPS_API_KEY,
        "kml_feed" : kml_feed
    }
    return direct_to_template(request,template=template,extra_context=extra_context)

