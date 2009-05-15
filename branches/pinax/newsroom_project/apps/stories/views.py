# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, Template, Context
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify

from multimedia.models import Media
from multimedia import views as media_views
from stories.forms import StoryForm, PageForm, PageFormSet
from stories.models import Story, Page

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

#TODO: add authentication check decorators

@login_required
def story_list(request):
    stories = request.user.story_set.all()
    return render_to_response('stories/story_list.html',locals(),context_instance=RequestContext(request))

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
    story = get_object_or_404(Story,pk=story_id)
    page = story.add_page()
    #return render_to_response('stories/story_page_list',locals(),context_instance=RequestContext(request))
    #return HttpResponseRedirect(reverse('stories_edit_page',args=[page.id]))
    return HttpResponse("", mimetype="text/plain")


@login_required
def save_page(request,story_id):
    """
    saves (creates or replaces) a story
    """
    story = get_object_or_404(Story,pk=story_id)
    page_formset = PageFormSet(request.POST)
    if page_formset.is_valid():
        page = None
        for form in page_formset.cleaned_data:
            try:
                page = Page.objects.get(story=story,pagenum=form['pagenum'])
            except MultipleObjectsReturned:
                Page.objects.filter(story=story,pagenum=form['pagenum']).delete()
            except ObjectDoesNotExist:
                pass

            if not page:
                page = Page()
                page.story = story
                page.pagenum = form['pagenum']

            page.content = form['content']
            page.save()
        return HttpResponse("1", mimetype="text/plain")
    else:
        print page_formset.errors
        return HttpResponse("-1", mimetype="text/plain")

@login_required
def edit_story(request,story_id):
    story = get_object_or_404(Story,pk=story_id)
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
    story = get_object_or_404(Story,pk=story_id)
    page_formset = PageFormSet()
    return render_to_response('stories/story_page_list.html',locals(),context_instance=RequestContext(request))

@login_required
def story_media(request,story_id):
    story = get_object_or_404(Story,pk=story_id)
    system_media_types = Media.media_types
    return render_to_response('stories/story_media_list.html',locals(),context_instance=RequestContext(request))

@login_required
def story(request,slug):
    story = get_object_or_404(Story,slug=slug)
    pagenum = request.GET.get('p',1)
    page = story.get_page(1)

    #render the page content so that media tags are handled
    template = Template("{%% load media_tags %%}%s" %  page.content)
    content = template.render(Context())

    #TODO: get the template to use from the story

    #TODO: handle column breaks
    return render_to_response('stories/display_page_content.html',
                              locals(),
                              context_instance=RequestContext(request))

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

    story = get_object_or_404(Story,pk=story_id)
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
def story_select_media(request,story_id,media_type):
    story = get_object_or_404(Story,pk=story_id)
    MediaType = Media.class_factory(media_type)

    object_list = MediaType.objects.filter(authors__pk__exact=request.user.pk)
    return render_to_response('stories/select_media.html',locals(),context_instance=RequestContext(request))



@login_required
def text_widget(request,widget_name):
    return render_to_response('stories/widgets/%s.html' % widget_name,locals(),context_instance=RequestContext(request))

@login_required
def media_widget(request,media_id):

    media = get_object_or_404(Media, pk=media_id)
    object = media.get_child_object()
    media_type = object.media_type.lower()

    return render_to_response('stories/widgets/media.html',locals(),context_instance=RequestContext(request))

@login_required
def page_template(request,template_name):
    return render_to_response('stories/templates/%s.html' % template_name,locals(),context_instance=RequestContext(request))

