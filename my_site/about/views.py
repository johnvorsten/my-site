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

    try:
        profile = Profile.objects.get(first_name__exact=profile_name_first,
            last_name__exact=profile_name_last)
    except ObjectDoesNotExist:
        raise Http404('User does not exist')

    skill_set = profile.skills_set.all()
    project_set = profile.projects_set.all()
    context = {
        'profile':profile,
        'skill_set':skill_set,
        'project_set':project_set}
        
    return render(request, 'about/about.html', context=context)