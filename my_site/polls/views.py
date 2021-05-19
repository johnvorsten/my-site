# Django imports
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone

# Local views and modules
from .models import Question, Choice


# Create your views here.
class IndexView(generic.ListView):
    """Uses template called <app_name>/<model_name>_list.html"""
    template_name = 'polls/index.html' # Explicit template
    # Explicit context object for use
    # In the template.. otherwise the default name would be <model_name>_list
    context_object_name = 'recent_question_list' 

    def get_queryset(self):
        """Return the (5) most recent published questions"""
        objects_filter = Question.objects\
                         .filter(pub_date__lte=timezone.now())\
                         .order_by('-pub_date')[:5]
        return objects_filter


class DetailView(generic.DetailView):
    """DetailView expects primary key value captured from URL to 
    be named 'pk' 
    Uses a templated called <app_name>/<model_name>_detail.html"""
    model = Question
    template_name = 'polls/detail.html' # Explicit template
    context_object_name = 'question'

    def get_queryset(self):
        """Exclude questions that arent published"""
        objects = Question.objects.filter(pub_date__lte=timezone.now())
        return objects


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html' # Explicit template
    context_object_name = 'question'


def vote(request, pk):
    """After the user votes on a poll, reflect the vote to the database
    methods
    get_object_or_404(model_object, pk=identifier_id)
    model.choice_set : used when relating objects between tables
    request.POST : a dictionary like structure that is a POST object
    render(request, 'template_string', context)
    HtmlRedirect : use after dealing with POST data
    reverse : Allows URL patterns to be used?..."""
    question = get_object_or_404(Question, pk=pk)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 
                     'polls/detail.html', 
                     context={'question':question,
                     'error_message':"You didn't select a choice"})
    else:
        selected_choice.vote_tally += 1
        selected_choice.save()

    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))






# Legacy
# # Create your views here.
# def index(request):
#     recent_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/index.html')
#     context = {'recent_question_list':recent_question_list}

#     return HttpResponse(template.render(context, request))


# def index_alternate(request):
#     """An alternative way to return an HttpResponse with only render()"""
#     recent_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'recent_question_list':recent_question_list}

#     return render(request, 'polls/index.html', context=context)


# def detail(request, question_id):

#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")

#     return render(request, 'polls/detail.html', {'question':question})


# def detail_alternate(request, question_id):
#     """An alternate method to get an object from database and
#     raise a 404 error if the object does not exist"""
#     question = get_object_or_404(Question, pk=question_id)

#     return render(request, 'polls/detail.html', {'question':question})


# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
    
#     return render(request, 'polls/results.html', context={'question':question})


# def vote(request, question_id):
#     """After the user votes on a poll, reflect the vote to the database
#     methods to learn
#     get_object_or_404(model_object, pk=identifier_id)
#     model.choice_set : used when relating objects between tables
#     request.POST : a dictionary like structure that is a POST object
#     render(request, 'template_string', context)
#     HtmlRedirect : use after dealing with POST data
#     reverse : Allows URL patterns to be used?..."""
#     question = get_object_or_404(Question, pk=question_id)

#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         return render(request, 
#                      'polls/detail.html', 
#                      context={'question':question,
#                      'error_message':"You didn't select a choice"})
#     else:
#         selected_choice.vote_tally += 1
#         selected_choice.save()

#     return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))