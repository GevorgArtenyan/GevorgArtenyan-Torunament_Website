from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from .models import TournamentModel
from .forms import TorunamentForm

class TournamentListView(ListView):
    model = TournamentModel
    template_name = 'tourney/home.html'

class TournamentCreateView(CreateView):
    form_class = TorunamentForm
    template_name = 'tourney/create_tournament.html'

    def form_valid(self, form):
        form.instance.host = self.request.user
        return super(TournamentCreateView, self).form_valid(form)

class TournamentDetailView(DetailView):
    model = TournamentModel
    template_name = 'tourney/tournament_detail.html'
