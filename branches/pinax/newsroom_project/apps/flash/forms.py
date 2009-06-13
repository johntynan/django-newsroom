from django import forms
from flash.models import Flash, FlashArchive

class FlashForm(forms.ModelForm):

    class Meta:
        model = Flash


class FlashArchiveForm(forms.ModelForm):

    class Meta:
        model = FlashArchive

