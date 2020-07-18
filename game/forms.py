from django import forms
from .models import *

class NewCombatInstance(forms.ModelForm):
    
    class Meta:
        model = CombatInstance
        exclude = ['dm']