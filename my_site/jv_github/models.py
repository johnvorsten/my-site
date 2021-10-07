# Django imports
from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver
from django.conf import settings

# Python imports
import datetime
import urllib.parse
import os

# Third party imports
import requests

# Local imports
from . import models_helper
GITHUB_ACCESS_TOKEN = settings.GITHUB_ACCESS_TOKEN

# Custom exception when a repository has not changed
class RepositoriesNotChanged(Exception):
    pass

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=100)
    avatar_url = models.URLField()
    user_url = models.URLField()
    repositories_url = models.URLField()
    etag = models.CharField(max_length=100)

    def __str__(self):
        return (self.username + ' ' + str(self.id))


class RepositoryShort(models.Model):
    """Field description
    id : Primary key of repository, see github primary key from APIv3
    repo_name : (str) repo name given by github API
    repo_user : (int) user ID that owns this repository"""
    id = models.IntegerField(primary_key=True)
    repo_name = models.CharField(max_length=100)
    repo_user = models.ForeignKey(User, on_delete=models.CASCADE)
    repo_url = models.URLField()
    repo_description = models.TextField(max_length=600)
    repo_description_custom = models.TextField(max_length=1000, blank=True)
    repo_last_update = models.DateTimeField()
    repo_show = models.BooleanField()
    repo_svg = models.CharField(max_length=200,
                                choices=models_helper.SVG_CHOICES,
                                default=(settings.STATIC_URL+'/jv_github','/images'+'/scatter_plot-24px.svg'))

    def __str__(self):
        return (self.repo_name + ' ' + str(self.id))

class Tag(models.Model):
    """Fun tags to associate with each repository. These must be 
    custom entered through the admin interface"""
    tag_text = models.CharField(max_length=20)
    tag_repo = models.ForeignKey(RepositoryShort, on_delete=models.CASCADE)

    def __str__(self):
        return self.tag_text

