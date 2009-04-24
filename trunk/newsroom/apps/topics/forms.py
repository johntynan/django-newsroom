from django import forms
from topics.models import Topic
from topics.models import TopicPath

class TopicForm(forms.ModelForm):
    
    class Meta:
        model = Topic
        fields = ('title','slug','description','collection')

class TopicPathForm(forms.ModelForm):
    
    class Meta:
        model = TopicPath
