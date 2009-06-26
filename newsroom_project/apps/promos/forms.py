from django import forms
from promos.models import *
from core.models import *

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

    headline = forms.CharField(widget=forms.TextInput(attrs={'size':'100'}))
    permalink = forms.CharField(widget=forms.TextInput(attrs={'size':'100'}))
    description = forms.CharField(widget=forms.Textarea(attrs = {'cols':76,'rows':8}))
    other_credits = forms.CharField(widget=forms.Textarea(attrs = {'cols':40,'rows':3}))
    
    class Meta:
        model = Promo
        fields = ('headline','permalink','description','authors','other_credits', 'location', 'topic_path')

class LinkForm(forms.ModelForm):
    
    class Meta:
        model = PromoLink
        fields = ('title','url','desc')
        
class ImageForm(forms.ModelForm):

    class Meta:
        model = PromoImage
        exclude =('promo')

class DateForm(forms.ModelForm):
    
    class Meta:
        model = PromoDate
        exclude =('promo')
