from django.test import TestCase

# Python imports
import copy

# Local imports
from .models import Projects, Skills, Profile, PICTURE_CHOICES
from .admin import ProfileForm

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

    def test_admin_form(self):

        # Create a model admin for testing form
        profile_form = ProfileForm(data=self.profile_data)

        # No errors should be raised for testing data
        if len(profile_form.errors) > 0:
            print(profile_form.errors)
        self.assertTrue(len(profile_form.errors) == 0)

        # phone number validation
        profile_data2 = copy.deepcopy(self.profile_data)
        profile_data2['phone'] = '0a23456789' # Non-numeric
        profile_form2 = ProfileForm(data=profile_data2)
        error = profile_form2.errors['phone']
        self.assertTrue(error[0].__contains__('Do not include dashes or spaces'))

        profile_data2['phone'] = '01234567899' # Too long
        profile_form2 = ProfileForm(data=profile_data2)
        error = profile_form2.errors['phone']
        self.assertTrue(error[0].__contains__('Ensure this value has at most 10 characters'))

        return None

    def test_admin_phone_validation(self):

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
