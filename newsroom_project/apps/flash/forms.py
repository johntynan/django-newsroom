from django import forms
from flash.models import FlashProject, PosterFrame

def handle_uploaded_file(f):
    destination = open('some/file/name.txt', 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

class FlashProjectForm(forms.ModelForm):

    zip_file = forms.FileField()

    class Meta:
        model = FlashProject
        exclude = ('modified_by', 'created_by')

    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data

class PosterFrameForm(forms.ModelForm):

    class Meta:
        model = PosterFrame

