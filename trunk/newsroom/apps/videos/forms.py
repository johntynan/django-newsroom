from django import forms
from videos.models import Video

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        exclude = ('slug','created_by', 'modified_by', 'created','modified','frame')

