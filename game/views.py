from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.

@login_required
def game_index(request):
    return render(request, "game_index.html")