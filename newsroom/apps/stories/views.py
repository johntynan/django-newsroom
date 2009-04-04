from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from stories.forms import StoryForm

def add_story(request):
    """
    Create a new Story for the user
    """
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            return HttpResponseRedirect(reverse('stories_story_detail'),args=[story.id])
    form = StoryForm()
    print form
    return render_to_response('stories/add_story.html',locals())
    

def add_page(request,story_id):
    """
    Add a Page to a Story
    """
    pass

def story_detail(request,story_id):
    pass



