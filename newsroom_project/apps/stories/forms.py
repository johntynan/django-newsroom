# -*- coding: utf-8 -*-
from django import forms
from stories.models import Story, Page

from django.forms.formsets import formset_factory


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        exclude = ('slug','created','modified','media','topics','status','projects',)

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        exclude = ('story',)

PageFormSet = formset_factory(PageForm)


#class SelectMediaForm(forms.Form):
#
#    @staticmethod
#    def factory(media_type):
#        pass

