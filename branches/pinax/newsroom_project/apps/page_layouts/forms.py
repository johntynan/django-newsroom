from django import forms
from page_layouts.models import PageLayout

class PageLayoutForm(forms.ModelForm):
    
    class Meta:
        model = PageLayout
        fields = ('title','html','description','image')
