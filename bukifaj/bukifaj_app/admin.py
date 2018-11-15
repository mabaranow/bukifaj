from django.contrib import admin
from bukifaj_app.models import BukifajUser, Author, Publisher, Book

admin.site.register(BukifajUser)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Book)
