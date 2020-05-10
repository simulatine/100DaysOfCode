#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Simulatine'
SITENAME = "Simulatine's 100 Days of Code Blog"
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/London'

DEFAULT_LANG = 'en'

# Simulatine, 10 May 2020 - Added a static folder. Files in this folder will be
#                           copied to the output directory without modification 
STATIC_PATHS = ['images']

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

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True