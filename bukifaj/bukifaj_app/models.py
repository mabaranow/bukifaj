from django.db import models
from django.contrib.auth.models import User


class BukifajUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        db_table = 'bukifaj_user'


class Creator(models.Model):
    AUTHOR = 0
    TRANSLATOR = 1
    CREATOR_TYPE = (
        (AUTHOR, 'author'),
        (TRANSLATOR, 'translator'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    type = models.IntegerField(choices=CREATOR_TYPE, default=0)

    def __str__(self):
        return "{0} {1} - {2}".format(self.first_name, self.last_name, self.type)

    class Meta:
        db_table = 'creator'


class Publisher(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'publisher'


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Creator, on_delete=models.CASCADE)

    def __str__(self):
        return "'{0}' {1}".format(self.title, self.author)

    class Meta:
        db_table = 'book'


class BookEdition(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    translator = models.ForeignKey(Creator, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    publication_date = models.IntegerField(blank=True, null=True)
    isbn = models.CharField(max_length=13)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    pages = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "{0} {1}".format(self.book, self.isbn)

    class Meta:
        db_table = 'book_edition'


class BukifajUsersBook(models.Model):
    bukifaj_user = models.ForeignKey(BukifajUser, on_delete=models.CASCADE)
    book = models.ForeignKey(BookEdition, on_delete=models.CASCADE)
    was_read = models.BooleanField(default=False)

    def __str__(self):
        return "{0} {1}".format(self.bukifaj_user, self.book)

    class Meta:
        db_table = 'bukifaj_users_book'

