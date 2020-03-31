from django import forms
from .models import TournamentModel

class TorunamentForm(forms.ModelForm):
    player1 = forms.CharField(max_length=150)
    player2 = forms.CharField(max_length=150)
    player3 = forms.CharField(max_length=150)
    player4 = forms.CharField(max_length=150)
    class Meta:
        model = TournamentModel
        fields = ['name', 'players']

    def save(self, commit=True):
        return super().save(commit=commit)
