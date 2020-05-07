from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from .models import TournamentModel, PlayerLeagueModel, MatchModel, GameModel
from django.forms import inlineformset_factory
from .serializers import PlayerSerializer, MatchSerializer
from rest_framework import generics
from .table import table, match_calc, sort_table, head_to_head_winner
from .forms import GameForm, TournamentForm
from .forms import TournamentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

class PlayerAPIListView(generics.ListAPIView):
    lookup_field = 'pk'
    queryset = PlayerLeagueModel.objects.all()
    serializer_class = PlayerSerializer

class MatchAPIListView(generics.ListAPIView):
    lookup_field = 'pk'
    queryset = MatchModel.objects.all()
    serializer_class = MatchSerializer

class TournamentCreateView(LoginRequiredMixin, CreateView):
    form_class = TournamentForm
    template_name = 'tourney/create_tournament.html'

    def form_valid(self, form):
        form.instance.host = self.request.user
        return super().form_valid(form)

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
    related_players = PlayerLeagueModel.objects.filter(tournament=tournament)
    matches = MatchModel.objects.filter(player1__in=related_players)
    games = GameModel.objects.filter(home_player__in=related_players).order_by('pk')
    match_calc(games)
    table(related_players, games)
    related_players = sort_table(PlayerLeagueModel.objects.filter(tournament=tournament))

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

@login_required
def game_update(request, pk):
    game = get_object_or_404(GameModel, pk=pk)
    if request.user == game.tournament.host:
        if request.method == 'POST':
            form = GameForm(request.POST, instance=game)
        else:
            form = GameForm(instance=game)
        return save_game_form(request, form, 'tourney/partials/partial_game_update.html')




