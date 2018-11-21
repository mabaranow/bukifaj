from bukifaj_app.models import BukifajUser, Book
from django.forms import ModelForm
from django import forms


class UsersProfilePicForm(ModelForm):
    class Meta:
        model = BukifajUser
        fields = ['profile_pic']


class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author')
        labels = {
            'title': 'Tytuł',
            'author': 'Autor',
        }