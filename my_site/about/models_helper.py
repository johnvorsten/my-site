# Django imports
from django.conf import settings

# Python imports 
import os

# Define SVG images that can be associated with a github repository
PICTURE_CHOICES = [
    (os.path.join(settings.MEDIA_URL,'about','images','○ Headshot 2 v1.jpg'), 'Headshot v1'),
    (os.path.join(settings.MEDIA_URL,'about','images','○ Headshot 2 v1 zoom.jpg'), 'Headshot v1 zoom'),
    (os.path.join(settings.MEDIA_URL,'about','images','○ Headshot 2 unfilter.jpg'), 'Headshot v1 unfiltered'),
    (os.path.join(settings.MEDIA_URL,'about','images','○ Headshot 2 unfilter sq.jpg'), 'Headshot unfiltered square'),
]