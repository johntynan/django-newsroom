from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm as BasicPasswordResetForm
from django.conf import settings
from django.utils.translation import ugettext as _
from registration.forms import RegistrationFormUniqueEmail

from profiles import utils
profile_model = utils.get_profile_model()

class ProfileForm(forms.ModelForm):
    
    mugshot = forms.FileField(
                help_text='A JPEG image of yourself or something that \
                           represents you.',
                )

    class Meta:
        model = profile_model
        exclude = ('user','latitude','longitude','mugshot')

class RegistrationForm(RegistrationFormUniqueEmail):
    """
    Subclass here if we want to add more fields or details to registration
    form. For now just inherit unique email form.
    """
    # max_length attr based on User definition since these are going in
    # user model
    first_name = forms.CharField(max_length=30)  
    last_name = forms.CharField(max_length=30)  
    
    class Meta:

        fields = ('first_name','last_name','username','email',
                  'password','password2')

    def save(self, *args, **kwargs):
        """
        Overriding save, so call the parent form save and return the new_user
        object.
        """
        new_user = super(RegistrationForm, self).save(*args, **kwargs) 
        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        new_user.save()
        return new_user


class PasswordResetForm(BasicPasswordResetForm):
    """
    Override clean_email()
    No sense in sending a password to someone who is not active, let them know.     
    """
    def clean_email(self):
        """
        Validates that a user exists with the given e-mail address.
        """
        email = self.cleaned_data["email"]
        self.users_cache = User.objects.filter(email__iexact=email)
        if len(self.users_cache) == 0:
            raise forms.ValidationError(_("That e-mail address doesn't have an associated user account. Are you sure you've registered?"))
        elif self.users_cache[0].is_active != True:
            raise forms.ValidationError(_("""Sorry, this account is inactive because the email address was never confirmed. You may have an active account with another email address, you can try that or contact us for further assistance."""))

