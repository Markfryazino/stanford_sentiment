from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserForm


def hello_world(request):
    return render(request, 'index.html')


def handle(s):
    return s.split()[0]


def index(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        label = handle(request.POST.get('review'))
        return render(request, "index.html", {"form": form, "label": label})
    else:
        userform = UserForm()
        return render(request, "index.html", {"form": userform, "label": 'kokkk'})
