# Django imports

# Python imports
import os

# Local imports

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/
DEBUG = os.environ.get('DEBUG') == 'TRUE'

if not DEBUG:
    SECRET_KEY = os.environ.get('SECRET_KEY')
else:
    SECRET_KEY = '123456789'

ALLOWED_HOSTS = []
if DEBUG:
    ALLOWED_HOSTS.append('localhost')
    for host in os.environ.get('ALLOWED_HOSTS','').split(','):
        ALLOWED_HOSTS.append(host)
else:
    for host in os.environ.get('ALLOWED_HOSTS', '').split(','):
        ALLOWED_HOSTS.append(host)


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Locally defined apps
    # 'accounts.apps.AccountsConfig', # Not used
    # 'jv_github.apps.JvGithubConfig', # Not used
    'jv_blog.apps.JvBlogConfig',
    'projects.apps.ProjectsConfig',
    'about.apps.AboutConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'my_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['my_site/templates', # Global templates, whole site
                 'my_site/templates/admin'], # For admin site override
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'my_site.wsgi.application'


# Load database variables from environment
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SQL_ENGINE'),
        'NAME': os.environ.get('SQL_DATABASE'),
        'USER': os.environ.get('SQL_USER'),
        'PASSWORD': os.environ.get('SQL_PASSWORD'),
        'HOST': os.environ.get('SQL_HOST'),
        'PORT': os.environ.get('SQL_PORT'),
        'CONN_MAX_AGE': 10,
    }
}

# Primary Key
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Chicago'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static-global"),
]
# Static files are served from here
STATIC_URL = '/static-serve/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static-serve')
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Alternate file storage system
DEFAULT_FILE_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
DROPBOX_OAUTH2_TOKEN = os.environ.get('DROPBOX_OAUTH2_TOKEN', 'token-null')
DROPBOX_TIMEOUT = 100 # seconds wait time to dropbox API

# Media files
MEDIA_URL = '/media/' # For serving in development
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Local declarations of settings variables
GITHUB_ACCESS_TOKEN = os.environ.get('GITHUB_ACCESS_TOKEN', 'token-null')

if DEBUG:
    # Don't allow https in debug mode
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False
else:
    # HTTPS settings
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    # https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-SECURE_HSTS_SECONDS
    SECURE_HSTS_SECONDS = 3600
    # https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-SECURE_PROXY_SSL_HEADER
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Logging
if os.environ.get('DEBUG') == 'TRUE':
    LOGGING = {
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
else:
    LOGGING = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'docker-custom': {
                    'format': '{levelname} {asctime} {module} {message}',
                    'style': '{',
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