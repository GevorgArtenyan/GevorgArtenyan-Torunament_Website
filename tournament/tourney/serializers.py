from .models import PlayerModel, PlayerLeagueModel, MatchModel
from rest_framework import serializers

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerLeagueModel
        fields = '__all__'


class MatchSerializer(serializers.ModelSerializer):
    player1 = serializers.StringRelatedField()
    player2 = serializers.StringRelatedField()
    class Meta:
        model = MatchModel
        fields = '__all__'