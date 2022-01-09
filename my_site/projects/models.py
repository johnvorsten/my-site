from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth.models import User

# Python imports
import os
import datetime
from hashlib import blake2s

# Third party imports
import mistune # .md to html
import mammoth # .docx to html
from bs4 import BeautifulSoup

# Local imports
from .models_helper import default_author, html_directory_path, raw_directory_path


# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    head_shot = models.ImageField(upload_to='projects/authors', blank=True)
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
        return self.keyword_text

class Entry(models.Model):
    entry_title = models.CharField(max_length=100)
    entry_date = models.DateTimeField('date published')
    entry_abstract = models.TextField(max_length=1000)
    entry_thumbnail = models.ImageField(default='projects/images/ivana-cajina-unsplash.jpg', 
                                        upload_to='projects/images',
                                        blank=True)
    raw_entry = models.FileField(upload_to=raw_directory_path)
    html_content = models.FileField(blank=True)
    entry_slug = models.SlugField(unique=True)
    entry_authors = models.ManyToManyField(Author)

    def __str__(self):
        return self.entry_title

    def article_summary(self, n_characters=200):
        """parse html to deliver plain text of the beginning of the blog
        # This will replace self.entry_abstract. Instead of an explicit abstract,
        # simply deliver the first 200 characters of the article..."""

        with self.html_content.open(mode='rt') as f:
            content = f.read()
        
        bs_html = BeautifulSoup(content)
        text = bs_html.get_text()

        return text[:n_characters]

    def save(self, *args, **kwargs):
        # Save .md, .tex, .docx file
        self.raw_entry.save(self.raw_entry.name, self.raw_entry, save=False)

        # Delete the old file if applicable
        try:
            existing = Entry.objects.get(id=self.id)
            print('Entry ', existing.raw_entry == self.raw_entry)
            print('Entry Existing ', existing.raw_entry)
            print('Entry instance ', self.raw_entry)
            if not existing.raw_entry == self.raw_entry:
                print('#Existing raw entry : ', existing.raw_entry)
                existing.raw_entry.delete(False)
        except ObjectDoesNotExist as e:
            print('raw entry exception ', e)
            pass

        # Create a html file from .md or .tex
        html_content = self.parse_raw_content(self.raw_entry)

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
            print('HTML ', existing.html_content == self.html_content)
            print('HTML Existing ', existing.html_content)
            print('HTML instance ', self.html_content)
            if not existing.html_content == self.html_content:
                print('#Existing html : ', existing.html_content)
                existing.html_content.delete(False)
        except ObjectDoesNotExist as e:
            print('HTML content exception ', e)
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
        with self.html_content.open(mode='rt') as f:
            html_content_text = f.read()
        
        return html_content_text

    def parse_raw_content(self, raw_entry):
        """inputs
        raw_entry : (django.db.models.FileField) object. This is a field 
        of this model
        output
        -------
        html_file : (django.db.models.File)"""

        raw_entry_path = raw_entry.name
        (root, extension) = os.path.splitext(raw_entry_path)

        if extension == ".html":
            # html should just be displayed
            html_content = self._parse_html(raw_entry)

        elif extension == ".md":
            # Parse markdown to html
            html_content = self._parse_markdown(raw_entry)

        elif extension in ['.docx', '.doc']:
            # parse .docx to html
            html_content = self._parse_docx(raw_entry)

        elif (extension == ".tex"): # TODO 
            # Parse latex to html
            html_content = self._parse_latex(raw_entry)

        else:
            html_content = (r"<p> No raw content was available to parse." +
                    "Make sure the uploaded raw content was of type .html, .md, or .tex </p>")

        return html_content # Return string

    def _parse_markdown(self, raw_entry):
        """Input
        -------
        raw_entry : (models.FileField) a FieldFile or FileField django model field
        output 
        -------
        generated_html : (str) a parsed html file using mistune 
        markdown->html package"""
        generated_html = ""

        with raw_entry.open(mode='rt') as f:
            content = f.read()
            generated_html += mistune.markdown(content)

        # make BeautifulSoup
        html_content_parsed = BeautifulSoup(generated_html, "html.parser")
        # prettify the html
        html_content = html_content_parsed.prettify()

        return html_content # Return string representation

    def _parse_html(self, raw_entry):
        """Input
        -------
        raw_entry : (models.FileField) a FieldFile or FileField django model field
        output 
        -------
        generated_html : (str) a parsed html file"""
        generated_html = ""

        with raw_entry.open(mode='rt') as f:
            content = f.readlines()
            for line in content:
                generated_html += line

        # make BeautifulSoup
        html_content_parsed = BeautifulSoup(generated_html, "html.parser")
        # prettify the html
        html_content = html_content_parsed.prettify()

        return html_content # Return string representation

    def _parse_latex(self, raw_entry):
        """Input
        -------
        raw_entry : (models.FileField) a FieldFile or FileField django model field 
        output 
        -------
        generated_html : (str) a parsed html file using mistune 
        markdown->html package"""

        # Call CLI executable on raw_entry.name location
        # Specify output directory
        output_directory = ""
        # Read
        generated_html = ""
        generated_html += '<p> TODO </p>' # TODO parse latex to html

        # make BeautifulSoup
        html_content_parsed = BeautifulSoup(generated_html, "html.parser")
        # prettify the html
        html_content = html_content_parsed.prettify()

        return html_content # Return string representation

    def _parse_docx(self, raw_entry):
        """Input
        -------
        raw_entry : (models.FileField) a FieldFile or FileField django model field
        output 
        -------
        generated_html : (str) a parsed html file using mammoth
        docx->html package"""

        # Define a style map for custom .css classes possible
        # Not implemented, use later if needed
        style_map = """
        p[style-name='Section Title'] => h1:fresh
        p[style-name='Subsection Title'] => h2:fresh"""

        # See https://github.com/mwilliamson/python-mammoth#image-converters
        # If I'm creating an image conversion function
        convert_image_and_save = False

        with raw_entry.open(mode='rb') as docx_file:

            if convert_image_and_save: # Not ready..
                result = mammoth.convert_to_html(docx_file, convert_image=convert_image)

            else: # Standard image included inline with html
                result = mammoth.convert_to_html(docx_file)

            generated_html = result.value # Generated html
            messages = result.messages # Errors or warnings

        # make BeautifulSoup
        soup = BeautifulSoup(generated_html, "html.parser")
        # prettify the html
        html_content = soup.prettify()

        return html_content # Return string representation