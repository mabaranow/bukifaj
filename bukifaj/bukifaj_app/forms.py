from bukifaj_app.models import BukifajUser, Book
from django.forms import ModelForm, Form
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


class SearchBookForm(Form):
    book_title = forms.CharField(max_length=50, required=False)
    book_author = forms.CharField(max_length=50, required=False)
    book_publisher = forms.CharField(max_length=50, required=False)
    book_isbn = forms.CharField(max_length=50, required=False)

    def __init__(self, *args, **kwargs):
        super(SearchBookForm, self).__init__(*args, **kwargs)
        self.fields['book_title'].label = 'Tytuł'
        self.fields['book_author'].label = 'Autor'
        self.fields['book_publisher'].label = 'Wydawnictwo'
        self.fields['book_isbn'].label = 'ISBN'