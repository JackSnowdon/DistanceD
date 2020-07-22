from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from characters.models import *
from accounts.models import Profile
from characters.models import *

# Create your models here.

class GameInstance(models.Model):
    name = models.CharField(max_length=255)
    dm = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class GameSheet(models.Model):
    base = models.ForeignKey(Base, related_name='current_games', on_delete=models.CASCADE)
    current_hit_points = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000)], default=0)
    game = models.ForeignKey(GameInstance, related_name='sheets', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.base.name} Sheet in {self.game}"

