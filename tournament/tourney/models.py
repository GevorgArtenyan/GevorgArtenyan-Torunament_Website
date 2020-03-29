from django.db import models
from django.contrib.auth.models import User

class TournamentModel(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)

