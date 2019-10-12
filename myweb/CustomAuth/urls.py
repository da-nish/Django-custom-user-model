
from django.urls import path
from . import views


urlpatterns = [
    path('signup', views.dosignup, name=''),
    path('signin', views.dosignin, name=''),
    path('home', views.gohome, name=''),
    path('logout', views.logout, name=''),
    path('', views.gohome, name=''),
]
