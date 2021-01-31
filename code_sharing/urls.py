# newspaper_project/urls.py

from django.contrib import admin
from django.urls import path, include # new


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')), # new
    path('users/', include('django.contrib.auth.urls')), # new
    path('articles/',include('articles.urls')),
    path('', include('pages.urls')), # new
]