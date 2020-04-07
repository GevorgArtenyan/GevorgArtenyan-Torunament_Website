from django.urls import path
from . import views
from .views import TournamentListView

urlpatterns = [
    path('tournament/<int:pk>/', views.index, name='index'),
    path('', TournamentListView.as_view(), name='home'),
]
