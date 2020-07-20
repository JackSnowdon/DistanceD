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
    combat_members = this_combat.sheets.order_by("-initiative")
    if this_combat.combat_state == False:
        return render(request, "enter_combat.html", {"this_combat": this_combat, "combat_members": combat_members})
    else:
        turnee = combat_members.filter(turn_state=True)
        if turnee[0].enemy == False:
            allies = combat_members.filter(enemy=False)
            enemies = combat_members.filter(enemy=True)
        else:
            allies = combat_members.filter(enemy=True)
            enemies = combat_members.filter(enemy=False)
        return render(request, "enter_combat.html", {"this_combat": this_combat, "combat_members": combat_members,
                        "turnee": turnee, "allies": allies, "enemies": enemies})


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


@login_required
def add_combat_member(request, pk):
    this_combat = get_object_or_404(CombatInstance, pk=pk)
    if request.method == "POST":
        combat_form = NewCombatMember(request.POST)
        if combat_form.is_valid():
            form = combat_form.save(commit=False)
            if form.current_hit_points > form.max_hit_points:
                messages.error(request, f"Current HP ({form.current_hit_points}) can't exceed Max HP ({form.max_hit_points})", extra_tags="alert")
            else:
                if form.current_hit_points == 0:
                    form.current_hit_points = form.max_hit_points
                form.game = this_combat
                form.save()
                messages.error(request, "Added {0}".format(form.name), extra_tags="alert")
                return redirect("enter_combat", this_combat.pk)
    else:
        combat_form = NewCombatMember()
    return render(request, "add_combat_member.html", {"combat_form": combat_form, "this_combat": this_combat })


@login_required
def edit_combat_member(request, pk):
    this_member = get_object_or_404(CombatMember, pk=pk)
    this_combat = this_member.game
    profile = request.user.profile
    if profile == this_combat.dm or profile.staff_access:
        if request.method == "POST":
            combat_form = NewCombatMember(request.POST, instance=this_member)
            if combat_form.is_valid():
                form = combat_form.save(commit=False)
                if form.current_hit_points > form.max_hit_points:
                    messages.error(request, f"Current HP ({form.current_hit_points}) can't exceed Max HP ({form.max_hit_points})", extra_tags="alert")
                else:
                    if form.current_hit_points == 0:
                        form.current_hit_points = form.max_hit_points
                    form.game = this_combat
                    form.save()
                    messages.error(request, "Edited {0}".format(form.name), extra_tags="alert")
                    return redirect("enter_combat", this_combat.pk)
        else:
            combat_form = NewCombatMember(instance=this_member)
        return render(request, "edit_combat_member.html", {"combat_form": combat_form, "this_combat": this_combat, "this_member": this_member })
    else:
        messages.error(
            request, "You Don't Have The Required Permissions", extra_tags="alert"
        )
        return redirect("enter_combat", this_combat.pk)


@login_required
def delete_combat_member(request, pk):
    this_member = get_object_or_404(CombatMember, pk=pk)
    this_combat = this_member.game
    profile = request.user.profile
    if profile == this_combat.dm or profile.staff_access:
        this_member.delete()
        messages.error(
            request, f"Deleted {this_member.name} from {this_combat}", extra_tags="alert"
        )
        return redirect("enter_combat", this_combat.pk)
    else:
        messages.error(
            request, "You Don't Have The Required Permissions", extra_tags="alert"
        )
        return redirect("enter_combat", this_combat.pk)

    
@login_required
def start_combat(request, pk):
    this_combat = get_object_or_404(CombatInstance, pk=pk)
    profile = request.user.profile
    if profile == this_combat.dm or profile.staff_access:
        combat_members = this_combat.sheets.order_by("-initiative")
        this_combat.combat_state = True
        this_combat.save()
        first = combat_members[0]
        first.turn_state = True
        first.save()
    else:
        messages.error(
            request, "You Don't Have The Required Permissions", extra_tags="alert"
        )
    return redirect("enter_combat", this_combat.pk)


@login_required
def end_combat(request, pk):
    profile = request.user.profile
    this_combat = get_object_or_404(CombatInstance, pk=pk)
    if profile == this_combat.dm or profile.staff_access:
        combat_members = this_combat.sheets.order_by("-initiative")
        this_combat.combat_state = False
        this_combat.save()
        for c in combat_members:
            c.turn_state = False
            c.save()
    else:
        messages.error(
            request, "You Don't Have The Required Permissions", extra_tags="alert"
        )
    return redirect("enter_combat", this_combat.pk)


@login_required
def next_turn(request, pk):
    profile = request.user.profile
    this_combat = get_object_or_404(CombatInstance, pk=pk)
    if profile == this_combat.dm or profile.staff_access:
        combat_members = this_combat.sheets.order_by("-initiative")
        battle_size = combat_members.count()
        current_go = 0
        next_go = 0
        for c in combat_members:
            current_go += 1
            if c.turn_state == True:
                next_go = current_go
                c.turn_state = False
                c.save()
        if next_go == battle_size:
            first = combat_members[0]
            first.turn_state = True
            first.save()
        else:
            turnee = combat_members[next_go]
            turnee.turn_state = True
            turnee.save()
    else:
        messages.error(
            request, "You Don't Have The Required Permissions", extra_tags="alert"
        )
    return redirect("enter_combat", this_combat.pk)


@login_required
def attack(request, pk, attacker):
    profile = request.user.profile
    this_combat = get_object_or_404(CombatInstance, pk=pk)
    if profile == this_combat.dm or profile.staff_access:
        if request.method == "POST":
            damage = request.POST.get("damage")
            target = request.POST.get("target")
            
    else:
        messages.error(
            request, "You Don't Have The Required Permissions", extra_tags="alert"
        )
    return redirect("enter_combat", this_combat.pk)


