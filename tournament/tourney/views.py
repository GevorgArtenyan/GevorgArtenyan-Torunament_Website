from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from .models import TournamentModel, PlayerLeagueModel, MatchModel, GameModel
from django.forms import inlineformset_factory
from .serializers import PlayerSerializer
from rest_framework import generics
from .table import table, match_calc, sort_table
from rest_framework.permissions import IsAuthenticated

class PlayerAPIListView(generics.UpdateAPIView):
    lookup_field = 'pk'
    queryset = PlayerLeagueModel.objects.all()
    serializer_class = PlayerSerializer


class TournamentListView(ListView):
    model = TournamentModel
    template_name = 'tourney/home.html'


class TournamentUpdateView(UpdateView):
    model = TournamentModel
    fields = ['position_priorities']
    template_name = 'tourney/index.html'


def index(request, pk):
    tournament = TournamentModel.objects.get(pk=pk)
    PlayerFormset = inlineformset_factory(TournamentModel, PlayerLeagueModel, fields=('name', ))

    if request.method == 'POST':
        formset = PlayerFormset(request.POST, instance=tournament)
        if formset.is_valid():
            formset.save()

            return redirect('index', pk=pk)
    formset = PlayerFormset(instance=tournament)
    related_players = sort_table(PlayerLeagueModel.objects.filter(tournament=tournament))
    matches = MatchModel.objects.filter(player1__in=related_players)
    games = GameModel.objects.filter(home_player__in=related_players)

    table(related_players, games)
    match_calc(games)

    return render(request, 'tourney/index.html', {'formset':formset, 'related_players':related_players,
                'matches':matches, 'games':games})


class GameUpdateView(UpdateView):
    model = GameModel
    fields = ['h_score', 'a_score']
    template_name = 'tourney/game_update.html'


