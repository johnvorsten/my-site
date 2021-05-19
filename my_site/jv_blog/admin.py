# Django imports
from django.contrib import admin
from django import forms

# Local imports
from .models import Entry, Author, Keywords, Blog

class KeywordInLine(admin.TabularInline):
    model = Keywords
    extra = 2


class EntryAdminForm(forms.ModelForm):
    uploaded_raw_entry = forms.FileField(required=True, 
        label='Upload raw content',
        initial=False, 
        help_text=('Select a file to upload as your blog content'))

    class Meta:
        model=Entry
        fields = '__all__'

class EntryAdmin(admin.ModelAdmin):
    model = Entry
    readonly_fields = ['html_content']
    # EntryAdminForm includes a user uploaded file
    form = EntryAdminForm

    fieldsets = [
        (None, {'fields':['entry_title','entry_abstract','entry_slug',
                          'blog', 'entry_authors', 'entry_show', ]}),
        ('Date Information', {'fields':['entry_date']}),
        ('Associated Files', {'fields':['entry_thumbnail', 'uploaded_raw_entry',
                                        'html_content']}),
    ]

    search_fields=['entry_title','entry_abstract','entry_slug']

    list_display = ['entry_title','entry_date','entry_abstract']

    # Display choice inline
    inlines = [KeywordInLine] 
 
    def save_model(self, request, obj, form, change):
        """When saving the model object pass the user uploaded file
        to the models save method.
        This lets me save only the users content (NOT the actual file)
        inputs
        -------
        request : (django.http.request) a HTTP request. It should have
            method=POST and enctype='multipart/form-data'
        obj : (models.Model) A model instance to save
        form : (django.Forms.ModelForm)
        change : (bool) depends on if the object is being changed (True) 
            or is new (False)"""

        # File from users POST request body 
        # https://docs.djangoproject.com/en/3.0/topics/http/file-uploads/
        uploaded_raw_entry = request.FILES['uploaded_raw_entry']

        obj.save(uploaded_raw_entry=uploaded_raw_entry)


class AuthorAdmin(admin.ModelAdmin):
    model = Author
    search_fields = ('first_name','last_name')
    list_display = ('first_name','last_name','email')


class BlogAdmin(admin.ModelAdmin):
    model = Blog

# Register your models here.
admin.site.register(Author, AuthorAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Blog, BlogAdmin)