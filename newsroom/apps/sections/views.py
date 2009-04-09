from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from sections.models import Section
from sections.models import SectionPath
# from sections.forms import SectionForm
from django.template import Context, loader
from sections.forms import *

def sections_list(request):
    sections_list = Section.objects.all()
    return render_to_response(
            'sections/sections_list.html',
            {'sections_list': sections_list},              
            context_instance=RequestContext(request))
    
def section_detail(request, id):
    section_detail = Section.objects.get(id=id)
    return render_to_response(
            'sections/section_detail.html',
            {'section': section_detail},              
            context_instance=RequestContext(request))
    
def section_add(request):
    """
    Process a new section submission.
    """

    if request.method == "POST":
        form = SectionForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.submitter = request.user
            section.save()
            request.user.message_set.create(
                message='Your section has been submitted.  Thank you.')
            return HttpResponseRedirect(request.user.get_profile().get_absolute_url())

    else:
        #form = SectionForm(user=request.user)
        form = SectionForm()

    return render_to_response(
              'sections/section_add.html',
              {'form':form},
              context_instance=RequestContext(request))

def section_edit(request,id):
    """
    Process a new section submission.
    """

    if request.method == "POST":
        form = SectionForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.submitter = request.user
            section.save()
            request.user.message_set.create(
                message='Your section has been submitted.  Thank you.')
            return HttpResponseRedirect(request.user.get_profile().get_absolute_url())

    else:
        #form = SectionForm(user=request.user)
        form = SectionForm()

    return render_to_response(
              'sections/section_edit.html',
              {'form':form},
              context_instance=RequestContext(request))
