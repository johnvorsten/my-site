## Common django (and other) command-line-interface
#### Activate miniconda/conda environment
conda activate django
#### Create django app
python manage.py startapp <app_name>
#### Development server
python manage.py runserver
#### Using the django shell for testing
python manage.py shell
#### Creating a user or superuser
python manage.py createsuperuser

## Unit Testing
use --settings=my_site.settings_test for local testing. This module uses sqlite3 and local file storage
#### Run all the tests in the <app_name>.tests module
`python manage.py test <app_name>.tests --settings=my_site.settings_test`
#### Run all the tests found within the <app_name> package
`python manage.py test <app_name>`
#### Run just one test case
`python manage.py test <app_name>.tests.<test_case_class>`
#### Run just one test method
`python manage.py test <app_name>.tests.<test_case_class>.<test_method>`
#### Currnet commands
`python manage.py test about.tests jv_blog.tests --settings=my_site.settings_test`


## Adding an 'app' in django
Add to the list of INSTALLED_APPS in settings.py
Create database model in models.py
Create migration script for `python manage.py makemigrations` or `python manage.py makemigrations <app_name>`
(Apply database migrations) Create database tables `python manage.py migrate`


## Testing Models
Here is a manual way to test models:
Open the django shell, then import the database model from your application. Then try to create an instance of a database model, and try to save it to the database
python manage.py shell
from <app_name>.models import <model_1>, <model_2>
<model_1>.objects.all()
<instance> = <model_1>(<param1>,<param2>)
<instance>.save()
<instance>.id
<instance>.<attribute>


## Standard files
root directory: my_site/ (container for my project) and my_site/ (inner package)
manage.py: command line utility for interacting w/ django
my_site/settings.py: settings for project
my_site/urls.py: "table of contents" for the website. This will reference urls in the views.py  module, which tells django what httpresponse to send based on the url pattern it receives
my_site/wsgi.py: entry point for WSGI-compatable web servers to serve the project (worry about this later)


## Views and urls
views.py - Contains views to specific models or applications.
urls.py - Contains URL paths for the application or project-wide. Import views to the URL dispatcher
@param <regex_route> string that contains a URL pattern
@param views.<function_name> should match the function returning a httpResponse in views.py. 
# @param name : lets your name your URL, and refer to it unambiguously from elsewhere in django. AKA if you want to use it in a <href> tag you can do {% url 'name_string' %}
urlpatterns =[
    path('<regex_route>', views.<function_name>, name=<name??>)
]


## Admin Files
To have database models editable from the admin, I have to add Models to the app_name/admin.py files admin.site.register(Question)


## Generic Views
1. Create a URLconf
2. Introduce views based on django generic views (ListView, DetailView)
DetailView & ListView:
queryset - (optional) all the objects to be passed as context. The default is <model>.objects.all()
    and all objects will be passed to the template being rendered
model - (mandatory) what model is the view representing? If you do not define this,
    then queryset must be defined
context_object_name
template_name : (optional) template name for generic view to render. If this is not defined,
    then it will look for a template that matches the model name. For DetailView, it 
    would look for <model_name>_detail.html.
get_context_data() : (optional) add context data to be passed to the template.
get_queryset() : returns the value of the class queryset attribute. Add more logic
    by overriding this class method


## Database Query
https://docs.djangoproject.com/en/3.0/topics/db/queries/


## Test Client - shell response content
Use this to test code at the view level (for example, was a certain context passed with the request; was a token passed in the request?). Use it in shell. Useful for looking at response context
from django.text.utils import setup_test_environment
setup_test_environment()
from django.test import Client
client = Client()
response = client.get('URL/conf')
response.status_code
from django import reverse
response = client.get(reverse('<app_name>:<view_name>'))
response.status_code # Check the status code of a response
response.content # HTML content
response.context # Dictionary, items passed to template

## Uninstalling an app
1. Remove imports and usage of app in the project
    1. Including urls.py, and others???
2. Remove the model data definition in models.py inside the app folder. Make migrations directions using `python manage.py makemigrations <app_name>`. Then, apply migrations using `python manage.py migrate <app_name>`
2. Remove the reference in settings.py and settings_test.py INSTALLED_APPS
2. Delete the application folder directory


