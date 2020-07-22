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
    game_sheets = this_game.sheets.all
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


@login_required
def add_game_sheet(request, pk):
    this_game = get_object_or_404(GameInstance, pk=pk)
    if request.method == "POST":
        sheet_form = NewGameSheet(request.POST)
        if sheet_form.is_valid():
            form = sheet_form.save(commit=False)
            if form.current_hit_points > form.base.max_hit_points:
                messages.error(request, f"Current HP ({form.current_hit_points}) can't exceed Max HP ({form.base.max_hit_points})", extra_tags="alert")
                form.current_hit_points = form.base.max_hit_points
            form.game = this_game
            form.save()
            messages.error(request, "Added {0}".format(form.base.name), extra_tags="alert")
            return redirect("enter_game", this_game.pk)
    else:
        sheet_form = NewGameSheet()
    return render(request, "add_game_sheet.html", {"sheet_form": sheet_form, "this_game": this_game})


@login_required
def edit_game_sheet(request, pk):
    this_sheet = get_object_or_404(GameSheet, pk=pk)
    this_game = this_sheet.game
    profile = request.user.profile
    if profile == this_game.dm or profile == this_sheet.base.created_by:
        if request.method == "POST":
            sheet_form = EditSheetHP(request.POST, instance=this_sheet)
            if sheet_form.is_valid():
                form = sheet_form.save(commit=False)
                if form.current_hit_points > this_sheet.base.max_hit_points:
                    messages.error(request, f"Current HP ({form.current_hit_points}) can't exceed Max HP ({this_sheet.base.max_hit_points})", extra_tags="alert")
                else:
                    form.save()
                    messages.error(request, "Edited {0}".format(this_sheet.base.name), extra_tags="alert")
                    return redirect("enter_game", this_game.pk)
        else:
            sheet_form = EditSheetHP(instance=this_sheet)
        return render(request, "edit_game_sheet.html", {"sheet_form": sheet_form, "this_game": this_game, "this_sheet": this_sheet})
    else:
        messages.error(
            request, "You Don't Have The Required Permissions", extra_tags="alert"
        )
        return redirect("enter_game", this_game.pk)


@login_required
def delete_game_sheet(request, pk):
    this_sheet = get_object_or_404(GameSheet, pk=pk)
    this_game = this_sheet.game
    profile = request.user.profile
    if profile == this_game.dm or profile == this_sheet.base.created_by:
        this_sheet.delete()
        messages.error(
            request, f"Deleted {this_sheet.base.name} from {this_game}", extra_tags="alert"
        )
    else:
        messages.error(
            request, "You Don't Have The Required Permissions", extra_tags="alert"
        )
    return redirect("enter_game", this_game.pk)


@login_required
def add_own_sheet(request, pk):
    this_game = get_object_or_404(GameInstance, pk=pk)
    profile = request.user.profile
    if request.method == "POST":
        sheet_form = AddOwnSheet(request.user, request.POST)
        if sheet_form.is_valid():
            form = sheet_form.save(commit=False)
            if form.current_hit_points > form.base.max_hit_points:
                messages.error(request, f"Current HP ({form.current_hit_points}) can't exceed Max HP ({form.base.max_hit_points})", extra_tags="alert")
                form.current_hit_points = form.base.max_hit_points
            form.game = this_game
            form.save()
            messages.error(request, "Added {0}".format(form.base.name), extra_tags="alert")
            return redirect("enter_game", this_game.pk)
    else:
        sheet_form = AddOwnSheet(request.user)
    return render(request, "add_game_sheet.html", {"sheet_form": sheet_form, "this_game": this_game})

