from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from features.models import * 
from features.forms import *

def front(request):
    return render_to_response(
              'features/front.html',
              {},
              context_instance=RequestContext(request))

def feature_add(request):
    """
    Process a new feature submission.
    """

    if request.method == "POST":
        form = FeatureForm(request.POST)
        if form.is_valid():
            feature = form.save(commit=False)
            feature.submitter = request.user
            feature.save()
            request.user.message_set.create(
                message='Your feature has been submitted.  Thank you.')
            return HttpResponseRedirect(request.user.get_profile().get_absolute_url())

    else:
        #form = FeatureForm(user=request.user)
        form = FeatureForm()

    return render_to_response(
              'features/feature_add.html',
              {'form':form},
              context_instance=RequestContext(request))

def feature_list(request):
    """
    Get index of features.
    """

    features = Feature.objects.all()

    return render_to_response(
              'features/feature_list.html',
              {'features':features},
              context_instance=RequestContext(request))

