"""
This file complements models.py
It is separated to give easy readability to models.py
"""
# Python imports
from hashlib import blake2s
import os

# Django imports
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

# Third party imports
import mistune # .md to html
import mammoth # .docx to html
from bs4 import BeautifulSoup

# Define upload error
class UploadError(Exception):
    """Upload occured during parsing or uploading to file system"""

def raw_directory_path(instance, filename):
    """Output a filename to save FileField inputs. The raw input content
    is one of (HTML, Markdown, Latex). Once the raw content is saved,
    it is converted to HTML to be served.
    This is used for directly saving raw markdown or .docx files before being parsed to html
    See models.Model.FildField.upload_to for more information
    inputs
    -------
    instance: (models.Model) instance of the model
    filename: (str) original filename given by the user
    Output
    -------
    filename_new: (str) filename with date appended to prevent overwrites"""
    # File uploaded to MEDIA_ROOT/jv_blog/entries/<filename_new>

    if hasattr(filename, 'name'):
        file_path = filename.name
    elif isinstance(filename, str):
        file_path = filename

    base_dir = 'jv_blog/raw_entries/{}'
    # time_now = datetime.datetime.now()
    # str_time = datetime.datetime.strftime(time_now, "%Y%m%d%H%M")
    (root, head) = os.path.split(file_path)
    (name, extension) = os.path.splitext(head)
    filename_new = name +  extension
    filepath_new = base_dir.format(filename_new)

    return filepath_new

def html_directory_path(instance, filename):
    """Output a directory path to save FileField inputs. The raw input content
    is one of (HTML, Markdown, .docx). Once the raw content is saved,
    it is converted to HTML to be served.
    This function is specifically used for saving .html files after they have been parsed
    See models.Model.FildField.upload_to for more information
    inputs
    -------
    instance: (models.Model) instance of the model
    filename: (str) original filename given by the user
    Output
    -------
    filename_new: (str) filename with date appended to prevent overwrites"""
    # File uploaded to MEDIA_ROOT/jv_blog/entries/<filename_new>

    if hasattr(filename, 'name'):
        file_path = filename.name
    elif isinstance(filename, str):
        file_path = filename

    base_dir = 'jv_blog/entries/{}'
    # time_now = datetime.datetime.now()
    # str_time = datetime.datetime.strftime(time_now, "%Y%m%d%H%M")
    (root, head) = os.path.split(file_path)
    (name, extension) = os.path.splitext(head)
    filename_new = name + '.html'
    filepath_new = base_dir.format(filename_new)

    return filepath_new

def convert_image(image):
    """Image converter (do NOT embed image data in html file)
    See https://github.com/mwilliamson/python-mammoth#image-converters
    for more details
    Not used; Optionally in the future. See python-mammoth package for
    Converting .docx files to html. Instead of parsing images to ASCII image embedded
    in HTML I can choose how to handle images. Something for another day"""
    # If I want to serve images separately, I need to save the
    # File then change the returned source
    # TODO Not implemented right now

    media_root = settings.MEDIA_ROOT
    # TODO Save document title in image name
    blake_hash_alg = blake2s(digest_size=8)

    with image.open() as image_bytes:

        # Save a new image file
        hash_digest = blake_hash_alg.update(image_bytes).hexdigest()
        # TODO this path is not supported w/ a wmf/emf buffer object
        image_path = f'{media_root}/jv_blog/entries/images/doc_title_image_{hash_digest}.png'

        with open(image_path, 'wb') as new_image_file:
            new_image_file.write(image_bytes)

    source_dict = { 'src': new_image_file.name }

    return source_dict

def default_author():
    """Return the default author. If the default author
    (Anonymous) is not defined, then an instance is created"""
    try:
        # Import models, a circular dependency is caused if this is
        # In the head of the file
        from .models import Author
        author = Author.objects.get(first_name__exact='Anonymous',
                                    last_name__exact='Author')
    except ObjectDoesNotExist:
        author = Author(first_name='Anonymous',
                        last_name='Author')
        author.save()
    
    return author.id

def parse_raw_content(raw_entry):
    """inputs
    raw_entry: (django.db.models.FileField) or similar
    (django.core.files.base.ContentFile)object. This is a field
    of this model Entry. It is a file-like object
    output
    -------
    html_file: (django.db.models.File)"""

    raw_entry_path = raw_entry.name
    (root, extension) = os.path.splitext(raw_entry_path)

    if extension == ".html":
        # html should just be displayed
        html_content = _parse_html(raw_entry)

    elif extension == ".md":
        # Parse markdown to html
        html_content = _parse_markdown(raw_entry)

    elif extension in ['.docx', '.doc']:
        # parse .docx to html
        html_content = _parse_docx(raw_entry)

    elif extension == ".tex": # TODO
        # Parse latex to html
        html_content = _parse_latex(raw_entry)

    else:
        html_content = (
            r"<p> No raw content was available to parse." +
            "Make sure the uploaded raw content was of type " +
            ".html, .md, or .tex </p>")

    return html_content # Return string

def _parse_markdown(raw_entry):
    """Input
    -------
    raw_entry: (models.FileField) a FieldFile or FileField django model field
    output
    -------
    generated_html: (str) a parsed html file using mistune markdown->html package"""

    with raw_entry.open(mode='rb') as file:
        content = file.read() # Content is bytes
        generated_html = mistune.markdown(content.decode('utf-8'), escape=False)

    # make BeautifulSoup
    html_content_parsed = BeautifulSoup(generated_html, "html.parser")
    html_content = html_content_parsed.prettify()

    return html_content # Return string representation

def _parse_html(raw_entry):
    """Input
    -------
    raw_entry: (models.FileField) a FieldFile or FileField django model field
    output 
    -------
    generated_html: (str) a parsed html file"""

    with raw_entry.open(mode='rb') as file:
        content = file.read()

    # Make BeautifulSoup
    html_content_parsed = BeautifulSoup(content.decode('utf-8'), "html.parser")
    # Prettify the html
    html_content = html_content_parsed.prettify()

    return html_content # Return string representation

def _parse_latex(raw_entry):
    """Input
    -------
    raw_entry: (models.FileField) a FieldFile or FileField django model field
    output
    -------
    generated_html: (str) a parsed html file using mistune
    markdown->html package"""

    # Call CLI executable on raw_entry.name location
    generated_html = '<p> TODO </p>' # TODO parse latex to html
    raise(NotImplementedError("Latex parseing to HTML is not implemented yet"))

    # make BeautifulSoup
    html_content_parsed = BeautifulSoup(generated_html, "html.parser")
    # prettify the html
    html_content = html_content_parsed.prettify()

    return html_content # Return string representation

def _parse_docx(raw_entry):
    """Input
    -------
    raw_entry: (models.FileField) a FieldFile or FileField django model field
    output
    -------
    generated_html: (str) a parsed html file using mammoth
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
