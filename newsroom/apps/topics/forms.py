from django import forms
from topics.models import Topic
from topics.models import TopicPath

class TopicForm(forms.ModelForm):
    
    class Meta:
        model = Topic
        fields = ('title','slug','description',)

class TopicPathForm(forms.ModelForm):
    
    class Meta:
        model = TopicPath
