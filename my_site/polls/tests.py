# Django imports
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

# Third party
import datetime

# Local
from .models import Question

# Create your tests here.
class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """was_published_recently returns False for questions with
        a publish date in the future"""

        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_within_day(), False)

    def test_was_published_recently_with_past_question(self):
        """was_published_recently returns True for questions with
        a publish date within one day"""

        time = timezone.now()
        past_question = Question(pub_date=timezone.now() - \
                                  datetime.timedelta(hours=23, minutes=59, seconds=59))

        self.assertIs(past_question.was_published_within_day(), True)

class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """If no questions are available to display"""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['recent_question_list'], [])
    
    def test_past_question(self):
        """Questions in the past are displayed"""
        time = timezone.now() - datetime.timedelta(days=1)
        question = Question.objects.create(question_text = 'past question',
                                pub_date=time)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['recent_question_list'], 
                                 ['<Question: past question>'])

    def test_future_question(self):
        """Question in future not displayed"""
        time = timezone.now() + datetime.timedelta(days=1)
        question = Question.objects.create(question_text = 'future question',
                                pub_date=time)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['recent_question_list'], 
                                 [])
        self.assertContains(response, "No polls are available")

    def test_future_and_past_question(self):
        """Only questions in the past are displayed..."""
        time_past = timezone.now() - datetime.timedelta(days=1)
        question = Question.objects.create(question_text = 'past question',
                                pub_date=time_past)

        time_future = timezone.now() + datetime.timedelta(days=1)
        question = Question.objects.create(question_text = 'future question',
                                pub_date=time_future)

        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['recent_question_list'], 
                                 ['<Question: past question>'])
        self.assertQuerysetEqual(response.context['recent_question_list'],
                                 ['<Question: past question>'])
        

