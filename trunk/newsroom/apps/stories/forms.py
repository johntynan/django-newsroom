from django import forms
from stories.models import Story, Page

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        exclude = ('authors','created','modified',)
        
class PageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)
        



