from django.contrib import admin
from bukifaj_app.models import BukifajUser, Creator, Publisher, Book, BookEdition, BukifajUsersBook

admin.site.register(BukifajUser)
admin.site.register(Creator)
admin.site.register(Publisher)
admin.site.register(Book)
admin.site.register(BookEdition)
admin.site.register(BukifajUsersBook)
