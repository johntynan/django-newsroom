from django import forms
from stories.models import Story

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        exclude = ('author','created','modified',)
        



