from django.contrib import admin
from django.forms import ModelForm
from django.utils.translation import gettext_lazy
from django.core.exceptions import ValidationError

# Python imports
import re

# Local imports
from .models import Profile, Skills, Projects

# Define models to appear under Profile
class SkillInLine(admin.StackedInline):
    model = Skills
    extra = 2

class ProjectInLine(admin.StackedInline):
    model = Projects
    extra = 2

class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = '__all__'

    def clean_phone(self):
        """The passed phone number should be
        10 characters
        not contain spaces, hyphens, or parenthesis"""
        value = self.cleaned_data['phone']

        if not value.__len__() == 10:
            raise(ValidationError(
                    gettext_lazy('Phone number "%(value)s" must follow the format ##########' +
                        ' Ensure this value has at most 10 characters'), 
                    params={'value':value},
                    ))

        reg = re.compile(pattern='[^0-9]')
        if reg.search(value):
            raise(ValidationError(
                gettext_lazy('Phone number "%(value)s" must' + 
                ' follow the format ##########. Do not include dashes or spaces'), 
                params={'value':value},
                ))

        return value

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    inlines = [SkillInLine, ProjectInLine]
    form = ProfileForm

admin.site.register(Profile, ProfileAdmin)