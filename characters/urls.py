from django.urls import path
from .views import *

urlpatterns = [
    path('sheet_index/', sheet_index, name="sheet_index"),
    path('add_base/', add_base, name="add_base"),
    path(r'edit_base/<int:pk>/', edit_base, name="edit_base"),
    path(r'view_base/<int:pk>/', view_base, name="view_base"),
    path(r'delete_base/<int:pk>/', delete_base, name="delete_base"),
]