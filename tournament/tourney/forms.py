from django import forms
from .models import TournamentModel, PlayerModel, GameModel
from django.forms.models import inlineformset_factory

class TournamentForm(forms.ModelForm):
    class Meta:
        model = TournamentModel
        fields = ['name', 'game', 'position_priority']

    def save(self, commit=True):
        return super().save(commit=commit)

class PlayerForm(forms.ModelForm):
    class Meta:
        model = PlayerModel
        fields = ['name']

class GameForm(forms.ModelForm):
    class Meta:
        model = GameModel
        fields = ['home_player', 'h_score', 'a_score', 'away_player']

