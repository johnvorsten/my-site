from django.urls import path

from . import views

app_name = 'about'
urlpatterns = [
    path('', views.about_me, {'profile_name_first':'John', 'profile_name_last':'Vorsten'}, name='about-me'),
]