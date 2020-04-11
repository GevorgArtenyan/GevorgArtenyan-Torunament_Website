from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from tourney.forms import TorunamentForm, PlayerForm, TournamentPlayerFormSet
from .models import TournamentModel, PlayerModel, MatchModel
from django.forms import modelformset_factory, inlineformset_factory
from django.db.models import Count, F
from django.http import JsonResponse
from django.core import serializers
import json
from django.contrib.auth.models import User
from .serializers import PlayerSerializer
from rest_framework import generics
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

    player_point_dict = {}
    player_games_played_dict = {}
    player_wins_dict = {}
    player_draw_dict = {}
    player_defeat_dict = {}
    player_goal_scored = {}
    player_goal_conceded = {}
    player_goal_difference = {}
    for p in related_players:
        player_point_dict[str(p.pk)] = 0
        player_games_played_dict[str(p.pk)] = 0
        player_wins_dict[str(p.pk)] = 0
        player_draw_dict[str(p.pk)] = 0
        player_defeat_dict[str(p.pk)] = 0
        player_goal_scored[str(p.pk)] = 0
        player_goal_conceded[str(p.pk)] = 0
        player_goal_difference[str(p.pk)] = 1

    # Calculating the points of players. Every victory is 3 points, every draw is 1.
    for m in matches:
        if m.score1 != None and m.score2 != None:
            player_games_played_dict[str(m.player1.pk)] += 1
            player_games_played_dict[str(m.player2.pk)] += 1
            player_goal_scored[str(m.player1.pk)] += m.score1
            player_goal_conceded[str(m.player1.pk)] += m.score2
            player_goal_scored[str(m.player2.pk)] += m.score2
            player_goal_conceded[str(m.player2.pk)] += m.score1

            if m.score1 > m.score2:
                    player_point_dict[str(m.player1.pk)] += 3
                    player_wins_dict[str(m.player1.pk)] += 1
                    player_defeat_dict[str(m.player2.pk)] += 1
            elif m.score1 < m.score2:
                    player_point_dict[str(m.player2.pk)] += 3
                    player_wins_dict[str(m.player2.pk)] += 1
                    player_defeat_dict[str(m.player1.pk)] += 1
            elif m.score1 == m.score2:
                    player_point_dict[str(m.player1.pk)] += 1
                    player_point_dict[str(m.player2.pk)] += 1
                    player_draw_dict[str(m.player1.pk)] += 1
                    player_draw_dict[str(m.player2.pk)] += 1

    for k, v in player_point_dict.items():
        PlayerModel.objects.filter(pk=k).update(points=v)

    for k, v in player_wins_dict.items():
        PlayerModel.objects.filter(pk=k).update(wins=v)

    for k, v in player_draw_dict.items():
        PlayerModel.objects.filter(pk=k).update(draws=v)

    for k, v in player_defeat_dict.items():
        PlayerModel.objects.filter(pk=k).update(defeats=v)

    for k, v in player_games_played_dict.items():
        PlayerModel.objects.filter(pk=k).update(games_played=v)

    for k, v in player_goal_scored.items():
        PlayerModel.objects.filter(pk=k).update(goals_scored=v)

    for k, v in player_goal_conceded.items():
        PlayerModel.objects.filter(pk=k).update(goals_conceded=v)

    for k, v, in player_goal_scored.items():
        for ck, cv in player_goal_conceded.items():
            if k == ck:
                v -= cv
                player_goal_difference[k] = v


    for k, v in player_goal_difference.items():
        PlayerModel.objects.filter(pk=k).update(goal_difference=v)


    #calculating scored and conceded goals by.



    return render(request, 'tourney/index.html', {'formset':formset, 'related_players':related_players,
                'matches':matches})



class MatchUpdateView(UpdateView):
    model = MatchModel
    fields = ['score1', 'score2']
    template_name = 'tourney/match_update.html'
