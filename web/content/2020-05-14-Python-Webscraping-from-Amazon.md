Title: Day 8: Python Webscraping from Amazon
Date: 2020-05-14
Category: Posts

## Continuing my ebook library management with Python ##

Over the last two days, I worked on two Python functions to extract data
from my 
[Calibre ebook library](https://simulatine.github.io/100DaysOfCode/day-6-python-and-calibre.html)
and from an 
[Airtable database](https://simulatine.github.io/100DaysOfCode/day-7-python-and-airtable.html)
I had created to track my ebooks.

Today I continued to expand my library functions by getting my Amazon digital
content. This involved learning about webscraping and the Python
`beautifulsoup` library.

## Amazon and Webscraping ##

Webscraping involves reading the content of a web page and extracting useful
information from it. Amazon deliberately makes this hard as they don't want
competitors and price comparison sites easily getting page content. They do
this by:

- Using A/B testing (where they randomly present different versions of the same
page on repeated visits).
- Continuously making small changes to the layout and site contents
- Moving content inside iFrames
- Using Captcha and similar login related hurdles


### Downloading my Amazon digital content list ###

With that caveat in mind, I found it easier to download the pages I wanted
from Amazon's website, and do the page scraping and data extraction on my local
disk. This meant that I was dealing with fixed web pages, and could repeatedly
modify and test my code against a local file, without the page constantly
changing, and without the hassle of Amazon's login API.

From the Account link in the top right of the Amazon home page, I went to the
[Manage your Content and Devices](https://www.amazon.com/mycd/myx)
link. This gave me a list of all the digital books I had ever bought from
Amazon. I used my browser's save function (Ctrl+S) to save the page.

![Amazon Manage Your Contents]({static}/images/2020-05-14_Amazon_Manage_Your_Contents_Screenshot.png)

I found that the page was limited to 200 items, so I had to scroll down to the
bottom and click *Show More* to get the second page of results. I also saved
this second page, so I now had two HTML files on my local disk:

- `Amazon_Content_Page_1.html`
- `Amazon_Content_Page_2.html`

## Beautifulsoup ##

To parse the HTML files I used a popular Python library called
[beautifulsoup](https://www.crummy.com/software/BeautifulSoup/).

I assume it was given that name as it has the ability to turn
[tag soup](https://en.wikipedia.org/wiki/Tag_soup)
into a beautiful Python object based tree structure. OK, so it has a weird
name, but it is very powerful. Like all powerful software tools, it took some
learning and experimentation to get the most out of it.

First of all, I installed the library

    pip install beautifulsoup4
    
Then, at the start of my script, I had to import it

    install bs4


## Writing the code ##

First, I created a function and initiated a number of variables

    def get_amazon_books():
        """Get the list of books and authors from my Amazon content library."""
        titles = []
        authors = []
        purchase_dates = []
        num_books = 0
        num_authors = 0
        num_purchase_dates = 0

I then created a loop to go through each of the "My Content" HTML files which I
had previously downloaded to my local disk.
        
        # List of Amazon "Manage Your Content and Devices" HTML files
        AMAZON_CONTENT_PAGES = [
        "Amazon_Content_Page_1.html",
        "Amazon_Content_Page_2.html",
        ]

        print("Getting Amazon data")
        for source in AMAZON_CONTENT_PAGES:
        
Inside the loop, I opened each HTML file and used BeautifulSoup to parse it.
When opening the HTML file, I found it necessary to force the encoding to
Unicode with `encoding="utf-8"`. Otherwise, I had issues reading some book
titles and author names containing Unicode characters.
        
            with open(source, encoding="utf-8") as html_file:
                html_content = html_file.read()
                soup = bs4.BeautifulSoup(html_content, "html.parser")

Now came the hard part. I had to experiment quite a bit to determine how best
to extract the data I wanted. After reviewing the source HTML data, I noticed
that Amazon used the identifier `bo-text` inside `<div>` statements to identify
the title, author and purchase date:

    <div class="myx-column" bo-text="tab.title" title="1984">1984</div>
    ...
    <div class="myx-column" bo-text="tab.author" title="George Orwell">George Orwell</div>

*(I removed a lot of extraneous CSS from the above div statements to show the
key attributes)*

This allowed me to search for the `bo-text` attribute, and extract the data I
needed:

                # Get the list of books
                for div in soup.find_all("div", attrs={"bo-text": "tab.title"}):
                    titles.append(div.string)
                    num_books += 1

                # Get the list of authors
                for div in soup.find_all("div", attrs={"bo-text": "tab.author"}):
                    authors.append(div.string)
                    num_authors += 1

                # Get the list of purchase dates
                for div in soup.find_all("div", attrs={"bo-text": "tab.purchaseDate"}):
                    purchase_dates.append(div.string)
                    num_purchase_dates += 1

As I did for my Calibre and Airtable functions, I created a dictionary keyed
off the title to store the data for each ebook, in this case, the Authors and
Purchase Date.

        books = {}
        for title in titles:
            books[title] = {}
            books[title]["Authors"] = authors[counter]
            books[title]["Purchase Date"] = purchase_dates[counter]
        print("Got {} books from Amazon".format(len(books)))
        return books

I can now call this function and display the results with pprint.

    if __name__ == "__main__":
        amazon_books = get_amazon_books()
        pprint.pprint(amazon_books)

## Conclusion ##

Over the
[last](https://simulatine.github.io/100DaysOfCode/day-6-python-and-calibre.html)
[three](https://simulatine.github.io/100DaysOfCode/day-7-python-and-airtable.html)
[days](https://simulatine.github.io/100DaysOfCode/day-8-python-webscraping-from-amazon.html)
I created three similar functions in Python:

- `get_calibre_books()`
- `get_airtable_books()`
- `get_amazon_books()`

Each function gets a list of ebooks from the specific source, and creates a
Python dictionary using the book's title as the key.

I can now compare and search on the results of these three functions,
allowing me to identify, for example, books that I bought from Amazon that
were not listed in my Airtable database.

Today's work taught me a lot about webscraping, the Python BeautifulSoup
library, and the many blockers that Amazon place in the way of webscraping
their data!

The full source code for today's work is in my Github repository here:

[https://github.com/simulatine/100DaysOfCode/blob/master/eBooks/ebooks.py](https://github.com/simulatine/100DaysOfCode/blob/master/eBooks/ebooks.py)

