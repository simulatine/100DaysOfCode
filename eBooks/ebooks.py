#!python3
# -*- coding: utf-8 -*-
"""
ebooks.py - Set of Python functions for working with my Calibre, Amazon and
            Airtable eBook databases.

12 May, 2020 - Original version, get_airtable_books()
13 May, 2020 - Added load_calibre boooks() and compare_libraries()
14 May, 2020 - Added get_amazon_books() and update functions
"""

import json
import pprint
import sys

import airtable
import bs4
import tqdm

# The ebooksconf Python file contains environment specific variables:
# AIRTABLE_API_KEY - My unique Airtable API Key
# EBOOKS_DATABASE_ID - Unique Airtable database ID for my eBooks database
# JSON_FILE - JSON input file name containing the Calibre library contents
import ebooksconf

# DEBUG flag. Set this to True and add conditional print statements for quick
# and easy debugging.
# if DEBUG: print(...)
DEBUG = False


def get_airtable_books():
    """Get the list of books and authors from my AirTable eBooks database."""
    my_books = airtable.Airtable(
        ebooksconf.EBOOKS_DATABASE_ID,
        "Books",
        api_key=ebooksconf.AIRTABLE_API_KEY,
    )
    my_authors = airtable.Airtable(
        ebooksconf.EBOOKS_DATABASE_ID,
        "Authors",
        api_key=ebooksconf.AIRTABLE_API_KEY,
    )

    books = {}
    # Iterate through the table and generate a list of file names
    print("Getting AirTable data")
    for book in tqdm.tqdm(my_books.get_all()):

        title = book["fields"]["Title"]
        books[title] = {}
        books[title]["id"] = book["id"]
        books[title]["Amazon Title"] = book["fields"]["Amazon Title"]
        books[title]["Purchase Date"] = book["fields"]["Purchase Date"]
        books[title]["Source"] = book["fields"]["Source"]
        try:
            books[title]["Copied to Calibre"] = book["fields"][
                "Copied to Calibre"
            ]
        except KeyError:
            books[title]["Copied to Calibre"] = False

        # The Authors field contains a list of zero or more links to records in
        # the separate Authors table.
        author_ids = book["fields"]["Authors"]
        authors = []
        for author_id in author_ids:
            # Open each linked Author record, and get the author's name
            author = my_authors.get(author_id)
            author_name = author["fields"]["Name"]
            authors.append(author_name)
        books[title]["Authors"] = authors
    print("Got {} books from Airtable".format(len(books)))
    return books


def get_amazon_books():
    """Get the list of books and authors from my Amazon content library."""
    titles = []
    authors = []
    purchase_dates = []
    num_books = 0
    num_authors = 0
    num_purchase_dates = 0

    print("Getting Amazon data")
    for source in ebooksconf.AMAZON_CONTENT_PAGES:
        # I found it necessary to force the encoding to 'utf-8'
        # Leaving this out caused issues with some book titles
        with open(source, encoding="utf-8") as html_file:
            html_content = html_file.read()
            soup = bs4.BeautifulSoup(html_content, "html.parser")

            # Get the list of books
            for div in soup.find_all("div", attrs={"bo-text": "tab.title"}):
                titles.append(str(div.string))
                num_books += 1

            # Get the list of authors
            for div in soup.find_all("div", attrs={"bo-text": "tab.author"}):
                authors.append(div.string)
                num_authors += 1

            # Get the list of purchase dates
            for div in soup.find_all(
                "div", attrs={"bo-text": "tab.purchaseDate"}
            ):
                purchase_dates.append(div.string)
                num_purchase_dates += 1

    # Create a dictionary keyed on the book title
    counter = 0
    books = {}
    for title in titles:
        # The dictionary value is a list containing the author's name
        books[title] = {}
        books[title]["Authors"] = authors[counter]
        books[title]["Purchase Date"] = purchase_dates[counter]
        counter += 1
    print("Got {} books from Amazon".format(len(books)))
    return books


