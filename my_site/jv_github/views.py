
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.http import request
from django.views.generic import ListView
from django.core.exceptions import ObjectDoesNotExist

# Local imports
from .models import RepositoryShort, User
from .signals import GithubModelSignals

# Create your views here.
def index(request):
    return render(request, 'jv_github/index.html', context={})

class IndexView(ListView):
    model = RepositoryShort
    template_name = 'jv_github/index.html' # Explicit template
    context_object_name = 'object_list'

    def get_queryset(self):
        """Return all RepositoryShort models associated with a specific github
        User"""
        # First get the user associated with 'username'
        github_username = self.kwargs.get('github_username', None)
        try:
            user = User.objects.get(username__exact=github_username)
            user_id = user.id
            # Return a list of RepositoryShort models to be rendered into a template
            repo_list = user.repositoryshort_set.all().filter(repo_show=True)

        except ObjectDoesNotExist:
            # Try and create a user
            GithubModelSignals.send_create_user_signal(github_username=github_username)
            # Return an empty queryset
            # While rendering the template indicate that no repositories exist for 
            # This user
            repo_list = RepositoryShort.objects.none()

        # Send a signal to update the models after each query
        GithubModelSignals.send_update_signal(github_username=github_username)

        return repo_list