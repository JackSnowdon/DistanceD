from django.shortcuts import render

# Create your views here.

def sheet_index(request):
    return render(request, "sheet_index.html")