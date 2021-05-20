from django.apps import apps

def load_tests(loader, tests, pattern):

    from django.conf import settings

    if apps.is_installed('polls'):
        pass

    # If this app is not in INSTALLED_APPS then we will not run tests for this app
    return