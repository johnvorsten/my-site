# Django imports
from django.contrib import admin
from django import forms

# Local imports
from .models import Entry, Author, Keywords

class EntryAdminForm(forms.ModelForm):

    class Meta:
        model=Entry
        fields = '__all__'

class KeywordInLine(admin.TabularInline):
    model = Keywords
    extra = 2

class EntryAdmin(admin.ModelAdmin):
    model = Entry
    readonly_fields = ['html_content']
    form = EntryAdminForm

    fieldsets = [
        (None, {'fields':['entry_title','entry_abstract','entry_slug',
                                        'entry_authors']}),
        ('Date Information', {'fields':['entry_date']}),
        ('Associated Files', {'fields':['entry_thumbnail','raw_entry',
                                        'html_content']}),
    ]

    search_fields=['entry_title','entry_abstract','entry_slug']

    list_display = ['entry_title','entry_date','entry_abstract']
 
     # Display choice inline
    inlines = [KeywordInLine] 


class AuthorAdmin(admin.ModelAdmin):
    model = Author
    search_fields = ('first_name','last_name')
    list_display = ('first_name','last_name','email')

# Register your models here.
admin.site.register(Author, AuthorAdmin)
admin.site.register(Entry, EntryAdmin)