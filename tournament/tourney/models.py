from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save, pre_save



class TournamentModel(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return f'/tournament/{self.pk}/'

    def __str__(self):
        return self.name

class PlayerModel(models.Model):
    name = models.CharField(max_length=150)
    tournament = models.ForeignKey(TournamentModel, models.CASCADE)
    points = models.PositiveIntegerField(default=0)
    games_played = models.PositiveIntegerField(default=0)
    wins = models.PositiveIntegerField(default=0)
    draws = models.PositiveIntegerField(default=0)
    defeats = models.PositiveIntegerField(default=0)
    goals_scored = models.PositiveIntegerField(default=0)
    goals_conceded = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.name


class MatchModel(models.Model):
    player1 = models.ForeignKey(PlayerModel, on_delete=models.CASCADE, related_name='home_player')
    player2 = models.ForeignKey(PlayerModel, on_delete=models.CASCADE, related_name='away_player')
    score1 = models.PositiveIntegerField(default=0)
    score2 = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.player1} {self.score1}:{self.score2} {self.player2}"

def save_player(sender, instance, **kwargs):
    for i in PlayerModel.objects.all():
        if i.tournament == instance.tournament and i != instance:
            h = MatchModel.objects.create(player1=instance, player2=i)
            a = MatchModel.objects.create(player1=i, player2=instance)
            h.save()
            a.save()

post_save.connect(save_player, sender=PlayerModel)
