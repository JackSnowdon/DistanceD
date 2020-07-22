from django import forms
from .models import *

class NewGameInstance(forms.ModelForm):
    
    class Meta:
        model = GameInstance
        exclude = ['dm']


class NewGameSheet(forms.ModelForm):

    class Meta:
        model = GameSheet
        exclude = ['game', 'current_hit_points']