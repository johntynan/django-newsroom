from django import forms
from django.forms import widgets
from promos.models import *
from core.models import *
from photos.models import Photo

class PromoForm(forms.ModelForm):
    """
    Create our own form based on the Promo model.  

    We also want to populate the affiliate field with people based on the
    current user making the request.  
    """
    
    #def __init__(self, user=None, *args, **kwargs):
    #    #queryset=Person.objects.filter()
    #    super(PromoForm, self).__init__(*args, **kwargs)
        #person = user.person_set.get()
        #self.fields['authors'].queryset = \
        #    Person.objects.filter(affiate=person.affiliate)
    #     self.fields['permalink'].widget = widgets.TextInput()
    #    #self.fields['authors'].widget = widgets.SelectMultiple()

    
    class Meta:
        model = Promo
        fields = ('headline','permalink','description','authors','other_credits', 'location', 'topic_path', 'suggested_dates', 'relevance_begins', 'relevance_ends')

class LinkForm(forms.ModelForm):
    
    class Meta:
        model = PromoLink
        fields = ('title','url','desc','promo')
        
class ImageForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ('title','image','caption','promo')
