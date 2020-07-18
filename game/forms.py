from django import forms
from .models import *

class NewCombatInstance(forms.ModelForm):
    
    class Meta:
        model = CombatInstance
        exclude = ['dm']


class NewCombatMember(forms.ModelForm):

    class Meta:
        model = CombatMember
        exclude = ['game']