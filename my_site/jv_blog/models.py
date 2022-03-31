"""Models related to blogs and blog entries"""
# Python imports

# Django Imports
from django.db import models
from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist
# from django.core.files import File
# from django.utils import timezone
# from django.dispatch import receiver
# from django.core.files.storage import FileSystemStorage
# from django.conf import settings
# from django.contrib.auth.models import User

# Third party imports
from bs4 import BeautifulSoup

# Local imports
from .models_helper import (raw_directory_path, html_directory_path,
                            default_author, UploadError,
                            parse_raw_content)

# Create your models here.
class Author(models.Model):
    """Author is a foreign key associated with an entry. It includes a reference to
    the blog entry's author if desired"""
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    head_shot = models.ImageField(upload_to='jv_blog/authors', blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return (self.first_name + ' ' + self.last_name)

    def __eq__(self, other):
        equality_tuple = (self.first_name == other.first_name,
                self.middle_name == other.middle_name,
                self.last_name == other.last_name,
                self.email == other.email)
        if all(equality_tuple):
            return True
        else:
            return False

class Keywords(models.Model):
    """Fun tags to associate with each repository. These must be
    custom entered through the admin interface"""
    keyword_text = models.CharField(max_length=50)
    entry_model = models.ForeignKey('Entry', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.keyword_text)

class Blog(models.Model):
    """There can be multiple blogs, and each Entry is associated with a
    Blog. The Blog model is used to render different templates or layouts
    for Entries that belong to a Blog"""
    description = models.CharField(max_length=50)

    def __str__(self):
        return str(self.description)

class Entry(models.Model):
    """Specific blog entry into a blog. This incldues metadata associated with a specific entry
    (such as title, date, abstract, and thumbnails) along with the bulk of content.
    This entry has the option to accept markdown, HTML, or microsoft word files. These files will be
    parsed into HTML (see save method).
    Parsed HTML is saved to the configured file storage system (see settings.py)
    The file path reference is saved to the database
    When a blog entry is requested, the file is fetched from file storage and served."""

    entry_title = models.CharField(max_length=100)
    entry_date = models.DateTimeField('date published')
    entry_abstract = models.TextField(max_length=500)
    entry_thumbnail = models.ImageField(default='default.png', 
                                        upload_to=r'jv_blog/images',
                                        blank=True)
    raw_entry = models.FileField(upload_to=raw_directory_path,
                                blank=True)
    html_content = models.FileField(blank=True)
    entry_slug = models.SlugField(unique=True)
    entry_authors = models.ManyToManyField(Author)
    entry_show = models.BooleanField(default=True)
    blog = models.ForeignKey('Blog', blank=True, null=True, on_delete=models.SET_DEFAULT, default=1)

    def __str__(self):
        return str(self.entry_title)

    def article_summary(self, n_characters=200):
        """Parse html to deliver plain text of the beginning of the blog
        This will replace self.entry_abstract 
        Instead of an explicit abstract simply deliver the first 200 
        characters of the article..."""

        with self.html_content.open(mode='rt') as f:
            content = f.read()
        
        bs_html = BeautifulSoup(content)
        text = bs_html.get_text()

        return text[:n_characters]

    def save(self, *args, **kwargs):
        """Save an raw_entry uploaded by the user
        1. Convert a raw uploaded file into a ContentFile object, and save the ContentFile
        object into a model field FieldField object
        2. Check if this instance of an entry already exists. If this entry exists and we
        are re-saving it, then it means the uplaoded content was modified. Delete the existing
        raw_entry file before saving the new raw_entry file.
        3. Parse raw content from .md, .html, or .docx into HTML
        4. Convert parsed HTML into a ContentFile object, and save the ContentFile
        object into the html_content model field FieldField object
        5. Check if this instance of an entry already exists. If this entry exists and we
        are re-saving it, then it means the uplaoded content was modified. Delete the existing
        parsed html_content before saving the new html_content file.
        6. Create a slug if none exists
        7. Associate the default author to this article if none exists or is not defined

        inputs
        -------
        *args: () not used
        **kwargs: (dict) {uploaded_raw_entry:SimpleUploadFile}"""
        try:
            uploaded_raw_entry = kwargs.pop('uploaded_raw_entry')
        except KeyError as exception:
            raise UploadError(('No uploaded_raw_entry file was passed from the admin interface. ' + 
                'Make sure a file was passeed when calling this models save method')) from exception

        with uploaded_raw_entry.open(mode='rb') as file:
            raw_entry_content = file.read()
        raw_entry_file = ContentFile(content=raw_entry_content,
                                     name=raw_directory_path(self, uploaded_raw_entry.name))

        # Save the content file into a model field
        raw_entry_file.open(mode='rb')
        self.raw_entry.save(raw_entry_file.name, raw_entry_file, save=False)
        raw_entry_file.close()

        # Delete the old file if applicable
        try:
            # Delete the existing raw entry file
            existing = Entry.objects.get(id=self.id)
            if not existing.raw_entry == self.raw_entry:
                existing.raw_entry.delete(False)
        except ObjectDoesNotExist:
            # This is the first time the entry object is created
            pass

        # Create a html file from .md, .html, or .docx
        html_content = parse_raw_content(self.raw_entry)

        # Save html content to a django ContentFile
        html_file = ContentFile(content=html_content.encode('utf-8'), 
                                name=html_directory_path(self, self.raw_entry.name))

        # Save the html file into a model field
        html_file.open(mode='r')
        self.html_content.save(html_file.name, html_file, save=False)
        html_file.close()

        # Delete the old file if applicable
        try:
            existing = Entry.objects.get(id=self.id)
            if not existing.html_content == self.html_content:
                existing.html_content.delete(False)
        except ObjectDoesNotExist:
            pass

        # Create a slug if none exists
        if not self.entry_slug:
            self.entry_slug = slugify(self.entry_title)

        super().save(*args, **kwargs) # Call the 'built-in' save() method

        # Associate author if None exists
        if not self.entry_authors.all().exists():
            default_author_id = default_author()
            self.entry_authors.add(Author.objects.get(id=default_author_id))

    def html_content_reader(self):
        """Return HTML strings that can be rendered straight into an HTML
        template. Use the {autoescape off} tag or {|safe} filter.."""
        with self.html_content.open(mode='rb') as f:
            # The file is saved encoded utf-8 format
            html_content_text = f.read().decode('utf-8')
        
        return html_content_text

