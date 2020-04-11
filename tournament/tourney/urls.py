from django.urls import path
from . import views
from .views import TournamentListView, MatchUpdateView, PlayerAPIListView

urlpatterns = [
    path('tournament/<int:pk>/', views.index, name='index'),
    path('', TournamentListView.as_view(), name='home'),
    path('match/<int:pk>/', MatchUpdateView.as_view(), name='match-update'),
    path('api/', views.PlayerAPIListView.as_view(), name='unit-list'),

]