class UpdateModels:
    """Update GithubRepo models based on the Github API responses
    This class logic should go as follows : 
    1. Check to see if a user is already created in the Django database
    2. Query the github API repositories for a specific user
    3. For each repository under that user create a GithubRepo model.
    The GithubRepo model will be used to display a custom Github page for
    a specific user (user refers to a user defined in Django)
    4. When the GithubRepo model is used there should be a callback to check if 
        the users repositories have been updated. If they have then this class
        should update all repositories under that user"""
    def __init__(self, update_period):
        """inputs
        -------
        update_frequency : (float) number of minutes between updates to 
            prevent frequent calls"""
        self.update_period = datetime.timedelta(update_period)

    def _create_RepositoryShort_model(self, repo_dict):
        """Create GithubRepo models only if the specified user
        has not been created 
        inputs
        -------
        repo_dict (dict) of values to create model with. Dict source is github API is JSON"""

        user = User.objects.get(pk=repo_dict['owner']['id'])

        repo_model = RepositoryShort()
        repo_model.id = repo_dict['id']
        repo_model.repo_name = repo_dict['name']
        repo_model.repo_user = user
        repo_model.repo_url = repo_dict['html_url']
        repo_model.repo_description = repo_dict['description']
        repo_model.repo_last_update = timezone.now()
        if repo_dict['fork'] == True:
            repo_model.repo_show = False
        else:
            repo_model.repo_show = True
        repo_model.save()

        return None

    def _update_RepositoryShort_model(self, repo_model, repo_dict):
        """Update a specific github repo model. Only certain fields will be 
        updated, including name and description. This assumes that other data does not
        change, including user, url, and id
        inputs
        -------
        repo_model : (models.Model) Reference to django model object
        repo_dict : (dict) of values to update model on"""

        repo_model.repo_name = repo_dict['name']
        repo_model.repo_description = repo_dict['description']
        repo_model.repo_last_update = timezone.now()
        repo_model.save()

        return None

    def _create_user(self, owner_dict, etag):
        """Create a user based on information from the repository
        inputs
        -------
        owner_dict : (dict) of values to create user model with
        etag : (str) from Github API response header to be used with subsequent API calls"""
        user = User()
        user.id = owner_dict['id']
        user.username = owner_dict['login']
        user.avatar_url = owner_dict['avatar_url']
        user.user_url = owner_dict['html_url']
        user.repositories_url = urllib.parse.urljoin(owner_dict['html_url'] + '/', '&tab=repositories')
        user.etag = etag
        user.save()
        return None

    def update_models(self, github_username='johnvorsten'):
        """Initiate an update on RepositoryShort models and User models 
        based on the github api results.  
        The query results from the github api will be used to update model fields based on 
        some conditions
        1) Check to see if a user is already created in the Django database. 
           The 'etag' field is used to perform subsequent github queries on a users 
           repositories. Most responses return an ETag header. Many responses also 
           return a Last-Modified header. You can use the values of these headers 
           to make subsequent requests to those resources using the 
           If-None-Match and If-Modified-Since headers, respectively. 
           If the resource has not changed, the server will return a 
           304 Not Modified. Making a conditional request and receiving a 304 response 
           does not count against your Rate Limit, so we encourage you to use it
        2) If no user is created, then create the user based on the github API response
        3) Query the github API repositories for a specific user
        4) The github API has a utility that returns HTTP304 if a users repositories
            have not been updated since the last query
        5) For each repository under that user create a GithubRepo model if not created.
            Otherwise, update the model.
        6) The GithubRepo model will be used to display my custom Github page
            When the GithubRepo model is used there should be a callback to check if 
            the users repositories have been updated. If they have then this class
            should update all repositories under that user
        """
        # Get an etag related to github_username if available
        try: 
            prelim_user = User.objects.get(username__exact=github_username)
            etag_old = prelim_user.etag
            # Get most recent update time of repository
            repos = prelim_user.repositoryshort_set.order_by('-repo_last_update')
            if repos:
                recent_update = repos[0].repo_last_update
            else:
                recent_update = timezone.now() - self.update_period
                # The queryset is empty, and no repositories are associated w/ user
                pass
        except ObjectDoesNotExist:
            # An API call should happen if a user does not exist (and recent update is defined)
            etag_old = None
            recent_update = timezone.now() - self.update_period
            pass

        # Query the github API for changes to the users repository structure
        try: 
            if recent_update <= (timezone.now() - self.update_period):
                response, etag_new = self._query_github(github_username=github_username, etag=etag_old)
                api_result_json = response.json()
            else:
                # Don't update if we recently updated
                return None
        except RepositoriesNotChanged:
            # No changes were detected, use the existing model
            return None
        
        # Iterate through all returned repositories...
        for repo in api_result_json:

            # Decide if I need to create a new user model
            owner_dict = repo['owner']
            try:
                user = User.objects.get(id__exact=owner_dict['id'])
                # Update the user etag each time you do a query
                user.etag = etag_new
                user.save()
            except ObjectDoesNotExist:
                # Create a user
                self._create_user(owner_dict, etag_new)

            # Decide if a new RepositoryShort model is needed
            try:
                repo_model = RepositoryShort.objects.get(id__exact=repo['id'])
                # Update the repo model if it exists
                self._update_RepositoryShort_model(repo_model, repo_dict=repo)
            except ObjectDoesNotExist:
                # Create a RepositoryShort
                self._create_RepositoryShort_model(repo_dict=repo)

        return None

    def create_user(self, github_username):
        """Initiate User models based on the github api results.  This method
        is called as a signal ONLY a specific user requested in the index 
        view cannot be found.  It will : 
        The query results from the github api will be used to create user entries based on 
        some conditions
        1) Check to see if a user is already created in the Django database. The 'etag'
            field is used to perform subsequent github queries on a users repositories
        1.5) If no user is created, then create the user based on the github API response
        2) Query the github API repositories for a specific user
        2.5) The github API has a utility that returns HTTP304 if a users repositories
            have not been updated since the last query
        """
        # Get an etag related to github_username if available
        try: 
            prelim_user = User.objects.get(username__exact=github_username)
            etag_old = prelim_user.etag
        except ObjectDoesNotExist:
            etag_old = None
            pass

        # Query the github API for changes to the users repository structure
        try: 
            response, etag_new = self._query_user(github_username=github_username, etag=etag_old)
        except RepositoriesNotChanged:
            # No changes were detected, use the existing model
            return None
        
        # Decide if I need to create a new user model
        owner_dict = response.json()
        try:
            user = User.objects.get(id__exact=owner_dict['id'])
            # Update the user etag each time you do a query
            user.etag = etag_new
            user.save()
        except ObjectDoesNotExist:
            # Create a user
            self._create_user(owner_dict, etag_new)

        return None
    
    def _query_github(self, github_username='johnvorsten', etag=None):
        """Query the github api for the repositories under 'user' 
        and return the results in json format
        inputs
        -------
        user : (str) name of github user account to update based on
        etag : (str) related to a specific github api request. Used on conditional
            calls to the github API"""

        # User agent - Use the default python requests 
        # connection - I think requests automatically closes after the server
        # Responds.. but close it anyway
        # Accept - Specifically allow version 3 of github API
        user_agent = requests.utils.default_headers()['User-Agent']
        headers = {
                'User-Agent':user_agent,
                'From':'johnvorsten@yahoo.com',
                'Connection':'close',
                'Accept': 'application/vnd.github.v3+json',
                'Authorization': 'token %s' % GITHUB_ACCESS_TOKEN,
                }

        if etag: # Add ETag to header for Github API
            headers['If-None-Match'] = etag

        rate_limit_url = 'https://api.github.com/rate_limit'
        # Repositores from the user associated w/ access token
        repo_url = 'https://api.github.com/user/repos'
        # Repositores from a selected user
        repo_user_url = 'https://api.github.com/users/{}/repos'.format(github_username)

        response = requests.get(repo_user_url, headers=headers)
        if response.status_code == 304: # Response not changed
            raise(RepositoriesNotChanged)
        else:
            # Update the models ETag so it can be checked next time
            etag = response.headers['ETag']

        return (response, etag)

    def _query_user(self, github_username, etag=None):
        """Query the github api for the repositories under 'user' 
        and return the results in json format
        inputs
        -------
        user : (str) name of github user account to update based on
        etag : (str) related to a specific github api request. Used on conditional
            calls to the github API"""

        # User agent - Use the default python requests 
        # connection - I think requests automatically closes after the server
        # Responds.. but close it anyway
        # Accept - Specifically allow version 3 of github API
        user_agent = requests.utils.default_headers()['User-Agent']
        headers = {
                'User-Agent':user_agent,
                'From':'johnvorsten@yahoo.com',
                'Connection':'close',
                'Accept': 'application/vnd.github.v3+json',
                'Authorization': 'token %s' % GITHUB_ACCESS_TOKEN,
                }

        if etag is not None: # Add ETag to header for Github API
            headers['If-None-Match'] = etag

        rate_limit_url = 'https://api.github.com/rate_limit'
        # Search a selected user
        user_url = 'https://api.github.com/users/{}'.format(github_username)

        response = requests.get(user_url, headers=headers)
        if response.status_code == 304: # Response not changed
            raise(RepositoriesNotChanged)
        else:
            # Update the models ETag so it can be checked next time
            etag = response.headers['ETag']

        return (response, etag)

# Don't instantiate a class each time this method is called
updater = UpdateModels(update_period=30)


def update_models(sender, **kwargs):
    """See signals.py for a signal that calls this method
    The signal is sent after a view is rendered for the 
    github index page related to a specific github user, guthub_username
    After each view is rendered, the models are updated.  The idea is to keep
    the models up to date"""
    github_username = kwargs.get('github_username', None)
    updater.update_models(github_username=github_username)
    return None

def create_user(sender, **kwargs):
    """See signals.py for a signal that calls this method
    The signal is sent if there is no user when rendering the github index page"""

    github_username = kwargs.get('github_username', None)
    updater.create_user(github_username)

    return None