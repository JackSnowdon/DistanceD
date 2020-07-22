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
            return redirect("enter_game", form.pk)
    else:
        game_form = NewGameInstance()
    return render(request, "new_game_instance.html", {"game_form": game_form})


@login_required
def enter_game(request, pk):
    this_game = get_object_or_404(GameInstance, pk=pk)
    game_sheets = this_game.sheets.order_by("-initiative")
    return render(request, "enter_game.html", {"this_game": this_game, "game_sheets": game_sheets})


@login_required
def delete_game(request, pk):
    this_game = get_object_or_404(GameInstance, pk=pk)
    profile = request.user.profile
    if profile == this_game.dm or profile.staff_access:
        this_game.delete()
        messages.error(
            request, f"Deleted {this_game.name}", extra_tags="alert"
        )
        return redirect(reverse("game_index"))
    else:
        messages.error(
            request, "You Don't Have The Required Permissions", extra_tags="alert"
        )
        return redirect("game_index")
