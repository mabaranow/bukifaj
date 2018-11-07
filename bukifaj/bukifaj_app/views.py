from django.shortcuts import render
from django.http import HttpResponse


def dashboard(request):
    return render(request, 'dashboard.html')


def library(request):
    return render(request, 'library.html')


def friends(request):
    return render(request, 'friends.html')
