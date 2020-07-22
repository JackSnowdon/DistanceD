from django.urls import path
from .views import *

urlpatterns = [
    path('game_index/', game_index, name="game_index"),
    path('new_game_instance/', new_game_instance, name="new_game_instance"),
    path(r'enter_game/<int:pk>/', enter_game, name="enter_game"),
    path(r'delete_game/<int:pk>/', delete_game, name="delete_game"),
]