from django.db import models
import datetime
from django.utils import timezone

# Create your models here.
# In this app, i have (2) models : question and choice
# Question : question w/ publication date
# Choice : text of choice + vote tally. Every choice is associated w/ question

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    thumbnail = models.ImageField(default='default.png', blank=True)

    def __str__(self):
        return self.question_text

    def was_published_within_day(self):

        if all((self.pub_date <= timezone.now(),
               self.pub_date >= timezone.now() - datetime.timedelta(days=1))):
            return True
            
        else:
            return False

class Choice(models.Model):
    question_key = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField('choice_text', max_length=200)
    vote_tally = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text