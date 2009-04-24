from django import forms
from sections.models import Section
from sections.models import SectionPath

class SectionForm(forms.ModelForm):
    
    class Meta:
        model = Section
        fields = ('title','slug','description','collection')

class SectionPathForm(forms.ModelForm):
    
    class Meta:
        model = SectionPath
