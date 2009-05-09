from django import forms
from multimedia.models import Media
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe


class MediaForm(forms.ModelForm):
    
    @staticmethod
    def factory(type):
        media_class = Media.class_factory(type) 
        class __MediaForm(forms.ModelForm):
            class Meta:
                model = media_class
                exclude = ('site','slug','created_by', 'modified_by', 'created','modified','pub_date',)
                
        return __MediaForm
    

class FileWidget(forms.FileInput):
    """
    Swiped from django admin.  Maybe all our media forms could inheret
    this.  TODO 
    """

    def __init__(self, attrs={}):
        super(FileWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, "url"):
            output.append('%s <a target="_blank" href="%s">%s</a> <br />%s ' % \
                (_('Currently:'), value.url, value, _('Change:')))
        output.append(super(FileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))
