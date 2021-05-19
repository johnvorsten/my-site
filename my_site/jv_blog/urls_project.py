from django.urls import path
from . import views

app_name = 'projects'
urlpatterns = [
    path('', view=views.ProjectIndexView.as_view(), name='index'), # landing page
    path('<slug:slug>/', view=views.ProjectDetail.as_view(), name='project_detail'),
]