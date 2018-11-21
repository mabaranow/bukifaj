from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string

from bukifaj_app.forms import UsersProfilePicForm, AddBookForm
from bukifaj_app.models import BukifajUser, Book


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


def save_book_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            books = Book.objects.all()
            data['html_book_list'] = render_to_string('profile/library_table.html', {
                'books': books
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def add_book(request):
    if request.method == 'POST':
        form = AddBookForm(request.POST)
    else:
        form = AddBookForm()
    return save_book_form(request, form, 'profile/add_book_form.html')


def update_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = AddBookForm(request.POST, instance=book)
    else:
        form = AddBookForm(instance=book)
    return save_book_form(request, form, 'profile/update_book_form.html')


def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    data = dict()
    if request.method == 'POST':
        book.delete()
        data['form_is_valid'] = True
        books = Book.objects.all()
        data['html_book_list'] = render_to_string('profile/library_table.html', {
            'books': books
        })
    else:
        context = {'book': book}
        data['html_form'] = render_to_string('profile/delete_book_form.html',
            context,
            request=request,
        )
    return JsonResponse(data)


@login_required
def friends(request):
    return render(request, 'profile/friends.html')

