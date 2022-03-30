from django.test import TestCase

# Python imports
import copy

# Local imports
from .models import Projects, Skills, Profile, PICTURE_CHOICES

# Create your tests here.

class ProfileTest(TestCase):

    def setUp(self):
        self.profile_data = {'first_name':'First Name',
                            'last_name':'Last Name',
                            'email':'first.last@example.com',
                            'profile_picture':PICTURE_CHOICES[0][0],
                            'phone':'1234567890',
                            'biography':'Test long description\n\nWith some more text',}
        return None

    def test_profile_model(self):

        profile = Profile(**self.profile_data)
        profile.save()

        return None


class ProjectsTest(TestCase):

    def setUp(self):
        self.project_data = {'project_name':'Test Project',
                        'project_description':'Test Description',}

        profile_data = {'id':73,
                        'first_name':'First Name',
                        'last_name':'Last Name',
                        'email':'first.last@example.com',
                        'profile_picture':PICTURE_CHOICES[0][0],
                        'phone':'1234567890',
                        'biography':'Test long description\n\nWith some more text',}
        self.profile = Profile(**profile_data)
        self.profile.save()

        return None

    def test_projects_model(self):
        self.project_data['project_profile'] = self.profile
        project = Projects(**self.project_data)
        project.save()
        return None

class SkillsTest(TestCase):

    def setUp(self):
        # Create a profile to associate with skill
        self.skill_data = {'skill_name':'Test Skill Name',
                        'skill_description':'Test Description',}
        profile_data = {'id':73,
                        'first_name':'First Name',
                        'last_name':'Last Name',
                        'email':'first.last@example.com',
                        'profile_picture':PICTURE_CHOICES[0][0],
                        'phone':'1234567890',
                        'biography':'Test long description\n\nWith some more text',}
        self.profile = Profile(**profile_data)
        self.profile.save()

        return None

    def test_skills_model(self):
        self.skill_data['skill_profile'] = self.profile
        skill = Skills(**self.skill_data)
        skill.save()
        return None 
