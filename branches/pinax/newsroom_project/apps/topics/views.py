from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext,Context, loader

from promos.models import Promo
from topics.forms import TopicForm, TopicPathForm, TopicImageForm
from topics.models import Topic,TopicPath, TopicImage

from django.forms.models import inlineformset_factory

@login_required
def topics_list(request):
    topics_list = Topic.objects.all()
    return render_to_response(
            'topics/topics_list.html',
            {'topics_list': topics_list},              
            context_instance=RequestContext(request))

@login_required
def topic_detail(request, id):
    topic_detail = Topic.objects.get(id=id)
    topic_slug = topic_detail.slug
    sec_paths = TopicPath.objects.filter(topic__slug=topic_slug)
    promos = Promo.objects.filter(topic_path__in=sec_paths).distinct()
    topic_image = TopicImage.objects.filter(topic=id)
    
    return render_to_response(
            'topics/topic_detail.html',{
                'topic': topic_detail,
                'sec_paths': sec_paths,
                'promos': promos,
                'topic_image': topic_image
             }, context_instance=RequestContext(request))

@login_required
def topics_add(request):
    """
    Process a new topic submission.
    """

    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            request.user.message_set.create(
                message='Your topic has been added.  Thank you.')
            return HttpResponseRedirect(reverse('topics_topic_list'))

    else:
        #form = TopicForm(user=request.user)
        form = TopicForm()

    return render_to_response(
              'topics/topic_add.html',
              {'form':form},
              context_instance=RequestContext(request))

@login_required
def topic_edit(request, id):
    """
    Edit an existing topic.
    """
    topic = Topic.objects.get(pk=id)

    promo = get_object_or_404(Promo, pk=id)
    
    TopicImageInlineFormSet = inlineformset_factory(Topic, TopicImage)    

    if request.method == "POST":
        formset1 = TopicImageInlineFormSet(request.POST, request.FILES, instance=topic)
        form = TopicForm(request.POST, instance=topic)
        if formset1.is_valid():
            formset1.save()
        if form.is_valid():
            form.save()
            request.user.message_set.create(
                message='Your topic has been edited.')
            return HttpResponseRedirect(reverse('topics_topic_list'))
    else:
        formset1 = TopicImageInlineFormSet(instance=topic)
        form = TopicForm(instance=topic)        

    return render_to_response(
              'topics/topic_edit.html',
              ({'form': form, 'formset1': formset1}),
              context_instance=RequestContext(request))


@login_required
def topic_path_list(request):
    topic_path_list = TopicPath.objects.all()
    return render_to_response(
            'topics/topic_path_list.html',
            {'topic_path_list': topic_path_list},              
            context_instance=RequestContext(request))

@login_required
def topic_path_add(request):
    """
    Process a new topic path.
    """
    if request.method == "POST":
        form = TopicPathForm(request.POST)
        if form.is_valid():
            form.save()
            request.user.message_set.create(
                message='Your topic path has been added.  Thank you.')
            return HttpResponseRedirect(reverse('topics_topic_path_list'))

    else:
        #form = TopicForm(user=request.user)
        form = TopicPathForm()

    return render_to_response(
              'topics/topic_path_add.html',
              {'form':form},
              context_instance=RequestContext(request))

@login_required
def topic_path_edit(request, id):
    """
    Edit an existing topic path.
    """
    topic_path = TopicPath.objects.get(pk=id)
    if request.method == "POST":
        form = TopicPathForm(request.POST, instance=topic_path)
        if form.is_valid():
            form.save()
            request.user.message_set.create(
                message='Your topic has been edited.  Thank you.')
            return HttpResponseRedirect(reverse('topics_topic_path_list'))

    else:
        form = TopicPathForm(instance=topic_path)        
    return render_to_response(
              'topics/topic_path_edit.html',
              {'form':form},
              context_instance=RequestContext(request))

@login_required
def topic_path_detail(request,id):
    """
    TopicPath details
    """
    topic_path = get_object_or_404(TopicPath,pk=id)
    return render_to_response('topics/topic_path_detail.html',locals(),context_instance=RequestContext(request))

@login_required   
def topic_image_add(request):
    """
    Process a new topic image submission.
    """

    if request.method == "POST":
        form = TopicImageForm(request.POST)
        if form.is_valid():
            form.save()
            request.user.message_set.create(
                message='Your topic image has been added.  Thank you.')
            return HttpResponseRedirect(reverse('topics_topic_list'))

    else:
        form = TopicImageForm()

    return render_to_response(
              'topics/topic_image_add.html',
              {'form':form},
              context_instance=RequestContext(request))
