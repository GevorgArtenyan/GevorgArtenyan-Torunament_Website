from django.urls import path
from . import views
from .views import TournamentListView, game_update, PlayerAPIListView

urlpatterns = [
    path('tournament/<int:pk>/', views.index, name='index'),
    path('', TournamentListView.as_view(), name='home'),
    path('game/<int:pk>/', game_update, name='game_update'),
    path('api/', views.PlayerAPIListView.as_view(), name='unit_list'),
]
