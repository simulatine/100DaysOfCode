#!python2
# -*- coding: utf-8 -*-
"""
get_calibre_library.py - Get my Calibre eBook library and dump to JSON.

13 May, 2020 - Original version
13 May, 2020 - Reformatted with black formatter.
               Passes pycodestyle, pydocstyle and flake8 checks.

IMPORTANT: Run this program using calibre-debug, rather than using Python
directly:
$ calibre-debug calibre_testing.py

This program reads a Calibre eBook database, extracts the list of book titles
and authors, and saves the resulting dictionary to a JSON file. I can then
read this dictionary from other programs.

This is part of a toolkit for comparing my Calibre eBook library with my
Amazon Kindle library, as well as with my Airtable database. Ideally I would
have the Calibre and Airtable functions in a single program. However I need to
run this program with Python 2, whereas all of my other current development is
in Python 3.

The reason for Python 2 is that the only easy way to access a Calibre database
is by running Calibre in debug mode, which allows you to execute a Python
script. See:
https://manual.calibre-ebook.com/develop.html#using-calibre-in-your-projects

This starts a separate version of Python embedded in Calibre. As of
May 2020, the current version Calibre 4.15 includes Python 2.7.16, which means
I cannot use Python 3 features and librares.
"""

import json
import pprint

import calibre.library

# The ebooksconf Python file contains environment specific variables:
# CALIBRE_LIBRARY_LOCATION - folder location of the Calibre library
# JSON_FILE - output file name for writing the Calibre library contents
import ebooksconf

# DEBUG flag. Set this to True and add conditional print statements for quick
# and easy debugging.
# if DEBUG: print(...)
DEBUG = False


def get_calibre_books():
    """Get the list of books and authors from my Calibre eBook library."""
    # First open the Calibre library database and get a list of the book IDs
    calibre_db = calibre.library.db(
        ebooksconf.CALIBRE_LIBRARY_LOCATION
    ).new_api
    book_ids = calibre_db.all_book_ids()
    print("Got {} book IDs from Calibre database".format(len(book_ids)))

    # Create a dictionary with the book contents
    # The dictionary key is the book title
    # The dictionary value is a list of zero or more authors for the book
    books = {}
    for book in book_ids:
        title = calibre_db.field_for("title", book)
        if title in books:
            print("Duplicate book found for title {}".format(title))
        else:
            # The authors field contains a list of zero or more author names
            authors = calibre_db.field_for("authors", book)
            books[title] = authors
    return books


def main():
    """Get the list of books and dump them to a JSON output file."""
    calibre_books = get_calibre_books()
    if DEBUG:
        pprint.pprint(calibre_books)

    # Dump the data to a JSON file
    print("Writing {} books to JSON".format(len(calibre_books)))
    with open(ebooksconf.JSON_FILE, "w") as output:
        json.dump(calibre_books, output)


if __name__ == "__main__":
    main()
