from django.contrib import admin
from django.urls import path, include

from bukifaj_app.views import home, signup, dashboard, library, friends

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard/', dashboard, name='dashboard'),
    path('library/', library, name='library'),
    path('friends/', friends, name='friends'),
]