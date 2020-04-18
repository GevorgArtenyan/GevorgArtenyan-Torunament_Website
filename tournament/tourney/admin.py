from django.contrib import admin
from .models import TournamentModel, PlayerModel, PlayerLeagueModel, MatchModel, GameModel
# Register your models here.

admin.site.register(TournamentModel)
admin.site.register(PlayerModel)
admin.site.register(PlayerLeagueModel)
admin.site.register(MatchModel)
admin.site.register(GameModel)