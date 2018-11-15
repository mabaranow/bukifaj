from django.urls import path, include

from bukifaj_app.views import home, signup, dashboard, library, friends, upload_file, add_book

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard/', dashboard, name='dashboard'),
    path('library/', library, name='library'),
    path('library/add_book', add_book, name='add_book'),
    path('friends/', friends, name='friends'),
    path('upload_file/', upload_file, name='upload_file'),
]