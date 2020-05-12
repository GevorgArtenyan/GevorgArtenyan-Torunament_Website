from django.urls import path
from . import views
from .views import game_update, PlayerAPIListView, TournamentCreateView

urlpatterns = [
    path('about/', views.about, name='about'),
    path('tournament/<int:pk>/', views.detail, name='detail'),
    path('', views.my_tournaments, name='home'),
    path('all_tournaments', views.tournamentlistview, name='all_tournaments'),
    path('game/<int:pk>/', game_update, name='game_update'),
    path('playerapi/', views.PlayerAPIListView.as_view(), name='player_list'),
    path('matchapi/', views.MatchAPIListView.as_view(), name='match_list'),
    path('create_tournament/', TournamentCreateView.as_view(), name='create_tournament'),
]
