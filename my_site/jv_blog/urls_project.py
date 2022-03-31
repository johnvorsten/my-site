# Django imports
from django.urls import path

# Third party imports

# Local imports
from . import views

app_name = 'projects'
urlpatterns = [
    path('', view=views.ProjectIndexView.as_view(), name='index'), # landing page
    path('mil/', view=views.mil, name='mil'),
    path('ranking/', view=views.ranking, name='ranking'),
    path('<slug:slug>/', view=views.ProjectDetail.as_view(), name='project_detail'),
]