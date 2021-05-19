# Django imports
from django.db import models
from django.conf import settings

# Python imports
import os

# Local imports
from .models_helper import PICTURE_CHOICES

# Create your models here.
class Profile(models.Model):
    # Define model attributes / fields
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    profile_picture = models.CharField(max_length=200,
                                choices=PICTURE_CHOICES,
                                default=(os.path.join(settings.MEDIA_URL,'about','images','○ Headshot 2 unfilter sq.jpg')))
    phone = models.CharField(max_length=10)
    biography = models.TextField(max_length=800)

    def __str__(self):
        return str(self.first_name +' ' + self.last_name)

    def format_phone(self):
        """Return the profile phone number rendered"""
        area_code = self.phone[:3] + '-'
        phone_number = self.phone[3:6] + '-' + self.phone[6:]
        return (area_code + phone_number)

class Skills(models.Model):
    skill_name = models.CharField(max_length=50)
    skill_description = models.CharField(max_length=150)
    skill_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.skill_name

class Projects(models.Model):
    project_name = models.CharField(max_length=50)
    project_description = models.CharField(max_length=150)
    project_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.project_name