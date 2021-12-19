# Django imports
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.views.generic import TemplateView, DetailView, ListView
from django.views.decorators.http import require_GET
from django.utils import timezone

# Local imports
from .models import Entry

# Declarations

#%%
# Function based views
@require_GET
def mil(request):
    return render(request, 'projects/mil.html')

# Class based views
class BlogIndexView(ListView):
    model = Entry
    template_name = 'jv_blog/index.html' # Explicit template
    context_object_name = 'object_list'

    def get_queryset(self):
        """Return a list of published articles"""
        time_now = timezone.now()
        objects_filter = Entry.objects\
                               .filter(entry_date__lte=time_now, 
                                        entry_show=True, 
                                        blog__description='blog')\
                               .order_by('-entry_date')
        
        # Prefetch related authors (reduce database queries)
        objects_related = objects_filter.prefetch_related('entry_authors')

        return objects_related

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        entry_objects = context.pop('object_list', '')
        new_object_list = []

        for entry in entry_objects:
            author = self.get_first_author(entry)
            entry_author_tuple = (entry, author)
            new_object_list.append(entry_author_tuple)

        context['object_list'] = new_object_list
        return context

    def get_first_author(self, entry):
        """Return the first author in the relation field between the Entry object
        and Author object"""
        authors = entry.entry_authors.all()
        if len(authors) > 1:
            first_author_string = authors[0].__str__() + ' et. al.'
        else:
            first_author_string = authors[0].__str__()
        return first_author_string


class BlogDetail(DetailView):
    template_name = 'jv_blog/entry_detail.html'
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
        entry = get_object_or_404(Entry, entry_slug__exact=self.kwargs['slug'], blog__description='blog')
        return entry

# Class based views for projects (similar to blogs, but fits in this module)
class ProjectIndexView(ListView):
    model = Entry
    template_name = 'projects/index.html' # Explicit template
    context_object_name = 'object_list'

    def get_queryset(self):
        """Return a list of published articles"""
        time_now = timezone.now()
        objects_filter = Entry.objects\
                               .filter(entry_date__lte=time_now, 
                                        blog__description='projects')\
                               .order_by('-entry_date')

        return objects_filter

    def get_context_data(self, **kwargs):
        """Only the entry objects should be returned to the template
        for parsing"""
        context = super().get_context_data(**kwargs)
        return context


class ProjectDetail(DetailView):
    template_name = 'projects/entry_detail.html'
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
        entry = get_object_or_404(Entry, entry_slug__exact=self.kwargs['slug'], 
                                blog__description='projects')
        return entry