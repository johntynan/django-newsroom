from django import forms
from multimedia.models import Media

class MediaForm(forms.ModelForm):
    
    @staticmethod
    def factory(type):
        media_type = Media.class_factory(type) 
        class __MediaForm(forms.ModelForm):
            class Meta:
                model = media_type
                exclude = ('slug','created_by', 'modified_by', 'created','modified','frame')
                
        return __MediaForm
    

