from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {
        'form': form
    })


@login_required
def dashboard(request):
    return render(request, 'profile/dashboard.html')


@login_required
def library(request):
    return render(request, 'profile/library.html')


@login_required
def friends(request):
    return render(request, 'profile/friends.html')

