from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserForm
from .algo import Handler


def hello_world(request):
    return render(request, 'index.html')


def handle(s):
    label = int(Handler.model(s))
    if label > 6:
        tone = 'positive'
    elif label < 5:
        tone = 'negative'
    else:
        tone = 'neutral'
    return label, tone


def index(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        label = handle(request.POST.get('review'))
        return render(request, "index.html", {"form": form,
                                              "label": f'Score: {label[0]}, sentiment: {label[1]}'})
    else:
        userform = UserForm()
        return render(request, "index.html", {"form": userform, "label": ''})
