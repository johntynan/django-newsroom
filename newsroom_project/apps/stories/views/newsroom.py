# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify

from multimedia.models import Media
from multimedia import views as media_views
from stories.forms import StoryForm, PageForm, PageFormSet
from stories.models import Story, Page
from utils.helpers import user_objects_qs

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

#TODO: add authentication check decorators

@login_required
def story_list(request):
    stories = user_objects_qs(Story,request.user)
    return render_to_response('stories/story_edit_list.html',
            {'stories':stories},
            context_instance=RequestContext(request))

@login_required
def add_story(request):
    """
    Create a new Story for the user
    """
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.slug = slugify(story.headline)
            story.save()
            form.save_m2m()
            request.user.message_set.create(
                    message='Your story was saved.')
            return HttpResponseRedirect(reverse('stories_edit_story',args=[story.id]))
    else:
        form = StoryForm()

    return render_to_response(
                'stories/add_story.html',
                locals(),
                context_instance=RequestContext(request))


@login_required
def add_page(request,story_id):
    """
    Add a Page to a Story
    """
    user_stories = user_objects_qs(Story, request.user)
    story = get_object_or_404(user_stories,pk=story_id)
    page = story.add_page()
    #return render_to_response('stories/story_page_list',locals(),context_instance=RequestContext(request))
    #return HttpResponseRedirect(reverse('stories_edit_page',args=[page.id]))
    return HttpResponse("", mimetype="text/plain")


@login_required
def save_page(request,story_id):
    """
    saves (creates or replaces) pages in a story
    takes a formset of page forms and saves each form object
    as a page object related to a story

    note: this view is only used for ajax requests
    response descriptions:
    1 : sucessfull
    -1 : invalid formset
    0 : invalid request
    """
    user_stories = user_objects_qs(Story, request.user)
    story = get_object_or_404(user_stories,pk=story_id)
    #post = {}
    #post['form-0-content'] = "abc"
    #post['form-0-pagenum'] = "1"
    #post['form-INITIAL_FORMS'] = "0"
    #post['form-TOTAL_FORMS'] = "1"

    if request.POST:
        page_formset = PageFormSet(request.POST)
        if page_formset.is_valid():

            for form in page_formset.forms:
                page = None
                try:
                    page = Page.objects.get(story=story,pagenum=form.cleaned_data['pagenum'])
                except MultipleObjectsReturned:
                    Page.objects.filter(story=story,pagenum=form.cleaned_data['pagenum']).delete()
                except ObjectDoesNotExist:
                    pass

                if not page:
                    page = Page()
                    page.story = story
                    page.pagenum = form.cleaned_data['pagenum']

                page.content = form.cleaned_data['content']
                page.save()
            return HttpResponse("1", mimetype="text/plain")
        else:
            return HttpResponse("-1", mimetype="text/plain")

    return HttpResponse("0", mimetype="text/plain")

@login_required
def edit_story(request,story_id):
    user_stories = user_objects_qs(Story, request.user)
    story = get_object_or_404(user_stories,pk=story_id)
    if request.method == 'POST':
        form = StoryForm(request.POST,instance=story)
        if form.is_valid():
            form.save()
            request.user.message_set.create(
                    message='Your story was saved.')
            return HttpResponseRedirect(
                    reverse('stories_story_pages', args=[story.id]))
    else:
        form = StoryForm(instance=story)

    return render_to_response(
                'stories/edit_story.html',
                locals(),
                context_instance=RequestContext(request))

@login_required
def story_pages(request,story_id):
    user_stories = user_objects_qs(Story, request.user)
    story = get_object_or_404(user_stories,pk=story_id)
    page_formset = PageFormSet()

    return render_to_response('stories/story_page_list.html',locals(),context_instance=RequestContext(request))

