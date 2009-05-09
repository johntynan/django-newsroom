from django import forms
from videos.models import Video, VideoFrame
from multimedia.forms import FileWidget

class VideoForm(forms.ModelForm):

    video = forms.FileField( widget=FileWidget)

    class Meta:
        model = Video
        fields = ('title','authors','license','status','video','tags','summary','attribution')


class VideoFrameForm(forms.ModelForm):

    image = forms.FileField( 
                label="Frame",
                help_text='One frame or image that represents the video.  Should be same width/height as the video.',
                widget=FileWidget, )

    class Meta:
        model = VideoFrame
