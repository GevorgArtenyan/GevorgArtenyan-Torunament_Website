from django.urls import path
from . import views
from .views import TournamentListView, game_update, PlayerAPIListView, TournamentCreateView

urlpatterns = [
    path('tournament/<int:pk>/', views.index, name='index'),
    path('', TournamentListView.as_view(), name='home'),
    path('game/<int:pk>/', game_update, name='game_update'),
    path('playerapi/', views.PlayerAPIListView.as_view(), name='player_list'),
    path('matchapi/', views.MatchAPIListView.as_view(), name='match_list'),
    path('create_tournament/', TournamentCreateView.as_view(), name='create_tournament'),
]
