from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, Template, Context

from stories.forms import StoryForm
from stories.models import Story

#TODO: add authentication check decorators

def add_story(request):
    """
    Create a new Story for the user
    """
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            story.save()
            return HttpResponseRedirect(reverse('stories_story_detail',args=[story.id]))
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
    pass

def story_detail(request,story_id):
    story = get_object_or_404(Story,pk=story_id)
    return render_to_response(
                'stories/story_detail.html',
                locals(),
                context_instance=RequestContext(request))


def show_story(request,slug):
    story = get_object_or_404(Story,slug=slug)
    pagenum = request.GET.get('p',1)
    page = story.get_page(1)
    
    #render the page content so that media tags are handled
    print page.content
    template = Template("{%% load media_tags %%}%s" %  page.content)
    content = template.render(Context())
    print content
    #TODO: get the template to use from the story
    
    return render_to_response('stories/display_page_content.html',
                              locals(),
                              context_instance=RequestContext(request))

