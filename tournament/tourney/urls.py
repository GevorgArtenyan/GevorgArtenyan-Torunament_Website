from django.urls import path
from .views import TournamentListView, TournamentCreateView, TournamentDetailView

urlpatterns = [
    path('',  TournamentListView.as_view(), name='home'),
    path('create/',  TournamentCreateView.as_view(), name='create'),
    path('tournament/<int:pk>/',  TournamentDetailView.as_view(), name='detail'),
]
