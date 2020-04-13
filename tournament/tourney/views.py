from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from .models import TournamentModel, PlayerModel, MatchModel
from django.forms import inlineformset_factory
from .serializers import PlayerSerializer
from rest_framework import generics
from .table import table
from rest_framework.permissions import IsAuthenticated

class PlayerAPIListView(generics.ListAPIView):
    lookup_field = 'pk'
    queryset = PlayerModel.objects.all()
    serializer_class = PlayerSerializer


class TournamentListView(ListView):
    model = TournamentModel
    template_name = 'tourney/home.html'


def index(request, pk):
    tournament = TournamentModel.objects.get(pk=pk)
    PlayerFormset = inlineformset_factory(TournamentModel, PlayerModel, fields=('name', ))

    if request.method == 'POST':
        formset = PlayerFormset(request.POST, instance=tournament)
        if formset.is_valid():
            formset.save()

            return redirect('index', pk=pk)
    formset = PlayerFormset(instance=tournament)
    related_players = PlayerModel.objects.filter(tournament=tournament).order_by('-points', '-goal_difference')
    matches = MatchModel.objects.filter(player1__in=related_players)

    table()

    return render(request, 'tourney/index.html', {'formset':formset, 'related_players':related_players,
                'matches':matches})



class MatchUpdateView(UpdateView):
    model = MatchModel
    fields = ['score1', 'score2']
    template_name = 'tourney/match_update.html'
