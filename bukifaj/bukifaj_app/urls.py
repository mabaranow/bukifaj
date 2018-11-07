from django.urls import path

from bukifaj_app.views import dashboard, library, friends

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('library/', library, name='library'),
    path('friends/', friends, name='friends'),
]