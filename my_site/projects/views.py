# Django imports
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.views.generic import TemplateView, DetailView, ListView
from django.utils import timezone

# Local imports
from .models import Entry

# Create your views here.
class IndexView(ListView):
    model = Entry
    template_name = 'projects/index.html' # Explicit template
    context_object_name = 'object_list'

    def get_queryset(self):
        """Return a list of published articles"""
        time_now = timezone.now()
        objects_filter = Entry.objects\
                               .filter(entry_date__lte=time_now)\
                               .order_by('-entry_date')

        return objects_filter

    def get_context_data(self, **kwargs):
        """Only the entry objects should be returned to the template
        for parsing"""
        context = super().get_context_data(**kwargs)
        return context


class EntryDetail(DetailView):
    template_name = 'projects/entry_detail.html'
    # model = Entry
    # queryset = Entry.objects.all() # Redundant
    context_object_name = 'entry' # This should be (1) entry object

    def get_context_data(self, **kwargs):
        """This class method is used to add context data when filling out
        a template. The base model is Entry in thise case. The default
        context will return an entry instance for filling a template. However,
        if I want additional context (from a different model), then I need
        to supply it through get_context_data(). Here, I can add a key:value
        pair to the context dict"""
        # Call base implementation to get base context
        context = super().get_context_data(**kwargs)

        # Example
        # context['other_context_key'] = <other_model>.objects.all()
        return context

    def get_object(self):
        entry = get_object_or_404(Entry, entry_slug__exact=self.kwargs['slug'])
        return entry