from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(GameInstance)
admin.site.register(GameSheet)
admin.site.register(CombatInstance)
admin.site.register(CombatMember)