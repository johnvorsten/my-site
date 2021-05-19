# Django imports
from django.test import TestCase
from django.utils import timezone
from django.conf import settings

# Python imports
import datetime
import urllib.parse
import os

# Local imports
from .models import User, RepositoryShort, UpdateModels
GITHUB_ACCESS_TOKEN = settings.GITHUB_ACCESS_TOKEN

# Third party imports
import requests

# Create your tests here.
class RepositoryShortModelTest(TestCase):

    def test_github_api_access(self):
        """Make sure the github oauth API token is functioning, and 
        I can reach the github API url"""
        # User agent - Use the default python requests 
        # connection - I think requests automatically closes after the server
        # Responds.. but close it anyway
        # Accept - Specifically allow version 3 of github API
        user_agent = requests.utils.default_headers()['User-Agent']
        etag = None
        headers = {
                'User-Agent':user_agent,
                'From':'johnvorsten@yahoo.com',
                'Connection':'close',
                'Accept': 'application/vnd.github.v3+json',
                'Authorization': 'token %s' % GITHUB_ACCESS_TOKEN,
                }

        if etag: # Add ETag to header for Github API
            headers['If-None-Match'] = etag

        # Test connectivity to github API
        response = requests.get('https://api.github.com')
        self.assertTrue(response.status_code == 200)

        return None

    def test_access_token(self):
        
        user_agent = requests.utils.default_headers()['User-Agent']
        headers = {
                'User-Agent':user_agent,
                'From':'johnvorsten@yahoo.com',
                'Connection':'close',
                'Accept': 'application/vnd.github.v3+json',
                'Authorization': 'token %s' % GITHUB_ACCESS_TOKEN,
                }
        rate_limit_url = 'https://api.github.com/rate_limit'
        response = requests.get(rate_limit_url, headers=headers)

        if response.status_code == 401:
            # Invalid access token
            print(response.content)
            raise(ValueError("Bad Credentials"))

        # Unit test
        self.assertTrue(response.status_code == 200)
        self.assertTrue('rate' in response.json().keys())

        return None

    def test_update_models(self):
        """Test the UpdateModels class that populates repositories for a given
        github user
        
        Steps
        1. Attempt to update a github User model, and if it is not created then
           create the model. Because this is a test database, the User will be created
           (see models.py)
        2. Verify that a user is created"""

        github_username = 'johnvorsten'
        updater = UpdateModels(update_period=30)
        updater.update_models(github_username)

        # A user should be created
        myself = User.objects.get(username__exact=github_username)
        my_id = myself.id

        # Several repositories should be created
        repos = RepositoryShort.objects.all()

        # All created repos should have the same id as 'myself'
        # This is a foreign key constraint
        for repo in repos:
            self.assertEqual(repo.repo_user.id, my_id)

        # Make sure the last update field is set
        for repo in repos:
            now = timezone.now()
            upper = now + datetime.timedelta(minutes=1)
            lower = now - datetime.timedelta(minutes=1)
            near_time_bool = all((repo.repo_last_update > lower, repo.repo_last_update < upper))
            self.assertTrue(near_time_bool)

        # Print other info that isn't easily checked (visual check)
        for repo in repos:
            print('Repo ID : ', repo.id)
            print('Name : ', repo.repo_name)
            print('URL : ', repo.repo_url)
            print('Description : ', repo.repo_description)

        return None

    def test_create_RepositoryShort(self):
        """Test basic creation of RepositoryShort model
        Also test creation of basic User"""

        user = User()
        user.id = 1
        user.username = 'johnvorsten'
        user.avatar_url = 'https://github.com/users/johnvorsten/pic.png'
        user.user_url = 'https://github.com/users/johnvorsten'
        user.repositories_url = 'https://github.com/users/johnvorsten/repos'
        user.etag = '51g5re51f5dds325t1y5468y1r'
        user.save()

        repo_data = {'id':1,
                    'repo_name':'test name',
                    'repo_user':user,
                    'repo_url':'https://github.com/johnrepo/repo1test',
                    'repo_description':'test description',
                    'repo_description_custom':'test a little more verbose',
                    'repo_show':True,'repo_last_update':timezone.now()}
        repo = RepositoryShort(**repo_data)
        repo.save()

        self.assertEqual(repo.repo_name, 'test name')
        return None

    def test_create_User(self):
        """Test basic creation of RepositoryShort model
        Also test creation of basic User"""

        user = User()
        user.id = 17
        user.username = 'johnvorsten'
        user.avatar_url = 'https://github.com/users/johnvorsten/pic.png'
        user.user_url = 'https://github.com/users/johnvorsten'
        user.repositories_url = 'https://github.com/users/johnvorsten/repos'
        user.etag = '51g5re51f5dds325t1y5468y1r'
        user.save()

        self.assertEqual(user.username, 'johnvorsten')
        self.assertEqual(user.id, 17)
        return None

    def test_query_github_repos(self):
        """Test the github API from my own class.. see what is returned"""
        github_username = 'johnvorsten'
        updater = UpdateModels(update_period=30)

        response, etag = updater._query_github(github_username=github_username)
        print(response)
        print('Response Headers : ', response.headers)
        print('Response ETag : ', response.headers['ETag'])

        self.assertEqual(response.status_code, 200)
        self.assertTrue('ETag' in response.headers.keys())

        return None

    def test_query_github_user(self):
        """Test the github API from my own class.. see what is returned"""
        github_username = 'johnvorsten'
        updater = UpdateModels(update_period=30)

        response, etag = updater._query_user(github_username=github_username)
        print('header in test : ', response.headers)
        print('ETag in test : ', response.headers['ETag'])

        self.assertEqual(response.status_code, 200)
        self.assertTrue('ETag' in response.headers.keys())
        
        return None