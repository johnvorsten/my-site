from django.urls import path
from . import views

app_name = 'projects'
urlpatterns = [
    path('', view=views.IndexView.as_view(), name='index'), # landing page
    path('<slug:slug>/', view=views.EntryDetail.as_view(), name='entry_detail'), # Match an article name
]