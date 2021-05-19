from django.contrib import admin
from .models import Question
from .models import Choice

class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3

# Change admin form look
class QuestionAdmin(admin.ModelAdmin):
    # fields = ['pub_date','question_text'] # Not needed (see fieldsets)
    fieldsets = [
        (None, {'fields':['question_text']}),
        ('Date Information', {'fields':['pub_date']})
        ]

    # Display choice inline
    inlines = [ChoiceInLine] 

    # Change list on object view
    list_display = ('question_text', 'pub_date')

    # Add search query
    search_fields = ['question_text']

    list_per_page = 100

# Register your models here.
admin.site.register(Question, QuestionAdmin)
