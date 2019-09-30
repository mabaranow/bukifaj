from bukifaj_app.models import Publisher, Creator, Book, BookEdition, BukifajUsersBook


def get_existing_publisher(potentially_new_publisher):
    existing_publisher = Publisher.objects.filter(name=potentially_new_publisher).first()
    return existing_publisher


def get_existing_author(authors_first_name, authors_last_name):
    existing_author = Creator.objects.filter(first_name=authors_first_name,
                                             last_name=authors_last_name,
                                             type=0).first()
    return existing_author


def get_existing_translator(translators_first_name, translators_last_name):
    existing_translators = Creator.objects.filter(first_name=translators_first_name,
                                                  last_name=translators_last_name,
                                                  type=1).first()
    return existing_translators


def get_existing_book(title, genre):
    existing_book = Book.objects.filter(title=title,
                                        genre=genre).first()
    return existing_book


def get_existing_book_edition(book, translator, publisher, publication_date, isbn):
    existing_book_edition = BookEdition.objects.filter(book=book,
                                                       translator=translator,
                                                       publisher=publisher,
                                                       publication_date=publication_date,
                                                       isbn=isbn).first()
    return existing_book_edition


def get_existing_bukifaj_users_book(bukifaj_user, book_edition):
    existing_bukifaj_users_book = BukifajUsersBook.objects.filter(bukifaj_user=bukifaj_user,
                                                                  book_edition=book_edition).first()
    return existing_bukifaj_users_book







