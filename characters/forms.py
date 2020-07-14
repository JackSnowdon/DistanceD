from django import forms
from .models import *

class BaseForm(forms.ModelForm):
    class Meta:
        model = Base
        exclude = ['created_by']