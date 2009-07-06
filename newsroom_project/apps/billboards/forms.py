from django import forms
from django.core.files.storage import FileSystemStorage
from billboards.models import Billboard

class BillboardForm(forms.ModelForm):

    headline_position_vertical = forms.CharField(widget=forms.TextInput(attrs={'size':'3'}))
    headline_position_horizontal = forms.CharField(widget=forms.TextInput(attrs={'size':'3'}))
    supporting_text = forms.CharField(widget=forms.Textarea(attrs = {'cols':40,'rows':3}))

    class Meta:
        model = Billboard

