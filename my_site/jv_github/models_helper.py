# Django imports
from django.conf import settings

# Python imports 
import os

# Define SVG images that can be associated with a github repository
SVG_CHOICES = [
    (os.path.join(settings.STATIC_URL,'jv_github','images','add_a_photo-24px.svg'), 'Insert Photo'),
    (os.path.join(settings.STATIC_URL,'jv_github','images','insert_photo-24px.svg'), 'Add Photo'),
    (os.path.join(settings.STATIC_URL,'jv_github','images','description-24px.svg'), 'Clipboard / Assignment'),
    (os.path.join(settings.STATIC_URL,'jv_github','images','deck-24px.svg'), 'Chairs / Deck'),
    (os.path.join(settings.STATIC_URL,'jv_github','images','assignment-24px.svg'), 'Description / Paper'),
    (os.path.join(settings.STATIC_URL,'jv_github','images','emoji_objects-24px.svg'), 'Light Bulb / Idea'),
    (os.path.join(settings.STATIC_URL,'jv_github','images','image_search-24px.svg'), 'Search / Image Search'),
    (os.path.join(settings.STATIC_URL,'jv_github','images','mail-24px.svg'), 'Mail'),
    (os.path.join(settings.STATIC_URL,'jv_github','images','memory-24px.svg'), 'Memory / Computer Chip'),
    (os.path.join(settings.STATIC_URL,'jv_github','images','mood-24px.svg'), 'Smiley Face'),
    (os.path.join(settings.STATIC_URL,'jv_github','images','pie_chart-24px.svg'), 'Pie Chart'),
    (os.path.join(settings.STATIC_URL,'jv_github','images','scatter_plot-24px.svg'), 'Scatter Plot'),
    (os.path.join(settings.STATIC_URL,'jv_github','images','score-24px.svg'), 'Score / Line Graph'),
    (os.path.join(settings.STATIC_URL,'jv_github','images','sports_golf-24px.svg'), 'Golf Ball'),
    (os.path.join(settings.STATIC_URL,'jv_github','images','square_foot-24px.svg'), 'Protractor'),
    (os.path.join(settings.STATIC_URL,'jv_github','images','weekend-24px.svg'), 'Couch / Sofa'),
    (os.path.join(settings.STATIC_URL,'jv_github','images','link-24px.svg'), 'Link / Chainlink / hyperlink'),
]