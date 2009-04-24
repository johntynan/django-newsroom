from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from sections.models import Section
from sections.models import SectionPath
from django.template import Context, loader
from django.core.urlresolvers import reverse
from sections.forms import SectionForm, SectionPathForm
from promos.models import Promo

def sections_list(request):
    sections_list = Section.objects.all()
    return render_to_response(
            'sections/sections_list.html',
            {'sections_list': sections_list},              
            context_instance=RequestContext(request))
 
def section_detail(request, id):
    section_detail = Section.objects.get(id=id)
    section_slug = section_detail.slug
    sec_paths = SectionPath.objects.filter(section__slug=section_slug)
    promos = Promo.objects.filter(section_path__in=sec_paths).distinct()

    return render_to_response(
            'sections/section_detail.html',{
                'section': section_detail,
                'sec_paths': sec_paths,
                'promos': promos

             }, context_instance=RequestContext(request))

def section_add(request):
    """
    Process a new section submission.
    """

    if request.method == "POST":
        form = SectionForm(request.POST)
        if form.is_valid():
            form.save()
            request.user.message_set.create(
                message='Your section has been added.  Thank you.')
            return HttpResponseRedirect(reverse('sections_section_list'))

    else:
        #form = SectionForm(user=request.user)
        form = SectionForm()

    return render_to_response(
              'sections/section_add.html',
              {'form':form},
              context_instance=RequestContext(request))

def section_edit(request, id):
    """
    Edit an existing section.
    """
    section = Section.objects.get(pk=id)
    
    if request.method == "POST":
        form = SectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            request.user.message_set.create(
                message='Your section has been edited.  Thank you.')
            return HttpResponseRedirect(reverse('sections_section_list'))

    else:
        form = SectionForm(instance=section)        
    return render_to_response(
              'sections/section_edit.html',
              {'form':form},
              context_instance=RequestContext(request))

def section_path_list(request):
    section_path_list = SectionPath.objects.all()
    return render_to_response(
            'sections/section_path_list.html',
            {'section_path_list': section_path_list},              
            context_instance=RequestContext(request))

def section_path_add(request):
    """
    Process a new section path.
    """
    if request.method == "POST":
        form = SectionPathForm(request.POST)
        if form.is_valid():
            form.save()
            request.user.message_set.create(
                message='Your section path has been added.  Thank you.')
            return HttpResponseRedirect(reverse('sections_section_path_list'))

    else:
        #form = SectionForm(user=request.user)
        form = SectionPathForm()

    return render_to_response(
              'sections/section_path_add.html',
              {'form':form},
              context_instance=RequestContext(request))

def section_path_edit(request, id):
    """
    Edit an existing section path.
    """
    section_path = SectionPath.objects.get(pk=id)
    if request.method == "POST":
        form = SectionPathForm(request.POST, instance=section_path)
        if form.is_valid():
            form.save()
            request.user.message_set.create(
                message='Your section has been edited.  Thank you.')
            return HttpResponseRedirect(reverse('sections_section_path_list'))

    else:
        form = SectionPathForm(instance=section_path)        
    return render_to_response(
              'sections/section_path_edit.html',
              {'form':form},
              context_instance=RequestContext(request))

