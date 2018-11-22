from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core import serializers

import requests
import re
from itertools import chain

from bukifaj_app.forms import UsersProfilePicForm, AddBookForm, SearchBookForm
from bukifaj_app.models import BukifajUser, Creator, Publisher, Genre, Book, BookEdition, BukifajUsersBook


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
    bukifaj_user = request.user.bukifajuser
    response = requests.get('https://data.bn.org.pl/api/bibs.json?author=Tanizaki&amp;title=Pochwa%C5%82a+cienia')
    bookdata = response.json()
    bookdata = bookdata['bibs'][0]

    users_books = BukifajUsersBook.objects.filter(bukifaj_user=bukifaj_user)
    all_users_books = []
    for item in users_books:
        all_users_books.append({
            'id': item.id,
            'title': item.book_edition.book.title,
            'authors_last_name': item.book_edition.book.author.last_name,
            'authors_first_name': item.book_edition.book.author.first_name,
            'publisher': item.book_edition.publisher.name,
            'publication_date': item.book_edition.publication_date,
            'was_read': item.was_read
        })

    return render(request, 'profile/library.html', {
        'all_users_books': all_users_books,
        'author': bookdata['author'],
        'title': bookdata['title'],
        'publisher': bookdata['publisher'],
        'location': bookdata['location'],
        'isbn': bookdata['isbnIssn'],
        'publication_date': bookdata['publicationYear']
    })


def save_book_form(request, form, template_name):
    data = dict()
    if request.method == 'GET':
        if any(data in ['book_title', 'book_author', 'book_publisher'] for data in request.GET):
            title = request.GET['book_title']
            author = request.GET['book_author']
            publisher = request.GET['book_publisher']
            print(title, author, publisher)
            response = requests.get(
                'https://data.bn.org.pl/api/bibs.json?author={0}&amp;publisher={1}&amp;title={2}'.format(author,
                                                                                                         publisher,
                                                                                                         title))
            bookdata = response.json()
            book_list = []
            for books in bookdata['bibs']:
                library_books = {}
                for key, value in books.items():

                    if key == 'title':
                        potentially_new_title = value
                        print(key, ': ', potentially_new_title)
                        library_books.update({
                            'title': potentially_new_title
                        })
                    if key == 'genre':
                        potentially_new_genre = value
                        existing_genre = Genre.objects.filter(genre=potentially_new_genre)
                        if existing_genre:
                            print('gatunek istnieje')
                        else:
                            new_genre = Genre.objects.create(genre=potentially_new_genre)
                        print(key, ': ', potentially_new_genre)
                        library_books.update({
                            'genre': potentially_new_genre
                        })
                    if key == 'author':
                        new_authors = value.split('. ')
                        creators_list = []
                        for a in new_authors[:-1]:
                            new_creator = re.findall('(\S.*?)(?:\(.*?\)|$)', a)
                            creators_list.append([c.strip().split(';') for c in new_creator])
                        creators_list = list(chain(*creators_list))
                        potentially_new_translator = creators_list[-1][0]
                        potentially_new_authors = list(chain(*creators_list[:-1]))
                        potentially_new_publisher = new_authors[-1].strip('.')
                        print('translator: ', potentially_new_translator)
                        print('authors: ', potentially_new_authors)
                        print('publisher: ', potentially_new_publisher)

                        existing_publisher = Publisher.objects.filter(name=potentially_new_publisher)
                        if existing_publisher:
                            print('wydawnictwo istnieje')
                        else:
                            new_publisher = Publisher.objects.create(name=potentially_new_publisher)


                        translators_last_name, translators_first_name = potentially_new_translator.split(', ')
                        print(translators_first_name, translators_last_name)
                        existing_translator = Creator.objects.filter(first_name=translators_first_name,
                                                                  last_name=translators_last_name,
                                                                  type=0)

                        if existing_translator:
                            print('tłumacz istnieje')
                        else:
                            new_translator = Creator.objects.create(first_name=translators_first_name,
                                                                last_name=translators_last_name, type=1)

                        for i in range(len(potentially_new_authors)):
                            authors_last_name, authors_first_name = potentially_new_authors[i].split(', ')
                            print(authors_first_name, authors_last_name)
                            existing_authors = Creator.objects.filter(first_name=authors_first_name,
                                                                      last_name=authors_last_name,
                                                                      type=0)

                            if existing_authors:
                                print('autor istnieje')
                            else:
                                new_author = Creator.objects.create(first_name=authors_first_name, last_name=authors_last_name, type=0)

                        library_books.update({
                            'author': potentially_new_authors,
                            'translator': potentially_new_translator,
                            'publisher': potentially_new_publisher,
                        })

                    if key == 'isbnIssn':
                        print(key, ': ', value)
                        library_books.update({
                            'isbn_issn': value
                        })
                    if key == 'publicationYear':
                        print(key, ': ', value)
                        library_books.update({
                            'publication_date': value
                        })

                book_list.append(library_books)
                print(len(book_list))









            data['form_is_valid'] = True
            # books = Book.objects.all()
            data['html_book_list'] = render_to_string('profile/library_table.html', {
                # 'books': books
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def add_book(request):
    if request.method == 'POST':
        form = SearchBookForm(request.POST)
    else:
        form = SearchBookForm()
    return save_book_form(request, form, 'profile/add_book_form.html')


def update_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    print(book)
    users_book = BukifajUsersBook.objects.get(book_edition_id=pk)
    print(users_book.id)
    print(book.id)
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
