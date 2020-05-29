Title: Day 6: Python and Calibre
Date: 2020-05-12
Category: Posts

## Using Python to manage an ebook library ##

I have a growing library of more than 350 digital ebooks. Today I started
to write some Python code to help me track and search my ebook library.

*A short aside on nomenclature: ebook, e-book, eBook or e-Book? It seems there
is no standard term to describe a digital book. In this article I will use the
simplest form *ebook*, which is similar to email.*

## Calibre ##

![Calibre]({static}/images/2020-05-12_Calibre_eBook_Screenshot.jpg)

[Calibre](https://calibre-ebook.com/) is a powerful open source ebook
manager. It provides the ability to read, store and convert ebooks in many
formats.

I had most of my ebooks in Calibre, but was missing a few which were scattered
elsewhere on my laptop's hard disk. I also wanted to check my Calibre library
against my Amazon purchase history, but didn't want to do this manually.

To help me achieve this, I wrote a Python function to extract the details of my
Calibre library allowing me to easily manipulate and search the data.

## Python and Calibre ##

Interestingly, Calibre is developed in Python, and actually includes an entire
embedded copy of the Python interpreter. To access the Calibre library, I
had to call my script with 
[Calibre in debug mode](https://manual.calibre-ebook.com/generated/en/calibre-debug.html)
:

    calibre-debug <python-script>

This caused a number of challenges:

1. The embedded interpreter had access to the standard Python libraries, but
not to any other modules I had installed wih `pip`. This meant that my script
was limited to using standard Python library functions.

2. A further complexity was that the Python interpreter embedded in Calibre,
at least as of Calibre version 4.15 in May 2020, is the older Python 2,
specifically Python 2.7.16. This meant I couldn't use any Python 3 code, which
clashes with most of my other Python scripts, where I make considerable use of
newer Python 3 features (I actually discovered this problem when trying to use
the `Pathlib` module to manage the path to my Calibre library - Pathlib is
Python 3 only!)

For these two reasons, I decided to create a standalone Python 2 script to
extract the Calibre library and save it to disk. I will leave the searching and
comparison with Amazon to a separate Python 3 script.

## Writing the code ##
First, I imported the Calibre API `calibre.library` and also the Python pretty
printer module `pprint`:

    import calibre.library
    import pprint
    
Next, I created a function `get_calibre_books()` to open the Calibre library
and get the data:

    def get_calibre_books():
        """Get the list of books and authors from my Calibre eBook library."""
        # First open the Calibre library and get a list of the book IDs
        calibre_db = calibre.library.db(
            ebooksconf.CALIBRE_LIBRARY_LOCATION
        ).new_api
        book_ids = calibre_db.all_book_ids()
        print("Got {} book IDs from Calibre library".format(len(book_ids)))

Calibre returns its data with a unique numeric ID for each ebook. I wanted to
compare the Calibre data with a list of ebooks from Amazon, so needed a
different key common to both data sources. I decided to use the ebook title as
the unique key. This could cause some issues if I had two ebooks with *exactly*
the same title, but so far that hasn't been a problem for me.

So I created a new dictionary, to store the data in the format I want, with the
dictionary key set to the book title. I displayed an error if I found two books
with exactly the same title.

*Note: as an exercise for the future, I could improve the error handling here
using try/except, and using the Python `logging` module to improve the error
logging.*

    books = {}
    for book in book_ids:
        title = calibre_db.field_for("title", book)
        if title in books:
            print("ERROR: Duplicate book found for title {}".format(title))

My dictionary values were the ebook author, or to be precise, authors. As some
ebooks have more than one author, Calibre returns a list rather than a single
string. The list could potentially have had zero elements if I didn't have any
author listed for the ebook in Calibre, but in practice that has not been the
case for my library.

For the moment, I am not interested in the many other fields in the Calibre
library. If I wanted, I could have extracted the ebook format, cover picture,
publisher, date etc. I can get a full list of fields for a book with the
following code:

    metadata = calibre_db.get_metadata(book_id)
    print(metadata.standard_field_keys())

The [Calibre API documentation](https://manual.calibre-ebook.com/develop.html#api-documentation-for-various-parts-of-calibre)
has a lot more details.

After adding the authors data as a dictionary value, I completed the function
by returning the entire `books` dictionary to the caller.

    books = {}
    for book in book_ids:
        title = calibre_db.field_for("title", book)
        if title in books:
            print("ERROR: Duplicate book found for title {}".format(title))
        else:
            # The authors field contains a list of zero or more author names
            authors = calibre_db.field_for("authors", book)
            books[title] = authors
    return books

I can now create the main part of my script, calling my get_calibre_books()
function, and displaying the results with pprint.

    if __name__ == "__main__":
        calibre_books = get_calibre_books()
        pprint.pprint(calibre_books)


## Exporting the data ##

Now that I have the data in a Python dictionary, I want to save it to disk
so I can access it from other Python 3 scripts. There are several ways to do
this. Python has a built in `pickle` module that saves any Python object to a
file. I could also simply write my dictionary contents in plain text to a text
file. I decided to save to a JSON file format:

    print("Writing {} books to JSON".format(len(calibre_books)))
    with open(ebooksconf.JSON_FILE, "w") as output:
        json.dump(calibre_books, output)

## Conclusion ##

I now have a short script that extracts my Calibre library contents and saves
it to a JSON file. In a later blog post, I will show I can use this data
to search and compare with other sources. The full source code is in my
Github repository here:

[https://github.com/simulatine/100DaysOfCode/blob/master/eBooks/get_calibre_library.py](https://github.com/simulatine/100DaysOfCode/blob/master/eBooks/get_calibre_library.py)

Creating this script taught me about the Calibre API, how to restructure
data with a Python dictionary, and how to save data with JSON.

Tomorrow I will look at doing something similar with ebook data that I
maintain online in [Airtable](https://https://airtable.com/).
