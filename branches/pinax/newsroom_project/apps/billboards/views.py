from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string

from promos.models import Promo, PromoImage
from billboards.models import Billboard
from billboards.forms import BillboardForm

@login_required
def billboard_list(request):
    """
    Get index of billboard files.
    """

    billboard_list = Billboard.objects.all()
    return render_to_response(
            'billboards/billboard_list.html',
            {'billboards_billboard_list': billboard_list},              
            context_instance=RequestContext(request))
    
def billboard_detail(request, id):
    billboard_detail = Billboard.objects.get(id=id)
    main_promo = billboard_detail.main_promo
    promo_image = PromoImage.objects.filter(promo=main_promo)
    

    return render_to_response(
            'billboards/billboard_detail.html',{
                'billboards_billboard_detail': billboard_detail,
                'promo_image': promo_image
             }, context_instance=RequestContext(request))

@login_required
def billboard_add(request):
    """
    Process a new Billboard project.
    """

    if request.method == "POST":
        form = BillboardForm(request.POST)
        if form.is_valid():
            form.save()
            request.user.message_set.create(
                message='Your Billboard project been added.  Thank you.')
            return HttpResponseRedirect(reverse('billboards_billboard_list'))

    else:
        form = BillboardForm()

    return render_to_response(
              'billboards/billboard_add.html',
              {'form':form},
              context_instance=RequestContext(request))
 


