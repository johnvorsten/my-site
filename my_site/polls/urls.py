# Django imports
from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results', views.ResultsView.as_view(), name='results'),
    path('<int:pk>/vote', views.vote, name='vote')
]

# Legacy... before default templates
# urlpatterns = [
#     path('', views.index, name='index'),
#     path('<int:pk>/', views.detail, name='detail'),
#     path('<int:pk>/results', views.results, name='results'),
#     path('<int:pk>/vote', views.vote, name='vote')
# ]