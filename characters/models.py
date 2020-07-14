from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from accounts.models import Profile

# Create your models here.

class Base(models.Model):
    name = models.CharField(max_length=255)
    strengh = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)], default=0)
    dexterity = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)], default=0)
    constitution = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)], default=0)
    intelligence = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)], default=0)
    wisdom = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)], default=0)
    charisma = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)], default=0)
    fellowship = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)], default=0)
    level = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)], default=0)
    max_hit_points = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000)], default=0)
    created_by = models.ForeignKey(Profile, related_name='sheets', on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=255)
    STRENGH = 'STR'
    DEXTERITY = 'DEX'
    CONSTITUTION = 'CON'
    INTELLIGENCE = 'INT'
    WISDOM = 'WIS'
    CHARISMA = 'CHA'
    BASE_STAT_CHOICES = [
        (STRENGH, 'Strengh'),
        (DEXTERITY, 'Dexterity'),
        (CONSTITUTION,  'Constitution'),
        (INTELLIGENCE, 'Intelligence'),
        (WISDOM, 'Wisdom'),
        (CHARISMA, 'Charisma'),
    ]
    base_stat = models.CharField(
        max_length=3,
        choices=BASE_STAT_CHOICES,
        default=STRENGH,
    )
    bonus = models.IntegerField()
    sheet = models.ForeignKey(Base, related_name='skills', on_delete=models.PROTECT)

    def __str__(self):
        return self.name
