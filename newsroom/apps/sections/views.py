from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from sections.models import Section
from sections.models import SectionPath
# from sections.forms import SectionForm
from django.template import Context, loader

def sections_list(request):
    sections_list = Section.objects.all()
    t = loader.get_template('sections/sections_list.html')
    c = Context({
                'sections_list': sections_list,
    })
    return HttpResponse(t.render(c))

def section_detail(request, id):
    section_detail = Section.objects.get(id=id)
    t = loader.get_template('sections/section_detail.html')
    c = Context({
                'section': section_detail,
    })
    return HttpResponse(t.render(c))
 
def add_section(request, **kwargs):
    return HttpResponse('add_section')

def edit_section(request, **kwargs):
    return HttpResponse('edit_section')





