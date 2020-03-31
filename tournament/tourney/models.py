from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class TournamentModel(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    players = models.CharField(max_length=2000)
    date_created = models.DateTimeField(default=timezone.now())

    def get_absolute_url(self):
        return f'/tournament/{self.pk}/'
