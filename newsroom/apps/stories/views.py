from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, Template, Context

from multimedia.models import Media
from stories.forms import StoryForm, PageForm
from stories.models import Story, Page

#TODO: add authentication check decorators

def story_list(request):
    stories = request.user.story_set.all()
    return render_to_response('stories/story_list.html',locals(),context_instance=RequestContext(request))

def add_story(request):
    """
    Create a new Story for the user
    """
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            story = form.save()
            return HttpResponseRedirect(reverse('stories_edit_story',args=[story.id]))
        else:
            print form.errors
    else:
        form = StoryForm()

    return render_to_response(
                'stories/add_story.html',
                locals(),
                context_instance=RequestContext(request))
    

def add_page(request,story_id):
    """
    Add a Page to a Story
    """
    story = get_object_or_404(Story,pk=story_id)
    page = story.add_page()
    #return render_to_response('stories/story_page_list',locals(),context_instance=RequestContext(request))
    return HttpResponseRedirect(reverse('stories_edit_page',args=[page.id]))

def edit_story(request,story_id):
    story = get_object_or_404(Story,pk=story_id)
    form = StoryForm(instance=story)
    return render_to_response(
                'stories/edit_story.html',
                locals(),
                context_instance=RequestContext(request))
    
def story_pages(request,story_id):
    story = get_object_or_404(Story,pk=story_id)
    return render_to_response('stories/story_page_list.html',locals(),context_instance=RequestContext(request))
    


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
    
def story_add_media(request,story_id):
    story = get_object_or_404(Story,pk=story_id)
    media = get_object_or_404(Media,pk=request.POST.get('media_id'))
    story.media.add(media)
    return render_to_response('stories/story_media_list.html',locals())