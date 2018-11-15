from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from bukifaj_app.forms import UsersProfilePicForm, AddBookForm
from bukifaj_app.models import BukifajUser, Book
from django.http import JsonResponse
from django.template.loader import render_to_string


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            created_user = form.save()
            BukifajUser.objects.create(user=created_user)
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {
        'form': form
    })


def upload_file(request):
    user = request.user.bukifajuser
    if request.method == 'POST':
        form = UsersProfilePicForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        form = UsersProfilePicForm()
    return render(request, 'profile/profile_pic_upload_form.html', {
        'form': form
    })


@login_required
def dashboard(request):
    return render(request, 'profile/dashboard.html')


@login_required
def library(request):
    books = Book.objects.all()
    return render(request, 'profile/library.html', {
        'books': books
    })


def add_book(request):
    data = dict()

    if request.method == 'POST':
        form = AddBookForm(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = AddBookForm()

    context = {'form': form}
    data['html_form'] = render_to_string('profile/add_book_form_modal.html',
        context,
        request=request
    )
    return JsonResponse(data)


@login_required
def friends(request):
    return render(request, 'profile/friends.html')

