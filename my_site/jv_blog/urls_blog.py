from django.urls import path
from . import views

app_name = 'jv_blog'
urlpatterns = [
    path('', view=views.BlogIndexView.as_view(), name='index'), # landing page
    path('<slug:slug>/', view=views.BlogDetail.as_view(), name='entry_detail'), # Match an article name
]