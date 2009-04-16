from django import forms
from django.forms import widgets
from features.models import *
from core.models import *
from photologue.models import Photo

class FeatureForm(forms.ModelForm):
    """
    Create our own form based on the Feature model.  

    We also want to populate the affiliate field with people based on the
    current user making the request.  
    """
    
    #def __init__(self, user=None, *args, **kwargs):
    #    #queryset=Person.objects.filter()
    #    super(FeatureForm, self).__init__(*args, **kwargs)
        #person = user.person_set.get()
        #self.fields['authors'].queryset = \
        #    Person.objects.filter(affiate=person.affiliate)
    #     self.fields['permalink'].widget = widgets.TextInput()
    #    #self.fields['authors'].widget = widgets.SelectMultiple()

    
    class Meta:
        model = Feature
        fields = ('headline','permalink','project','authors','other_credits', 'section', 'relevance_begins', 'relevance_ends')

class LinkForm(forms.ModelForm):
    
    class Meta:
        model = FeatureLink

class ImageForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ('title','image','caption')
