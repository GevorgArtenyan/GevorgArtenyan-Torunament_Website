from django.urls import path
from . import views
from .views import TournamentListView, GameUpdateView, PlayerAPIListView, TournamentUpdateView

urlpatterns = [
    path('tournament/<int:pk>/', views.index, name='index'),
    path('', TournamentListView.as_view(), name='home'),
    path('game/<int:pk>/', GameUpdateView.as_view(), name='game-update'),
    path('api/', views.PlayerAPIListView.as_view(), name='unit-list'),
    path('tournament/<int:pk>/', TournamentUpdateView.as_view(), name='tournament-update'),
]
