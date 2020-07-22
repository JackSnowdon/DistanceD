from django.urls import path
from .views import *

urlpatterns = [
    path('game_index/', game_index, name="game_index"),
    path('new_game_instance/', new_game_instance, name="new_game_instance"),
    path(r'enter_game/<int:pk>/', enter_game, name="enter_game"),
    path(r'delete_game/<int:pk>/', delete_game, name="delete_game"),
    path(r'add_game_sheet/<int:pk>/', add_game_sheet, name="add_game_sheet"),
    path(r'edit_game_sheet/<int:pk>/', edit_game_sheet, name="edit_game_sheet"),
    path(r'delete_game_sheet/<int:pk>/', delete_game_sheet, name="delete_game_sheet"),
    path(r'add_own_sheet/<int:pk>/', add_own_sheet, name="add_own_sheet"),
]