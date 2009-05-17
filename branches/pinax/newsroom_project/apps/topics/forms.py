from django import forms
from topics.models import Topic
from topics.models import TopicPath
from photos.models import Photo

class TopicForm(forms.ModelForm):
    
    class Meta:
        model = Topic
        fields = ('title','slug','description','topic_path')

class TopicPathForm(forms.ModelForm):
    
    class Meta:
        model = TopicPath

class TopicImageForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ('title','image','caption','promo')