from django import forms
from multimedia.models import Media

class MediaForm(forms.ModelForm):
    class Meta:
        model = Media

