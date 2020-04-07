from django.contrib import admin
from .models import TournamentModel, PlayerModel, MatchModel
# Register your models here.

admin.site.register(TournamentModel)
admin.site.register(PlayerModel)
admin.site.register(MatchModel)