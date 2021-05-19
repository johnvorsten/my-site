# Django imports
from django.dispatch import Signal

# Local imports
from .models import update_models, create_user

# Third party imports

# Define your signals here
class GithubModelSignals:
    """Update models after a view is rendered.
    See the models.py for how the models are updated on this signal
    The update function uses the github API to update my internal
    models to hedge the need to continually use the github API"""
    update_models_signal = Signal(providing_args=['github_username'])
    update_models_signal.connect(update_models)

    create_user_signal = Signal(providing_args=['github_username'])
    create_user_signal.connect(create_user)

    @classmethod
    def send_update_signal(cls, github_username):
        cls.update_models_signal.send(sender=cls.__name__, 
                                github_username=github_username)

    @classmethod
    def send_create_user_signal(cls, github_username):
        cls.create_user_signal.send(sender=cls.__name__,
                                    github_username=github_username)