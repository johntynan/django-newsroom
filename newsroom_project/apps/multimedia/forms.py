from django import forms
from multimedia.models import Media

class MediaForm(forms.ModelForm):
    
    @staticmethod
    def factory(type):
        media_type = Media.class_factory(type) 
        class __MediaForm(forms.ModelForm):
            class Meta:
                model = media_type
                exclude = ('site','slug','created_by', 'modified_by', 'created','modified','pub_date','frame')
                
        return __MediaForm
    

