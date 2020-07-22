from django import forms
from .models import *
from characters.models import Base

class NewGameInstance(forms.ModelForm):
    
    class Meta:
        model = GameInstance
        exclude = ['dm']


class NewGameSheet(forms.ModelForm):

    class Meta:
        model = GameSheet
        exclude = ['game']


class EditSheetHP(forms.ModelForm):

    class Meta:
        model = GameSheet
        fields = ['current_hit_points']


class AddOwnSheet(forms.ModelForm):

    class Meta:
        model = GameSheet
        exclude = ['game']

    def __init__(self, user, *args, **kwargs):
        super(AddOwnSheet, self).__init__(*args, **kwargs)
        self.fields['base'].queryset = Base.objects.filter(created_by=user.profile)

        