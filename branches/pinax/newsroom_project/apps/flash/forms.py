from django import forms

class FlashForm(forms.ModelForm):

    class Meta:
        model = Flash


class FlashArchiveForm(forms.ModelForm):

    class Meta:
        model = FlashArchive

