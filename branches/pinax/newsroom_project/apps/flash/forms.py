from django import forms
from django.core.files.storage import FileSystemStorage
from flash.models import Flash, FlashArchive

class FlashForm(forms.ModelForm):

    class Meta:
        model = Flash


class FlashArchiveForm(forms.ModelForm):

    class Meta:
        model = FlashArchive
