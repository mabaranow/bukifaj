from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist

import requests
import re
from itertools import chain
import json, urllib.request

from bukifaj_app.forms import UsersProfilePicForm, AddBookForm, SearchBookForm
from bukifaj_app.models import BukifajUser, Creator, Publisher, Genre, Book, BookEdition, BukifajUsersBook
from bukifaj_app.data_access.queries import get_existing_author, get_existing_book, get_existing_book_edition, \
    get_existing_bukifaj_users_book, get_existing_publisher, get_existing_translator


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
            'author': item.book_edition.book.author,
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
    bukifaj_user = request.user.bukifajuser
    data = dict()
    if request.method == 'GET':
        if any(data in ['book_title', 'book_author', 'book_publisher', 'book_isbn'] for data in request.GET):
            title = request.GET['book_title']
            author = request.GET['book_author']
            publisher = request.GET['book_publisher']
            isbn = request.GET['book_isbn']
            print('wyszukiwanie: ', title, author, publisher, isbn)
            response = requests.get(
                'https://data.bn.org.pl/api/bibs.json?author={0}&amp;publisher={1}&amp;title={2}&amp;isbnIssn={3}' \
                    .format(
                    author,
                    publisher,
                    title,
                    isbn
                ))
            bookdata = response.json()

            raw_authors = bookdata['bibs'][0]['author']
            raw_title = bookdata['bibs'][0]['title']
            raw_isbnIssn = bookdata['bibs'][0]['isbnIssn']
            raw_genre = bookdata['bibs'][0]['genre']
            raw_publication_date = bookdata['bibs'][0]['publicationYear']

            existing_genre = Genre.objects.filter(genre=raw_genre).first()
            if not existing_genre:
                Genre.objects.create(genre=raw_genre)

            new_authors = raw_authors.split('. ')
            creators_list = []

            if len(new_authors) < 2:
                new_creator = re.findall('(\S.*?)(?:\(.*?\)|$)', raw_authors)
                potentially_new_author = new_creator[0]
                authors_last_name, authors_first_name = potentially_new_author.split(', ')
                potentially_new_publisher = new_creator[1].strip('.')

                existing_publisher = get_existing_publisher(potentially_new_publisher)
                existing_author = get_existing_author(authors_first_name, authors_last_name)
                existing_book = get_existing_book(existing_author, raw_title, existing_genre)
                existing_book_edition = get_existing_book_edition(existing_book,
                                                                  existing_publisher,
                                                                  raw_publication_date,
                                                                  raw_isbnIssn)
                existing_bukifaj_users_book = get_existing_bukifaj_users_book(bukifaj_user, existing_book_edition)

                if not existing_publisher:
                    Publisher.objects.create(name=potentially_new_publisher)

                if not existing_author:
                    Creator.objects.create(first_name=authors_first_name,
                                           last_name=authors_last_name,
                                           type=0)

                if not existing_book:
                    Book.objects.create(author=existing_author,
                                        title=raw_title,
                                        genre=existing_genre)

                if not existing_book_edition:
                    BookEdition.objects.create(book=existing_book,
                                               publisher=existing_publisher,
                                               publication_date=raw_publication_date,
                                               isbn=raw_isbnIssn)

                if not existing_bukifaj_users_book:
                    BukifajUsersBook.objects.create(bukifaj_user=bukifaj_user,
                                                    book_edition=existing_book_edition)



            else:
                for a in new_authors[:-1]:
                    new_creator = re.findall('(\S.*?)(?:\(.*?\)|$)', a)
                    creators_list.append([c.strip().split(';') for c in new_creator])
                creators_list = list(chain(*creators_list))
                potentially_new_authors = list(chain(*creators_list[:-1]))
                potentially_new_publisher = new_authors[-1].strip('.')
                translators_last_name, translators_first_name = creators_list[-1][0].split(', ')

                existing_translator = get_existing_translator(translators_first_name, translators_last_name)
                if not existing_translator:
                    existing_translator = Creator.objects.create(first_name=translators_first_name,
                                                                 last_name=translators_last_name,
                                                                 type=1)

                for i in range(len(potentially_new_authors)):
                    authors_last_name, authors_first_name = potentially_new_authors[i].split(', ')

                    existing_publisher = get_existing_publisher(potentially_new_publisher)
                    if not existing_publisher:
                        existing_publisher = Publisher.objects.create(name=potentially_new_publisher)

                    existing_author = get_existing_author(authors_first_name, authors_last_name)
                    if not existing_author:
                        existing_author = Creator.objects.create(first_name=authors_first_name,
                                                                 last_name=authors_last_name,
                                                                 type=0)

                    existing_book = get_existing_book(raw_title, existing_genre)
                    if not existing_book:
                        existing_book = Book.objects.create(
                            title=raw_title,
                            genre=existing_genre)
                        existing_book.author.add(existing_author)
                    else:
                        existing_book.author.add(existing_author)

                    existing_book_edition = get_existing_book_edition(existing_book,
                                                                      existing_translator,
                                                                      existing_publisher,
                                                                      raw_publication_date,
                                                                      raw_isbnIssn)
                    if not existing_book_edition:
                        existing_book_edition = BookEdition.objects.create(book=existing_book,
                                                                           translator=existing_translator,
                                                                           publisher=existing_publisher,
                                                                           publication_date=raw_publication_date,
                                                                           isbn=raw_isbnIssn)

                    existing_bukifaj_users_book = get_existing_bukifaj_users_book(bukifaj_user,
                                                                                  existing_book_edition)
                    if not existing_bukifaj_users_book:
                        BukifajUsersBook.objects.create(bukifaj_user=bukifaj_user,
                                                        book_edition=existing_book_edition)

                print('autorzy :', potentially_new_authors,
                      'wydawca :', potentially_new_publisher,
                      'tytuł :', raw_title,
                      'isbn :', raw_isbnIssn,
                      'data publikacji :', raw_publication_date,
                      'gatunek :', raw_genre
                      )

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
