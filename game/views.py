from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

# Create your views here.

@login_required
def game_index(request):
    combats = CombatInstance.objects.order_by("name")
    return render(request, "game_index.html", {"combats": combats})


@login_required
def new_combat_instance(request):
    if request.method == "POST":
        combat_form = NewCombatInstance(request.POST)
        if combat_form.is_valid():
            form = combat_form.save(commit=False)
            form.dm = request.user.profile
            form.save()
            messages.error(request, "Started {0}".format(form.name), extra_tags="alert")
            return redirect("enter_combat", form.pk)
    else:
        combat_form = NewCombatInstance()
    return render(request, "new_combat_instance.html", {"combat_form": combat_form})


@login_required
def enter_combat(request, pk):
    this_combat = get_object_or_404(CombatInstance, pk=pk)
    return render(request, "enter_combat.html", {"this_combat": this_combat})


@login_required
def delete_combat(request, pk):
    this_combat = get_object_or_404(CombatInstance, pk=pk)
    profile = request.user.profile
    if profile == this_combat.dm or profile.staff_access:
        this_combat.delete()
        messages.error(
            request, f"Deleted {this_combat.name}", extra_tags="alert"
        )
        return redirect(reverse("game_index"))
    else:
        messages.error(
            request, "You Don't Have The Required Permissions", extra_tags="alert"
        )
        return redirect("game_index")

