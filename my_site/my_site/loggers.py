# Python imports
import os

# Local imports
from .settings import BASE_DIR


LOGGING_TESTING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {module} {message}',
            'style': '{',
        },
    },

    'handlers': {
        # Write problems to a file
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR,'my_site','my_site.log'),
            'formatter': 'verbose',
        },
        # Write messages to the console
        'console': {
            'level': 'DEBUG',
            'filters':['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },

    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers':['console'],
            'level':'DEBUG',
            'propagate':True,
        },
    },

    'filters': {
        'require_debug_true': {
            '()':'django.utils.log.RequireDebugTrue',
        }
    },
}

LOGGING_DOCKER = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'docker-custom': {
            'format': '{levelname} {asctime} {module} {message}',
        }
    },

    'handlers': {
        # Write messages to the console
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'docker-custom',
        },
    },

    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}