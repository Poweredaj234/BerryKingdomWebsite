from django.db import models
from django.conf import settings

class Game(models.Model):
    name = models.CharField(max_length=100)
    is_multiplayer = models.BooleanField(default=False)

class GameSession(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    result = models.CharField(max_length=100)
    stake = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.game.name}: {self.result}"
