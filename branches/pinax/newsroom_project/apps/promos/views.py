from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponseRedirect
from promos.models import Promo, PromoImage, PromoLink
from promos.forms import PromoForm, ImageForm, LinkForm

from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

from django.forms.models import inlineformset_factory

if "mailer" in settings.INSTALLED_APPS:
    from mailer import send_mail
else:
    from django.core.mail import send_mail


def front(request):
    return render_to_response(
              'promos/front.html',
              {},
              context_instance=RequestContext(request))

def promo_add(request):
    """
    Process a new promo submission.
    """

    if request.method == "POST":
        form = PromoForm(request.POST)
        if form.is_valid():
            promo = form.save(commit=False)
            promo.submitter = request.user
            promo.save()
            to_user = [mail_tuple[1] for mail_tuple in settings.PROMO_MODERATORS]
            message = render_to_string('promos/promo_sent.txt', { 'user': request.user , 'current_site': Site.objects.get_current().domain, 'object': promo.id })
            send_mail("promo_submitted", message, settings.DEFAULT_FROM_EMAIL, to_user)
            request.user.message_set.create(
                message='Your promo has been submitted.')

            return HttpResponseRedirect(reverse('promos_promo_list'))

    else:
        form = PromoForm()

    return render_to_response(
              'promos/promo_add.html',
              {'form':form},
              context_instance=RequestContext(request))

def promo_edit(request, promo_id):
    """
    Edit an existing promo.
    """
    promo = get_object_or_404(Promo, pk=promo_id)

    PromoImageInlineFormSet = inlineformset_factory(Promo, PromoImage)   
    PromoLinkInlineFormSet = inlineformset_factory(Promo, PromoLink)  
    if request.method == "POST":
        formset1 = PromoImageInlineFormSet(request.POST, request.FILES, instance=promo)
        formset2 = PromoLinkInlineFormSet(request.POST, request.FILES, instance=promo)
        form = PromoForm(request.POST, instance=promo)
        if formset1.is_valid():
            formset1.save()
        if formset2.is_valid():
            formset2.save()
        if form.is_valid():
            form.save()
            request.user.message_set.create(
                message='Your promo has been edited.')
            return HttpResponseRedirect(reverse('promos_promo_list'))
    else:
        formset1 = PromoImageInlineFormSet(instance=promo)
        formset2 = PromoLinkInlineFormSet(instance=promo)
        form = PromoForm(instance=promo)        

    return render_to_response(
              'promos/promo_edit.html',
              ({'form': form,
              'formset1': formset1,
              'formset2': formset2,
              'promo':promo}),
              context_instance=RequestContext(request))

def promo_list(request):
    """
    Get index of promos.
    """

    promos = Promo.objects.all()
    promo_image = PromoImage.objects.all()

    return render_to_response(
                'promos/promo_list.html',{
                'promos': promos,
                'promo_image': promo_image,
                },
              context_instance=RequestContext(request))

def promo_detail(request, promo_id):
    """
    Get promo details.
    """
    promo = Promo.objects.get(pk=promo_id)
    # do not use this: promo_link = promo.promolink_set.all() - a pain for introspection.
    promo_link = PromoLink.objects.filter(promo=promo_id)
    promo_image = PromoImage.objects.filter(promo=promo_id)

    return render_to_response(
              'promos/promo_detail.html',{
              'promo': promo,
              'promo_link': promo_link,
              'promo_image': promo_image,
             },
              context_instance=RequestContext(request))
    
    
def promo_image_add(request, promo_id):
    """
    Process a new promo link submission.
    """

    if request.method == "POST":
        form = ImageForm(request.POST)
        if form.is_valid():
            form.save()
            request.user.message_set.create(
                message='Your promo image has been added.  Thank you.')
            return HttpResponseRedirect(reverse('promos_promo_list'))

    else:
        form = ImageForm()

    return render_to_response(
              'promos/promo_image_add.html',
              {'form':form},
              context_instance=RequestContext(request))

def promo_link_add(request, promo_id):
    """
    Process a new promo link submission.
    """

    if request.method == "POST":
        form = LinkForm(request.POST)
        if form.is_valid():
            form.save()
            request.user.message_set.create(
                message='Your promo link has been added.  Thank you.')
            return HttpResponseRedirect(reverse('promos_promo_list'))

    else:
        form = LinkForm()

    return render_to_response(
              'promos/promo_link_add.html',
              {'form':form},
              context_instance=RequestContext(request))

