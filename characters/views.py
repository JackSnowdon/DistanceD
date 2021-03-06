from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
import math

# Create your views here.

@login_required
def sheet_index(request):
    profile = request.user.profile
    sheets = profile.sheets.all()
    return render(request, "sheet_index.html", {"sheets": sheets})


@login_required
def add_base(request):
    if request.method == "POST":
        base_form = BaseForm(request.POST)
        if base_form.is_valid():
            profile = request.user.profile
            form = base_form.save(commit=False)
            form.created_by = profile
            form.save()
            messages.error(request, 'Created {0}'.format(form.name), extra_tags='alert')
            return redirect("sheet_index")
    else:
        base_form = BaseForm()
    return render(request, "add_base.html", {"base_form": base_form})


@login_required
def edit_base(request, pk):
    this_sheet = get_object_or_404(Base, pk=pk)
    profile = request.user.profile
    if profile == this_sheet.created_by or profile.staff_access:
        if request.method == "POST":
            base_form = BaseForm(request.POST, instance=this_sheet)
            if base_form.is_valid():
                form = base_form.save(commit=False)
                form.save()
                messages.error(
                    request, "Edited {0}".format(form.name), extra_tags="alert"
                )
                return redirect("sheet_index")
        else:
            base_form = BaseForm(instance=this_sheet)
        return render(
            request,
            "edit_base.html",
            {"base_form": base_form, "this_sheet": this_sheet},
        )
    else:
        messages.error(
            request, "You Don't Have The Required Permissions", extra_tags="alert"
        )
        return redirect("sheet_index")


@login_required
def view_base(request, pk):
    profile = request.user.profile
    this_base = get_object_or_404(Base, pk=pk)
    if profile == this_base.created_by or profile.staff_access:
        mod = return_ability_modifiers(this_base)
        return render(request, "view_base.html", {"this_base": this_base, "mod": mod})
    else:
        messages.error(
            request, "You Don't Have The Required Permissions", extra_tags="alert"
        )
        return redirect("sheet_index")
    

@login_required
def delete_base(request, pk):
    this_sheet = get_object_or_404(Base, pk=pk)
    profile = request.user.profile
    if profile == this_sheet.created_by or profile.staff_access:
        this_sheet.delete()
        messages.error(
            request, f"Deleted {this_sheet.name}", extra_tags="alert"
        )
        return redirect(reverse("sheet_index"))
    else:
        messages.error(
            request, "You Don't Have The Required Permissions", extra_tags="alert"
        )
        return redirect("sheet_index")


# Helper Functions


def return_ability_modifiers(b):
    """
    Takes a signle Base object
    returns a dict with "str_mod" for strengh mod etc 
    """
    modifiers = []
    str_mod = math.floor((b.strengh - 10) / 2)
    dex_mod = math.floor((b.dexterity - 10) / 2)
    con_mod = math.floor((b.constitution - 10) / 2)
    int_mod = math.floor((b.intelligence - 10) / 2)
    wis_mod = math.floor((b.wisdom - 10) / 2)
    cha_mod = math.floor((b.charisma - 10) / 2)
    stringList = ["str_mod", "dex_mod", "con_mod", "int_mod", "wis_mod", "cha_mod"]
    modifiers.extend((str_mod, dex_mod, con_mod, int_mod, wis_mod, cha_mod))
    zipped = zip(stringList, modifiers)
    dictMod = dict(zipped)
    return dictMod