def load_calibre_books():
    """
    Load the list of Calibre books and authors from a JSON file.

    The JSON file should have been created by running the separate
    get_calibre_library.py program using calibre-debug:
    $ calibre-debug get_calibre_library.py
    """
    print("Getting Calibre data")
    with open(ebooksconf.JSON_FILE) as json_input:
        books = json.load(json_input)
    print("Got {} books from Calibre".format(len(books)))
    return books


def update_source(airtable_books, amazon_books):
    """Update my Airtable to show if the book was bought from Amazon."""
    my_books = airtable.Airtable(
        ebooksconf.EBOOKS_DATABASE_ID,
        "Books",
        api_key=ebooksconf.AIRTABLE_API_KEY,
    )

    airtable_database = my_books.get_all()
    updated = 0
    print("Updating Airtable 'Source' field")
    for book in airtable_books:
        book_id = airtable_books[book]["id"]
        amazon_title = airtable_books[book]["Amazon Title"]
        if amazon_title in amazon_books:
            # Update the Airtable record
            if airtable_books[book]["Source"] != "Amazon.co.uk":
                updated += 1
                print(
                    "{}: Updating Airtable record for Amazon book".format(book)
                )
                my_books.update(book_id, {"Source": "Amazon.co.uk"})
        else:
            # Book was not sourced from Amazon
            if airtable_books[book]["Source"] == "Amazon.co.uk":
                print(
                    "{}: Book not sourced from Amazon says it is".format(book)
                )
    print("Updated {} Airtable records".format(updated))


def update_calibre_flag(airtable_books, calibre_books):
    """Update Airtable to show if the book is on Calibre."""
    my_books = airtable.Airtable(
        ebooksconf.EBOOKS_DATABASE_ID,
        "Books",
        api_key=ebooksconf.AIRTABLE_API_KEY,
    )

    airtable_database = my_books.get_all()
    updated = 0
    print("Updating Airtable 'Copied to Calibre' flag")
    for book in tqdm.tqdm(airtable_books):
        book_id = airtable_books[book]["id"]
        calibre_flag = airtable_books[book]["Copied to Calibre"]
        if book in calibre_books and not calibre_flag:
            # Book is in the Calibre database
            updated += 1
            my_books.update(book_id, {"Copied to Calibre": True})
        elif book not in calibre_books and calibre_flag:
            # Book is not in Calibre
            updated += 1
            my_books.update(book_id, {"Copied to Calibre": False})
    print("Updated {} Airtable records".format(updated))


def compare_libraries(lib1, name1, lib2, name2):
    """Compare two book libraries."""
    # First compare the book titles (which are the dictionary keys)
    set1 = set(lib1.keys())
    set2 = set(lib2.keys())

    print("\n\n{} books missing from {}".format(name2, name1))
    pprint.pprint(sorted(set2 - set1))
    print("{} books missing from {}".format(len(set2 - set1), name1))

    print("\n\n{} bookss missing from {}".format(name1, name2))
    pprint.pprint(sorted(set1 - set2))
    print("{} books missing from {}".format(len(set1 - set2), name2))


def save_data(object, filename):
    """Save a Python object to a text file."""
    with open(filename, "w") as output:
        output.write(pprint.pformat(object))


def main():
    """Compare lists of books from multiple sources."""
    # Comment out lines as required.

    # Get the list of book and authors from AirTable
    airtable_books = get_airtable_books()
    # save_data(airtable_books, "Airtable_Books.txt")

    # Get the list of books and authors from Amazon
    amazon_books = get_amazon_books()
    # save_data(amazon_books, "Amazon_Books.txt")

    # Get the list of books and authors from Calibre
    calibre_books = load_calibre_books()
    # save_data(calibre_books, "Calibre_Books.txt")

    if DEBUG:
        print("Airtable database has {} books".format(len(airtable_books)))
        print("Amazon library has {} books".format(len(amazon_books)))
        print("Calibre library has {} books".format(len(calibre_books)))
        pprint.pprint(amazon_books)
        pprint.pprint(airtable_books)
        pprint.pprint(calibre_books)

    # Update functionality
    # update_calibre_flag(airtable_books, calibre_books)
    # update_source(airtable_books, amazon_books)

    # Compare any two libraries
    # compare_libraries(amazon_books, "Amazon", airtable_books, "Airtable")


if __name__ == "__main__":
    main()
