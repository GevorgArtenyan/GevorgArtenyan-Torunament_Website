from django import forms
from .models import TournamentModel, PlayerModel
from django.forms.models import inlineformset_factory

class TorunamentForm(forms.ModelForm):
    class Meta:
        model = TournamentModel
        fields = ['name']

    def save(self, commit=True):
        return super().save(commit=commit)

class PlayerForm(forms.ModelForm):
    class Meta:
        model = PlayerModel
        fields = ['name']


TournamentPlayerFormSet = inlineformset_factory(TournamentModel, PlayerModel,
                                                form=PlayerForm, extra=2)