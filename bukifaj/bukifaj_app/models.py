from django.db import models
from django.contrib.auth.models import User


class BukifajUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        db_table = 'bukifaj_user'


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    class Meta:
        db_table = 'author'


class Publisher(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'publisher'


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    publication_date = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    pages = models.IntegerField(blank=True, null=True)
    was_read = models.BooleanField(default=False)

    def __str__(self):
        return "'{0}' {1}".format(self.title, self.author)

    class Meta:
        db_table = 'book'
