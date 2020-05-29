Title: Day 7: Python and Airtable
Date: 2020-05-13
Category: Posts

## Continuing my ebook library management with Python ##

Yesterday, I developed a
[Python function](https://simulatine.github.io/100DaysOfCode/day-6-python-and-calibre.html)
to extract data from the Calibre ebook manager.

Today I wanted to extend this to extracting similar data from Airtable.

## Airtable ##

[Airtable](https://https://airtable.com/) is an online database/spreadsheet
tool that allows me to save and manage data online. The basic interface is
very much like an online spreadsheet, such as the 
[Google Sheets](https://docs.google.com/spreadsheets/u/0/)
component of Google Docs.

![Airtable screenshot]({static}/images/2020-05-13_Airtable_Screenshot.png)
*Image by Kvysyar from [Wikipedia](https://commons.wikimedia.org/w/index.php?curid=46824078)*

Airtable's power comes from its API, which provides remote access to the data,
giving me the ability to search, edit and update the data from a Python script.

I had actually played with Airtable previously, and started to create a
database (called a "base" by Airtable) to store a list of my ebooks, by
directly typing in the ebook details on screen. Rather than trying to manually
complete this database, I decided to use the power of Python!

## Using Python with Airtable  ##

Airtable has a simple
[Python API wrapper](https://airtable-python-wrapper.readthedocs.io/en/master/)
which I used to access my data.

Two key IDs I needed were my Personal API Key, which is unique to me and is
required to access my data via the API, and the Database ID, which uniquely
identifies my database.

The Personal API Key is visible by going to to my **Account Overview** on the
Airtable website. The Database ID is visible by opening the base on the
Airtable website, and then clicking on **Help** and **API Documentation**.

Both of these are unique to me, and I saved them in a separate Python module
which i called `ebooksconf.py`.

    AIRTABLE_API_KEY = "********"
    EBOOKS_DATABASE_ID = "********"

## Writing the code ##

I first needed to install the Airtable wrapper library:

    pip install airtable-python-wrapper

Then in my Python script, I imported the library:

    import airtable

I next wrote a function `get_airtable_books()` to read my ebooks and authors.
I have two separate tables *Books* and *Authors* in my ebooks database, so
I read both of them.

    def get_airtable_books():
        """Get the list of books and authors from my AirTable ebooks database."""
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

Airtable returns its data with a unique ID key for each record. I wanted to
compare this data with other sources, such as my Calibre library, so the
Airtable key is not relevant for my needs. I took a similar approach to the way
I dealt with Calibre data yesterday, creating a new Python dictionary, keyed
off the book title rather than the record ID.

I read in a number of different fields into the dictionary, including the
Purchase Date and the original Source (mostly [Amazon](https://www.amazon.com),
but I also bought some of my ebooks from
[OReilly.com](http://shop.oreilly.com/),
[humblebundle.com](https://www.humblebundle.com/) and other sources).

*Note: the loop below took some time to to through each of my Airtable
records. I added the `tqdm` progress bar to visually show activity. Otherwise
not much seemed to happen for a minute or more. I had this already installed
`tqdm` on my system (`pip install tqdm`) and imported (`import tqdm`) at the
start of my script. I probably should optimize this loop at some future stage
so that the progress bar is not required.*

        books = {}
        # Iterate through the table and generate a list of file names
        print("Getting AirTable data")
        for book in tqdm.tqdm(my_books.get_all()):

            title = book["fields"]["Title"]
            books[title] = {}
            books[title]["id"] = book["id"]
            books[title]["Purchase Date"] = book["fields"]["Purchase Date"]
            books[title]["Source"] = book["fields"]["Source"]

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

I can now call this function and display the results with pprint.

    if __name__ == "__main__":
        airtable_books = get_airtable_books()
        pprint.pprint(airtable_books)

## Conclusion ##

Combining
[yesterday's](https://simulatine.github.io/100DaysOfCode/day-6-python-and-calibre.html)
and today's work, I now have two functions which get data from  Calibre and
Airtable, and restructures that data into two similar Python dictionaries.

Today's work taught me about the Airtable API, and how to get data from a
remote cloud source.

The full source code for today's work is in my Github repository here:

[https://github.com/simulatine/100DaysOfCode/blob/master/eBooks/ebooks.py](https://github.com/simulatine/100DaysOfCode/blob/master/eBooks/ebooks.py)

