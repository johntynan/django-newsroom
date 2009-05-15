# -*- coding: utf-8 -*-
from django import forms
from stories.models import Story, Page

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        exclude = ('slug','created','modified','media','topics','status','projects',)

class PageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)
    pagenum = forms.CharField()
    pagecount = forms.CharField()

#class SelectMediaForm(forms.Form):
#
#    @staticmethod
#    def factory(media_type):
#        pass

