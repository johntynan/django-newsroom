from django import forms
from flash.models import FlashProject, PosterFrame

def handle_uploaded_file(f):
    destination = open('some/file/name.txt', 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

class FlashProjectForm(forms.ModelForm):

    zip_file = forms.FileField(
                    help_text="Zip file containing a subdirectory with flash project inside of it.")

    class Meta:
        model = FlashProject
        fields = ('title', 'authors','license','status','summary','attribution','width','height','flash_compat','zip_file')

    def clean(self):
        return self.cleaned_data

class PosterFrameForm(forms.ModelForm):

    class Meta:
        model = PosterFrame

