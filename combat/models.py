from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from characters.models import *
from accounts.models import Profile

# Create your models here.

class CombatInstance(models.Model):
    name = models.CharField(max_length=255)
    dm = models.ForeignKey(Profile, on_delete=models.CASCADE)
    combat_state = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class CombatMember(models.Model):
    name = models.CharField(max_length=255)
    initiative = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(30)], default=0)
    current_hit_points = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000)], default=0)
    max_hit_points = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000)], default=0)
    game = models.ForeignKey(CombatInstance, related_name='sheets', on_delete=models.CASCADE)
    turn_state = models.BooleanField(default=False)
    enemy = models.BooleanField(default=False)

    def __str__(self):
        return self.name
