# Django imports
from django.test import TestCase, Client
from django.utils import timezone
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import SuspiciousFileOperation
from django.utils._os import safe_join

# Python imports
import datetime
import os, io

# Third party imports
import dropbox

# Local imports
from .models import (Entry, 
                    Author, 
                    Blog,
                    raw_directory_path, 
                    html_directory_path,
                    parse_raw_content)
from .admin import EntryAdmin

# Global Variables
try:
    DROPBOX_OAUTH2_TOKEN = settings.DROPBOX_OAUTH2_TOKEN
    DROPBOX_CON = dropbox.Dropbox(DROPBOX_OAUTH2_TOKEN)
except AttributeError:
    # The test settings module does not have the dropbox token
    if (settings.DEFAULT_FILE_STORAGE != 'django.core.files.storage.FileSystemStorage'):
        msg = 'DEFAULT_FILE_STORAGE must be one of "django.core.files.storage.FileSystemStorage"'\
            ' or "storages.backends.dropbox.DropBoxStorage"'
        raise ValueError(msg)

# Create your tests here.
class EntryModelTest(TestCase):

    def setUp(self):
        # Create an Entry object to perform actions on
        entry_title = 'Test Title'
        entry_date = timezone.now()
        entry_abstract = 'Test Abstract'
        entry_show = True
        entry_slug = 'test-entry-slug'

        # Create a default author
        self.entry_authors = Author(first_name='Joe',
                                    last_name='Smith',
                                    email='first.last@example.com')
        self.entry_authors.save()

        # Create default blog foreign key
        blog_description = 'blog'
        self.blog = Blog(description=blog_description, id=1)
        self.blog.save()

        # A SimpleUploadFile is a proxy for an uploaded file attached through
        # a POST request
        raw_html = r"<h2>This is a test heading</h2><p>This is a test paragraph</p>"
        self.html_upload_file = SimpleUploadedFile('test_html_file.html', 
                                    raw_html.encode('utf-8'), 
                                    content_type="text/plain")
        raw_markdown = r'# This is a heading\n\nThis is some text\n\n*listitem'
        self.md_upload_file = SimpleUploadedFile('test_md_file.md', 
                                    raw_markdown.encode('utf-8'), 
                                    content_type="text/plain")
        
        self.entry_data = {'entry_title':entry_title,
                            'entry_abstract':entry_abstract,
                            'entry_date':entry_date,
                            'entry_slug':entry_slug,
                            }

        # Create a super user for interacting w/ admin interface
        self.username = 'content_tester'
        self.password = 'goldenstandard'
        self.user = User.objects.create_superuser(self.username, 'test@example.com', self.password)

        return None

    @staticmethod
    def _full_path(name):
        root_path = '/'
        base_path = root_path
        if name == '/':
            name = ''
        
        # If the machine is windows do not append the drive letter to file path
        if os.name == 'nt':
            final_path = os.path.join(root_path, name).replace('\\', '/')
            
            # Separator on linux system
            sep = '/'

            if (not os.path.normcase(final_path).startswith(os.path.normcase(base_path + sep)) and
                    os.path.normcase(final_path) != os.path.normcase(base_path) and
                    os.path.dirname(os.path.normcase(base_path)) != os.path.normcase(base_path)):
                raise SuspiciousFileOperation(
                    'The joined path ({}) is located outside of the base path '
                    'component ({})'.format(final_path, base_path))
            
            return final_path
        
        else:
            return safe_join(root_path, name).replace('\\', '/')

    def test_raw_save(self):
        """See where raw files are being saved. 
        Ensure the file is saved in the desired location within dropbox
         OR within the local file system depending on configuration
        """

        # Define a file for import and parsing
        raw_markdown = r'# This is a heading\n\nThis is some text\n\n*listitem'
        content = raw_markdown.encode()
        name = 'test-md-file.md'
        uploaded_file = ContentFile(content, name=name)

        # Create database instance
        entry = Entry()
        entry.entry_date = timezone.now()
        entry.entry_abstract = 'Some abstract data'
        entry.save(uploaded_raw_entry=uploaded_file)

        # Make sure the files were saved properly
        if (settings.DEFAULT_FILE_STORAGE == 'django.core.files.storage.FileSystemStorage'):
            self.assertTrue(os.path.exists(entry.raw_entry.path))
            self.assertTrue(os.path.exists(entry.html_content.path))
        elif (settings.DEFAULT_FILE_STORAGE == 'storages.backends.dropbox.DropBoxStorage'):
            # The root of this token is 'Apps/jv-webapp'. AKA Do not try to 
            # query the full file path 'Apps/jv-webapp/jv_blog/raw_entries/test-md-file.md'
            # Only use the path relative to the key
            file_metadata = DROPBOX_CON.files_get_metadata('/jv_blog/raw_entries/test-md-file.md')
            # Make sure the file was inserted into dropbox
            self.assertTrue(bool(file_metadata))

        # Delete old stuff so its not on the file system
        entry.raw_entry.delete(False)
        entry.html_content.delete(False)

        return None

    def test_save_directory_output(self):
        """Custom save path"""
        raw_entry_path = r"C:\Path-a/to b\file\markdown-sample.md"
        save_path_output = raw_directory_path(None, raw_entry_path)
        desired_path = r'jv_blog/raw_entries/{}'.format(os.path.split(raw_entry_path)[1])
        print('Output Save Path : ', save_path_output)
        print('Desired Save Path : ', desired_path)

        self.assertEqual(save_path_output, desired_path)

    def test_html_entry_add(self):
        """Input an HTML document into the chosen 'raw entry' attribute of 
        the Entry model
        ## Test ##
        I am adding raw html as the raw-entry input. This should parse the raw html and output
        it to both the raw_entry and entry_directory
        No exceptions should be raised during the process"""

        # Create database instance
        entry_data = self.entry_data
        test_entry = Entry(**entry_data)
        test_entry.save(uploaded_raw_entry=self.html_upload_file)
        test_entry.entry_authors.add(self.entry_authors)

        with test_entry.html_content.open(mode='rt') as f:
            print('Entry HTML Content file name : ', f.name)
            contents = f.read()
            print(contents[:25])

        # Make sure the files were saved properly
        if (settings.DEFAULT_FILE_STORAGE == 'django.core.files.storage.FileSystemStorage'):
            # Used for testing on a local machine, local file storage
            # FileField.path is not supported with remote storage
            raw_entry_name = test_entry.raw_entry.path 
            html_content_name = test_entry.html_content.path
            raw_entry_saved = os.path.isfile(raw_entry_name)
            html_content_saved = os.path.isfile(html_content_name)
            raw_entry_head = os.path.split(raw_entry_name)
            html_content_head = os.path.split(html_content_name)
            print('File {} Saved? : {}'.format(raw_entry_head, raw_entry_saved))
            print('File {} Saved? : {}'.format(html_content_head, html_content_saved))
            self.assertTrue(all((raw_entry_saved, html_content_saved)))

        elif (settings.DEFAULT_FILE_STORAGE == 'storages.backends.dropbox.DropBoxStorage'):
            # Retrieve file names from Dropbox manually (not through Django storage)
            raw_entry_name = test_entry.raw_entry.name 
            html_content_name = test_entry.html_content.name
            # The root of this token is 'Apps/jv-webapp'. AKA Do not try to 
            # query the full file path 'Apps/jv-webapp/jv_blog/raw_entries/test-md-file.md'
            file_metadata = DROPBOX_CON.files_get_metadata(self._full_path(raw_entry_name))
            self.assertEquals(file_metadata.path_display, self._full_path(raw_entry_name))
            file_metadata = DROPBOX_CON.files_get_metadata(self._full_path(html_content_name))
            self.assertEquals(file_metadata.path_display, self._full_path(html_content_name))

        # Delete file
        test_entry.raw_entry.delete(False)
        test_entry.html_content.delete(False)
        return None

    def test_html_entry_form(self):

        # Generate data to fill form
        raw_html = r"<h2>This is a test heading</h2><p>This is a test paragraph</p>"
        title = "test_docx_file.docx"
        file = SimpleUploadedFile(title, raw_html.encode('utf-8'), content_type="text/plain")
        entry_title = 'test_title'
        entry_date = timezone.now()
        entry_abstract = "Abstract Test"
        entry_slug = 'test-entry'
        entry_author = ['1']
        data = {'entry_title':entry_title,
                'entry_abstract':entry_abstract,
                'entry_date':entry_date,
                'entry_slug':entry_slug,
                'entry_authors':entry_author,
                }
        file_data = {'uploaded_raw_entry':file}

        # Create a model admin for testing form
        model_admin = EntryAdmin(model=Entry, admin_site=AdminSite())
        entry_form = model_admin.form(data=data, files=file_data)
        if len(entry_form.errors) > 0:
            print(entry_form.errors)
        self.assertTrue(len(entry_form.errors) == 0)

        file.close()

        return None

    def test_parse_html(self):
        """Parse different html raw entries
        Raw HTML entries are assumed to be encoded in utf-8 and
        will be read by the Entry.save() method as bytes"""

        raw_html = bytes('<img alt="√-4" class="sqrt" src="clustering1x.png"/>', encoding='utf-8')
        raw_entry_file = ContentFile(content=raw_html,
                                     name='/jv_blog/raw_entries/test_html.html')
        
        # Attempt to parse the HTML
        html_content = parse_raw_content(raw_entry_file)
        test_content = '<img alt="√-4" class="sqrt" src="clustering1x.png"/>\n'
        self.assertEqual(html_content, test_content)

        return None

    def test_markdown_entry_add(self):
        """Input a markdown document into 'raw-entry' attribute of Entry model
        and parse the result to HTML
        ## TEST ##
        The test is simple. 
        Are markdown files successfully parsed into HTML?
        Are markdown files saved?
        Are html files saved?"""

        # Define a file for import and parsing
        entry_data = self.entry_data
        test_entry = Entry(**entry_data)
        test_entry.save(uploaded_raw_entry=self.md_upload_file)
        test_entry.entry_authors.add(self.entry_authors)

        # Make sure the files were saved properly
        if (settings.DEFAULT_FILE_STORAGE == 'django.core.files.storage.FileSystemStorage'):
            # Used for testing on a local machine, local file storage
            # FileField.path is not supported with remote storage
            raw_entry_name = test_entry.raw_entry.path 
            html_content_name = test_entry.html_content.path
            raw_entry_saved = os.path.isfile(raw_entry_name)
            html_content_saved = os.path.isfile(html_content_name)
            raw_entry_head = os.path.split(raw_entry_name)
            html_content_head = os.path.split(html_content_name)
            print('File {} Saved? : {}'.format(raw_entry_head, raw_entry_saved))
            print('File {} Saved? : {}'.format(html_content_head, html_content_saved))
            self.assertTrue(all((raw_entry_saved, html_content_saved)))

        elif (settings.DEFAULT_FILE_STORAGE == 'storages.backends.dropbox.DropBoxStorage'):
            # Retrieve file names from Dropbox manually (not through Django storage)
            raw_entry_name = test_entry.raw_entry.name 
            html_content_name = test_entry.html_content.name
            # The root of this token is 'Apps/jv-webapp'. AKA Do not try to 
            # query the full file path 'Apps/jv-webapp/jv_blog/raw_entries/test-md-file.md'
            file_metadata = DROPBOX_CON.files_get_metadata(self._full_path(raw_entry_name))
            self.assertEquals(file_metadata.path_display, self._full_path(raw_entry_name))
            file_metadata = DROPBOX_CON.files_get_metadata(self._full_path(html_content_name))
            self.assertEquals(file_metadata.path_display, self._full_path(html_content_name))

        # Delete file
        test_entry.raw_entry.delete(False)
        test_entry.html_content.delete(False)
        return None

    def test_docx_entry_add(self):
        """Input a docx (microsoft word) document into 'raw-entry' 
        attribute of Entry model and parse the result to HTML
        ## TEST ##
        The test is simple. 
        Are docx files successfully parsed into HTML?
        Are docx files saved?
        Are html files saved?"""

        docx_file_path = r".\media\testing\word-doc-sample.docx"
        entry_data = self.entry_data
        test_entry = Entry(**entry_data)
        with open(docx_file_path, 'rb') as f:
            content = f.read()
            name = f.name
            docx_file = ContentFile(content, name=name)
        test_entry.save(uploaded_raw_entry=docx_file)
        test_entry.entry_authors.add(self.entry_authors)

        # Make sure the files were saved properly
        if (settings.DEFAULT_FILE_STORAGE == 'django.core.files.storage.FileSystemStorage'):
            # Used for testing on a local machine, local file storage
            # FileField.path is not supported with remote storage
            raw_entry_name = test_entry.raw_entry.path 
            html_content_name = test_entry.html_content.path
            raw_entry_saved = os.path.isfile(raw_entry_name)
            html_content_saved = os.path.isfile(html_content_name)
            raw_entry_head = os.path.split(raw_entry_name)
            html_content_head = os.path.split(html_content_name)
            print('File {} Saved? : {}'.format(raw_entry_head, raw_entry_saved))
            print('File {} Saved? : {}'.format(html_content_head, html_content_saved))
            self.assertTrue(all((raw_entry_saved, html_content_saved)))

        elif (settings.DEFAULT_FILE_STORAGE == 'storages.backends.dropbox.DropBoxStorage'):
            # Retrieve file names from Dropbox manually (not through Django storage)
            raw_entry_name = test_entry.raw_entry.name 
            html_content_name = test_entry.html_content.name
            # The root of this token is 'Apps/jv-webapp'. AKA Do not try to 
            # query the full file path 'Apps/jv-webapp/jv_blog/raw_entries/test-md-file.md'
            file_metadata = DROPBOX_CON.files_get_metadata(self._full_path(raw_entry_name))
            self.assertEquals(file_metadata.path_display, self._full_path(raw_entry_name))
            file_metadata = DROPBOX_CON.files_get_metadata(self._full_path(html_content_name))
            self.assertEquals(file_metadata.path_display, self._full_path(html_content_name))

        # Delete file
        test_entry.raw_entry.delete(False)
        test_entry.html_content.delete(False)
        return None

    def test_default_author_added(self):
        """A Default author should be added if none is defined when 
        creating an entry
        
        Expectation
        When saving an entry without defining an Author there should
        be a default author assigned by the entry model. The default
        author has a first name 'Anonymous' and last name 'Author'
        Equality is determined if both the first and last name match
        """

        # Create a test instance without an author defined
        entry_data = self.entry_data
        test_entry = Entry(**entry_data)
        test_entry.save(uploaded_raw_entry=self.md_upload_file)

        default_author = Author(first_name='Anonymous',
                                last_name='Author')

        self.assertEqual(test_entry.entry_authors.all()[0], default_author)

        # Delete old stuff so its not on the file system
        test_entry.raw_entry.delete(False)
        test_entry.html_content.delete(False)
        return None

    def test_delete_file_on_update(self):
        """Test if existing files are deleted when the Entry model 
        is updated
        This includes raw_entry and html_content
        ## What should happen? ##
        First, a file named media/jv_blog/raw_entries/markdown-sample.md should be created
        The markdown file is parsed and an HTML file is saved at media/jv_blog/entries/markdown-sample.html
        The model is saved
        A new raw entry is entered named sample.md
        a file named media/jv_blog/raw_entries/sample.md should be created
        The old file media/jv_blog/raw_entries/markdown-sample.md is deleted
        New html is parsed and saved media/jv_blog/entries/sample.html

        ## Test ##
        Make sure the files exist after the first save
        Make sure the new files were saved
        Make sure the old files were deleted
        """

        # Create an Entry object
        entry_data = self.entry_data
        test_entry = Entry(**entry_data)
        test_entry.save(uploaded_raw_entry=self.md_upload_file)
        test_entry.entry_authors.add(self.entry_authors)

        # Make sure the files were saved properly
        if (settings.DEFAULT_FILE_STORAGE == 'django.core.files.storage.FileSystemStorage'):
            # Used for testing on a local machine, local file storage
            # FileField.path is not supported with remote storage
            raw_entry_name = test_entry.raw_entry.path 
            html_content_name = test_entry.html_content.path
            raw_entry_saved = os.path.isfile(raw_entry_name)
            html_content_saved = os.path.isfile(html_content_name)
            raw_entry_head = os.path.split(raw_entry_name)
            html_content_head = os.path.split(html_content_name)
            print('File {} Saved? : {}'.format(raw_entry_head, raw_entry_saved))
            print('File {} Saved? : {}'.format(html_content_head, html_content_saved))
            self.assertTrue(all((raw_entry_saved, html_content_saved)))

        elif (settings.DEFAULT_FILE_STORAGE == 'storages.backends.dropbox.DropBoxStorage'):
            # Retrieve file names from Dropbox manually (not through Django storage)
            raw_entry_name = test_entry.raw_entry.name 
            html_content_name = test_entry.html_content.name
            # The root of this token is 'Apps/jv-webapp'. AKA Do not try to 
            # query the full file path 'Apps/jv-webapp/jv_blog/raw_entries/test-md-file.md'
            file_metadata = DROPBOX_CON.files_get_metadata(self._full_path(raw_entry_name))
            self.assertEquals(file_metadata.path_display, self._full_path(raw_entry_name))
            file_metadata = DROPBOX_CON.files_get_metadata(self._full_path(html_content_name))
            self.assertEquals(file_metadata.path_display, self._full_path(html_content_name))

        # Attempt to replace the old file
        raw_entry_name_v1 = test_entry.raw_entry.name # Keep track of original file name
        html_content_name_v1 = test_entry.html_content.name # Keep track of original file name
        test_entry.save(uploaded_raw_entry=self.html_upload_file)

        # Make sure the files were saved properly
        if (settings.DEFAULT_FILE_STORAGE == 'django.core.files.storage.FileSystemStorage'):
            # Used for testing on a local machine, local file storage
            # FileField.path is not supported with remote storage
            raw_entry_name = test_entry.raw_entry.path 
            html_content_name = test_entry.html_content.path
            raw_entry_saved = os.path.isfile(raw_entry_name)
            html_content_saved = os.path.isfile(html_content_name)
            raw_entry_head = os.path.split(raw_entry_name)
            html_content_head = os.path.split(html_content_name)
            print('File {} Saved? : {}'.format(raw_entry_head, raw_entry_saved))
            print('File {} Saved? : {}'.format(html_content_head, html_content_saved))
            self.assertTrue(all((raw_entry_saved, html_content_saved)))

        elif (settings.DEFAULT_FILE_STORAGE == 'storages.backends.dropbox.DropBoxStorage'):
            # Retrieve file names from Dropbox
            raw_entry_name = test_entry.raw_entry.name 
            html_content_name = test_entry.html_content.name
            # The root of this token is 'Apps/jv-webapp'. AKA Do not try to 
            # query the full file path 'Apps/jv-webapp/jv_blog/raw_entries/test-md-file.md'
            # Only use the path relative to the key
            file_metadata = DROPBOX_CON.files_get_metadata(self._full_path(raw_entry_name))
            self.assertEquals(file_metadata.path_display, self._full_path(raw_entry_name))
            file_metadata = DROPBOX_CON.files_get_metadata(self._full_path(html_content_name))
            self.assertEquals(file_metadata.path_display, self._full_path(html_content_name))


        # Make sure the original file was deleted
        if (settings.DEFAULT_FILE_STORAGE == 'django.core.files.storage.FileSystemStorage'):
            # Used for testing on a local machine, local file storage
            # FileField.path is not supported with remote storage
            raw_entry_saved = os.path.isfile(raw_entry_name_v1)
            html_content_saved = os.path.isfile(html_content_name_v1)
            self.assertFalse(raw_entry_saved)
            self.assertFalse(html_content_saved)

        elif (settings.DEFAULT_FILE_STORAGE == 'storages.backends.dropbox.DropBoxStorage'):
            # API Raises dropbox.exceptions.ApiError when file does not exist
            self.assertRaises(dropbox.exceptions.ApiError, DROPBOX_CON.files_get_metadata, self._full_path(raw_entry_name_v1))
            self.assertRaises(dropbox.exceptions.ApiError, DROPBOX_CON.files_get_metadata, self._full_path(html_content_name_v1))

        # Remove test file from file system
        test_entry.raw_entry.delete(False)
        test_entry.html_content.delete(False)
        return None


class AuthorModelTest(TestCase):

    def test_create_author(self):
        """Create a generic author so we can assign authors to articles.."""
        author = Author()
        author.name = 'John Vorsten'
        author.email = 'johnvorsten@yahoo.com'
        author.save()

        self.assertEqual(author.name, 'John Vorsten')

class IntegrationTest(TestCase):

    def test_reverse_resolve(self):
        """Test how URLs are reverse resolved for the jv_blog app"""
        url1 = reverse('projects:index')
        url2 = reverse('jv_blog:index')
        self.assertEqual(url1, '/projects/')
        self.assertEqual(url2, '/blog/')
        return None
