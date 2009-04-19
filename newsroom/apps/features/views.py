from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponseRedirect
from features.models import Feature 
from features.forms import FeatureForm
from features.models import FeatureImage
from features.models import FeatureLink

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
                message='Your feature has been submitted.')
            return HttpResponseRedirect(reverse('features_feature_list'))

    else:
        form = FeatureForm()

    return render_to_response(
              'features/feature_add.html',
              {'form':form},
              context_instance=RequestContext(request))

def feature_edit(request, id):
    """
    Edit an existing feature.
    """
    feature = get_object_or_404(Feature, pk=id)
    
    if request.method == "POST":
        form = FeatureForm(request.POST, instance=feature)
        if form.is_valid():
            form.save()
            request.user.message_set.create(
                message='Your feature has been edited.')
            return HttpResponseRedirect(reverse('features_feature_list'))
    else:
        form = FeatureForm(instance=feature)        

    return render_to_response(
              'features/feature_edit.html',
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

def feature_detail(request, id):
    """
    Get feature details.
    """
    feature = Feature.objects.get(pk=id)
    feature_link = FeatureLink.objects.filter(feature=id)
    feature_image = FeatureImage.objects.filter(feature=id)

    return render_to_response(
              'features/feature_detail.html',{
              'feature_image': feature_image,
              'feature_link': feature_link,
              'feature': feature
             },
              context_instance=RequestContext(request))

