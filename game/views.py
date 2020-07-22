from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

# Create your views here.

@login_required
def game_index(request):
    games = GameInstance.objects.order_by("name")
    return render(request, "game_index.html", {"games": games})


@login_required
def new_game_instance(request):
    if request.method == "POST":
        game_form = NewGameInstance(request.POST)
        if game_form.is_valid():
            form = game_form.save(commit=False)
            form.dm = request.user.profile
            form.save()
            messages.error(request, "Started {0}".format(form.name), extra_tags="alert")
            return redirect("game_index")
    else:
        game_form = NewGameInstance()
    return render(request, "new_game_instance.html", {"game_form": game_form})