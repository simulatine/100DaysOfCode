#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# Simulatine, 10 May 2020 - Set the site details
AUTHOR = 'Simulatine'
SITENAME = "Simulatine's 100 Days of Code Blog"
SITEURL = 'https://simulatine.github.io/100DaysOfCode'

PATH = 'content'

TIMEZONE = 'Europe/London'

DEFAULT_LANG = 'en'

# Simulatine, 10 May 2020 - Added static folders. Files in these folders will
#                           be copied to the output directory without
#                           modification 
STATIC_PATHS = ['images', 'extras']

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
'''
# Original version
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)
'''

# Simulatine, 10 May 2020 - Added links. These will appear in the page footer
#                           (or page header, depending on the theme layout).
LINKS = (('Python', 'https://python.org/'),
         ('Pygame', 'https://www.pygame.org/docs/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),)

# Simulatine, 10 May 2020 - Added social links. Pelican will add icons for
#                           commonly used social media sites.
SOCIAL = (('Twitter', 'https://twitter.com/simulatine'),
          ('GitHub', 'https://github.com/simulatine/100DaysOfCode'),)

# Simulatine, 10 May 2020 - Added my twitter username
#                           This adds a button at the top of article pages,
#                           encouraging others to tweet about them.
TWITTER_USERNAME = 'Simulatine'


# Simulatine, 10 May 2020 - Updated the standard date format to show the full
#                           day of the week. Example: Sunday, 10 May 2020
DEFAULT_DATE_FORMAT = '%A, %d %B %Y'

# Simulatine, 10 May 2020 - Limit summaries of blog posts to 25 words.
SUMMARY_MAX_LENGTH = 25

DEFAULT_PAGINATION = 10

# Simulatine, 10 May 2020 - Added a favicon link.
EXTRA_PATH_METADATA = {
    'extras/favicon.ico': {'path': 'favicon.ico'},
}

# Simulatine, 10 May 2020 - Try a different theme.
THEME = "notmyidea"


# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True