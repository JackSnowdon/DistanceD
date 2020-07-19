from django.urls import path
from .views import *

urlpatterns = [
    path('game_index/', game_index, name="game_index"),
    path('new_combat_instance/', new_combat_instance, name="new_combat_instance"),
    path(r'enter_combat/<int:pk>/', enter_combat, name="enter_combat"),
    path(r'delete_combat/<int:pk>/', delete_combat, name="delete_combat"),
    path(r'add_combat_member/<int:pk>/', add_combat_member, name="add_combat_member"),
    path(r'edit_combat_member/<int:pk>/', edit_combat_member, name="edit_combat_member"),
    path(r'delete_combat_member/<int:pk>/', delete_combat_member, name="delete_combat_member"),
    path(r'start_combat/<int:pk>/', start_combat, name="start_combat"),
    path(r'end_combat/<int:pk>/', end_combat, name="end_combat"),
    path(r'next_turn/<int:pk>/', next_turn, name="next_turn"),
]