@login_required
def story_media(request,story_id):

    user_stories = user_objects_qs(Story, request.user)
    story = get_object_or_404(user_stories,pk=story_id)
    system_media_types = Media.media_types
    related_content = story.get_relatedcontent()
    if request.is_ajax():
        return render_to_response('stories/story_media_list_ajax.html',locals(),context_instance=RequestContext(request))
    return render_to_response('stories/story_media_list.html',locals(),context_instance=RequestContext(request))


#TODO: Check the security on this view
@login_required
def edit_page(request,page_id):
    page = get_object_or_404(Page,pk=page_id)
    story = page.story
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page.content = form.cleaned_data['content']
            page.save()
            return HttpResponseRedirect(reverse('stories_story_pages',args=[page.story.id]))
    else:
        form = PageForm({'content':page.content})
    return render_to_response('stories/edit_page.html',
                              locals(),
                              context_instance=RequestContext(request))

@login_required
def story_add_edit_media(request, story_id, media_type=None, media_id=None):
    """
    media_type should be defined on add, and media_id is defined on edit.
    """

    user_stories = user_objects_qs(Story, request.user)
    story = get_object_or_404(user_stories,pk=story_id)
    kwargs = {}

    if media_id:
        media = get_object_or_404(Media, pk=media_id)
        object = media.get_child_object()
        media_type = object.media_type.lower()

    kwargs['template'] = 'stories/%s_add_edit.html' % media_type
    kwargs['redirect_to'] = 'stories_story_list'
    kwargs['context_dict'] = {'story':story,}
    kwargs['story'] = story
    if media_id:
        kwargs['media_id'] = media_id

    return media_views.add_edit_child_media(request, media_type, **kwargs)

    #media = get_object_or_404(Media,pk=request.POST.get('media_id'))
    #story.media.add(media)
    #return render_to_response(
    #            'stories/add_edit_media.html',
    #            {'story':story,},
    #            context_instance=RequestContext(request))

@login_required
def story_add_edit_geotag(request,story_id,
    template=None, form_class=None, geotag_class=None):
    """
    This view determines the content_type and the
    object_id for the given story (story_id) then it returns
    the response of add_edit_geotag.
    """
    user_stories = user_objects_qs(Story, request.user)
    story = get_object_or_404(user_stories,pk=story_id)
    story_content_type = ContentType.objects.get_for_model(story)
    try:
        geotag = geotag_class.objects.get(content_type__pk=story_content_type.id,
                               object_id=story.id)
    except ObjectDoesNotExist:
        geotag = None
    if request.method == "POST":
        form = form_class(request.POST, instance=geotag)
        if form.is_valid():
            new_object = form.save(commit=False)
            new_object.object = story
            new_object.save()
            return HttpResponseRedirect(
                reverse('stories_story_pages', args=[story.id]))
    form = form_class(instance=geotag)

    context = RequestContext(request, {
        "form": form,
        "geo_type": form_class._meta.model._meta.verbose_name,
        "story": story,
        "google_key": settings.GOOGLE_MAPS_API_KEY,
        "geotag": geotag,
    })
    return render_to_response(template, context_instance=context )


@login_required
def story_select_media(request,story_id,media_type):
    user_stories = user_objects_qs(Story, request.user)
    story = get_object_or_404(user_stories,pk=story_id)
    MediaType = Media.class_factory(media_type)

    object_list = MediaType.objects.filter(authors__pk__exact=request.user.pk)
    return render_to_response('stories/select_media.html',locals(),context_instance=RequestContext(request))



@login_required
def text_widget(request,widget_name):
    return render_to_response('stories/widgets/%s.html' % widget_name,locals(),context_instance=RequestContext(request))

# TODO: Check the security of this view
@login_required
def media_widget(request,media_id):

    media = get_object_or_404(Media, pk=media_id)
    object = media.get_child_object()
    media_type = object.media_type.lower()

    return render_to_response('stories/widgets/media.html',locals(),context_instance=RequestContext(request))

@login_required
def page_template(request,template_name):
    return render_to_response('stories/templates/%s.html' % template_name,locals(),context_instance=RequestContext(request))



