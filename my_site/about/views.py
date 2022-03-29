# Django imports
from django.shortcuts import render, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

# Python imports

# Third party imports

# Local imports
from .models import Profile


# Create your views here.
def about_me(request, profile_name_first='john', profile_name_last='vorsten'):
    """Return a static rendering of a profile about page"""
    return render(request, 'about/about.html', context=None)