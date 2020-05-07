from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from django.urls import reverse

POS_PRIORITY = (
    ('Goal Difference', 'Goal Difference'),
    ('Head to Head Matches', 'Head to Head Matches')
)


class TournamentModel(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    game = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    position_priority = models.CharField(max_length=150, choices=POS_PRIORITY, default='1')

    def get_absolute_url(self):
        return f'/tournament/{self.pk}/'

    def __str__(self):
        return self.name

class PlayerModel(models.Model):
    name = models.CharField(max_length=130)
    tournament = models.ForeignKey(TournamentModel, models.CASCADE)


    def __str__(self):
        return self.name

class PlayerLeagueModel(PlayerModel):
    points = models.PositiveIntegerField(default=0)
    games_played = models.PositiveIntegerField(default=0)
    wins = models.PositiveIntegerField(default=0)
    draws = models.PositiveIntegerField(default=0)
    defeats = models.PositiveIntegerField(default=0)
    goals_scored = models.PositiveIntegerField(default=0)
    goals_conceded = models.PositiveIntegerField(default=0)
    goal_difference = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class MatchModel(models.Model):
    player1 = models.ForeignKey(PlayerLeagueModel, on_delete=models.CASCADE, related_name='player1')
    player2 = models.ForeignKey(PlayerLeagueModel, on_delete=models.CASCADE, related_name='player2')
    score1 = models.PositiveIntegerField(null=True, blank=True)
    score2 = models.PositiveIntegerField(null=True, blank=True)
    winner = models.ForeignKey(PlayerLeagueModel, null=True, blank=True, on_delete=models.CASCADE, related_name='winner')
    loser = models.ForeignKey(PlayerLeagueModel, null=True, blank=True, on_delete=models.CASCADE, related_name='loser')

    def __str__(self):
        return f"{self.player1} {self.score1}:{self.score2} {self.player2}"


class GameModel(models.Model):
    tournament = models.ForeignKey(TournamentModel, on_delete=models.CASCADE)
    match = models.ForeignKey(MatchModel, on_delete=models.CASCADE)
    home_player = models.ForeignKey(PlayerLeagueModel, on_delete=models.CASCADE, related_name='home_player')
    away_player = models.ForeignKey(PlayerLeagueModel, on_delete=models.CASCADE, related_name='away_player')
    h_score = models.PositiveIntegerField(null=True, blank=True)
    a_score = models.PositiveIntegerField(null=True, blank=True)
    def __str__(self):
        return f"{self.home_player} {self.h_score}:{self.a_score} {self.away_player}"

    def get_absolute_url(self):
        return reverse('game-update', kwargs={'pk': self.pk})

def save_player(sender, instance, **kwargs):
    for i in PlayerLeagueModel.objects.all():
        if i.tournament == instance.tournament and i != instance:
            m = MatchModel.objects.create(player1=instance, player2=i, score1=0, score2=0)
            h = GameModel.objects.create(tournament=instance.tournament, match=m, home_player=instance, away_player=i)
            a = GameModel.objects.create(tournament=instance.tournament, match=m, home_player=i, away_player=instance)
            m.save()
            h.save()
            a.save()

post_save.connect(save_player, sender=PlayerLeagueModel)

