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
        labels = {
        "current_hit_points": "Current HP (Leave at 0 to match max)",
        "max_hit_points": "Max HP",
    }