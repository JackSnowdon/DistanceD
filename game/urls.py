from django.urls import path
from .views import *

urlpatterns = [
    path('game_index/', game_index, name="game_index"),
    path('new_combat_instance/', new_combat_instance, name="new_combat_instance"),
    path(r'enter_combat/<int:pk>/', enter_combat, name="enter_combat"),
    path(r'delete_combat/<int:pk>/', delete_combat, name="delete_combat"),
    path(r'add_combat_member/<int:pk>/', add_combat_member, name="add_combat_member"),
]