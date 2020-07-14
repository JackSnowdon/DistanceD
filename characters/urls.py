from django.urls import path
from .views import *

urlpatterns = [
    path('sheet_index/', sheet_index, name="sheet_index"),
]