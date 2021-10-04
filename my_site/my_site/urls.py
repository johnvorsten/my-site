"""my_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Django imports
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static # serve media files
from django.conf import settings
from django.views.generic.base import RedirectView

# include() allows me to reference other URLconf's
# If the site encounters a url http://site_name/polls/some_poll_1 it will
# Chop off [http://site_name/polls/] and send [some_poll_1] to polls.urls
urlpatterns = [
    path('', RedirectView.as_view(url='about/')),
    path('admin/', admin.site.urls),
    path('blog/', include('jv_blog.urls_blog', namespace='jv_blog')),
    path('projects/', include('jv_blog.urls_project', namespace='projects')),
    path('about/', include('about.urls')),
]

# Files for serving static files
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

# For requesting media files for a template
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)