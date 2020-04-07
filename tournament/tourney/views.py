from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from tourney.forms import TorunamentForm, PlayerForm, TournamentPlayerFormSet
from tourney.models import TournamentModel, PlayerModel, MatchModel
from django.forms import modelformset_factory, inlineformset_factory


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
    related_players = PlayerModel.objects.filter(tournament=tournament)

    return render(request, 'tourney/index.html', {'formset':formset, 'related_players':related_players,
                })

