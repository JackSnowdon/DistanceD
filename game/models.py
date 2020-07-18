from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from characters.models import *
from accounts.models import Profile

# Create your models here.

class GameInstance(models.Model):
    name = models.CharField(max_length=255)
    dm = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class GameSheet(models.Model):
    base = models.ForeignKey(Base, related_name='game_instances', on_delete=models.PROTECT)
    initiative = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(30)], default=0)
    current_hit_points = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000)], default=0)
    game = models.ForeignKey(GameInstance, related_name='sheets', on_delete=models.PROTECT)

    def __str__(self):
        return self.base.name


class CombatInstance(models.Model):
    name = models.CharField(max_length=255)
    dm = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class CombatMember(models.Model):
    name = models.CharField(max_length=255)
    initiative = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(30)], default=0)
    current_hit_points = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000)], default=0)
    max_hit_points = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000)], default=0)
    game = models.ForeignKey(CombatInstance, related_name='sheets', on_delete=models.PROTECT)
    enemy = models.BooleanField(default=False)

    def __str__(self):
        return self.name
