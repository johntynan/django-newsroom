from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from sections.forms import SectionForm
from sections.models import Section

#TODO: add authentication check decorators

def add_section(request):
    """
    Create a new Section for the user
    """
    if request.method == 'POST':
        form = SectionForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.author = request.user
            section.save()
            return HttpResponseRedirect(reverse('sections_section_detail',args=[section.id]))
    form = SectionForm()
    print form
    return render_to_response('sections/add_section.html',locals())
    

def add_page(request,section_id):
    """
    Add a Page to a Section
    """
    pass

def section_detail(request,section_id):
    section = get_object_or_404(Section,pk=section_id)
    return render_to_response('sections/section_detail.html',locals())



