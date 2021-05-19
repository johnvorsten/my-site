from django.urls import path
from . import views

app_name = 'jv_github'
urlpatterns = [
    # path('', views.index, {'username':'johnvorsten'}, name='index'), # landing page
    path('', views.IndexView.as_view(), {'github_username':'johnvorsten'}, name='index'), # landing page
]
