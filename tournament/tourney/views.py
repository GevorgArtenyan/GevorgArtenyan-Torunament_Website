from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from .models import TournamentModel, PlayerLeagueModel, MatchModel, GameModel
from django.forms import inlineformset_factory
from .serializers import PlayerSerializer
from rest_framework import generics
from .table import table, match_calc, sort_table
from .forms import GameForm
from .forms import TournamentForm
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string

class PlayerAPIListView(generics.UpdateAPIView):
    lookup_field = 'pk'
    queryset = PlayerLeagueModel.objects.all()
    serializer_class = PlayerSerializer


class TournamentListView(ListView):
    model = TournamentModel
    template_name = 'tourney/home.html'


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


def save_game_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            games = GameModel.objects.all()
            data['html_game_list'] = render_to_string('tourney/partials/partial_game_list.html', {
                'games':games
            })
        else:
            data['form_is_valid'] = False
    context = {'form':form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def game_update(request, pk):
    game = get_object_or_404(GameModel, pk=pk)
    if request.method == 'POST':
        form = GameForm(request.POST, instance=game)
    else:
        form = GameForm(instance=game)
    return save_game_form(request, form, 'tourney/partials/partial_game_update.html')

