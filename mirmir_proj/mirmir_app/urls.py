from django.urls import path
from . import views

app_name = 'mirmir_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('main/', views.main, name='main'),
    path('about/', views.about, name='about'),
    path('mead_club/', views.club, name='club'),
    path('archive/', views.archive, name='archive'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]
