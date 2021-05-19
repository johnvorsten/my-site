"""
This file complements models.py
It is separated to give easy readability to models.py

Helper methods defined here : 
raw_directory_path : output a directory path to save FileField inputs
    This is used for directly saving raw markdown or .docx files before being parsed to html
    See models.Model.FildField.upload_to for more information
html_directory_path : output a directory path to save FileField inputs
    This function is specifically used for saving .html files after they have been parsed
    See models.Model.FildField.upload_to for more information
convert_image: Not used; Optionally in the future. See python-mammoth package for 
    Converting .docx files to html. Instead of parsing images to ASCII image embedded
    in HTML I can choose how to handle images. Something for another day
default_author : a function to return the default author. If the default author
    (Anonymous) is not defined, then an instance is created"""

# Django imports
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

# Python imports
from hashlib import blake2s
import os


def raw_directory_path(instance, filename): 
    """Output a file name for raw input content. The raw input content
    is one of (HTML, Markdown, Latex). Once the raw content is saved,
    it is converted to HTML to be served.
    inputs
    -------
    instance : (models.Model) instance of the model
    filename : (str) original filename given by the user
    Output
    -------
    filename_new : (str) filename with date appended to prevent overwrites"""
    # File uploaded to MEDIA_ROOT/jv_blog/entries/<filename_new>

    if hasattr(filename, 'name'):
        file_path = filename.name
    elif isinstance(filename, str):
        file_path = filename

    base_dir = 'projects/raw_entries/{}'
    # time_now = datetime.datetime.now()
    # str_time = datetime.datetime.strftime(time_now, "%Y%m%d%H%M")
    (root, head) = os.path.split(file_path)
    (name, extension) = os.path.splitext(head)
    filename_new = name +  extension
    filepath_new = base_dir.format(filename_new)

    return filepath_new

def html_directory_path(instance, filename):
    """Output a file name for raw input content. The raw input content
    is one of (HTML, Markdown, .docx). Once the raw content is saved,
    it is converted to HTML to be served.
    inputs
    -------
    instance : (models.Model) instance of the model
    filename : (str) original filename given by the user
    Output
    -------
    filename_new : (str) filename with date appended to prevent overwrites"""
    # File uploaded to MEDIA_ROOT/jv_blog/entries/<filename_new>

    if hasattr(filename, 'name'):
        file_path = filename.name
    elif isinstance(filename, str):
        file_path = filename

    base_dir = 'projects/entries/{}'
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
    for more details"""
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
        image_path = r'{}/jv_blog/entries/images/doc_title_image_{}.png'.format(media_root, hash_digest)

        with open(image_path, 'wb') as new_image_file:
            new_image_file.write(image_bytes)
    
    source_dict = { 'src': new_image_file.name }

    return source_dict

def default_author():
    """get or create the pk of the deafult author. This should
    be an author with name Anonymous"""
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
