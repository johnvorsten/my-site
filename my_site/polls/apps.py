from django.apps import AppConfig

# Include this in the main package settings.py 'installed apps' 
# This 'plugs-in' the app to the main website
class PollsConfig(AppConfig):
    name = 'polls'
