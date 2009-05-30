from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext,Context, loader

from page_layouts.forms import PageLayoutForm
from page_layouts.models import PageLayout

from django.core import serializers

# @login_required
def page_layout_list(request):
    page_layout_list = PageLayout.objects.all()
    return render_to_response(
            'page_layouts/page_layout_list.html',
            {'page_layout_list': page_layout_list},              
            context_instance=RequestContext(request))

# @login_required
def page_layout_detail(request, id):
    page_layout = PageLayout.objects.get(id=id)    
    return render_to_response(
            'page_layouts/page_layout_detail.html',{
                'page_layout': page_layout,
             }, context_instance=RequestContext(request))

# @login_required
def page_layout_list_json(request):
    page_layout_list = serializers.serialize("json", PageLayout.objects.all())
    return render_to_response(
            'page_layouts/page_layout_list.json',
            {'page_layout_list': page_layout_list},              
            context_instance=RequestContext(request))

# @login_required
def page_layout_detail_json(request, id):
    page_layout = serializers.serialize("json", PageLayout.objects.get(id=id))    
    return render_to_response(
            'page_layouts/page_layout_detail.json',{
                'page_layout': page_layout,
             }, context_instance=RequestContext(request))
