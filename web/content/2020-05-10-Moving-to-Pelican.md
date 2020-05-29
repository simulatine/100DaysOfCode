Title: Day 4: Moving from Jekyll to Pelican
Date: 2020-05-10
Category: Posts

## Trying Pelican ##

I am trying out using [Pelican](https://docs.getpelican.com/en/stable/) to
create this site, as a replacement for [Jekyll](https://jekyllrb.com/) with the
[Minima](https://github.com/jekyll/minima) theme, provided by default with
GitHub Pages. Pelican is a static site generator, and is conceptually very
similar to Jekyll - it converts simple text files in
[Markdown](https://daringfireball.net/projects/markdown/) format into a
fully fledged website. But Pelican is Python based, which feels a lot more
natural to me.

## Installing Pelican ##

I started by installing the pelican and markdown libraries:

    pip install pelican markdown

I then followed instructions at the
[Pelican quickstart guide](https://docs.getpelican.com/en/stable/quickstart.html#installation) to
create and configure my site.

I first created a folder for my website:

    mkdir C:\Users\Simulatine\Documents\Git\100DaysOfCode\web

I went to the website folder and ran `pelican-quickstart` to create the initial structure

    cd C:\Users\Simulatine\Documents\Git\100DaysOfCode\web
    pelican-quickstart
    
    Welcome to pelican-quickstart v4.2.0.

    This script will help you create a new Pelican-based website.
    Please answer the following questions so this script can generate the files
    needed by Pelican.

    > Where do you want to create your new web site? [.]
    > What will be the title of this web site? Simulatine's 100 Days of Code
    > Who will be the author of this web site? Simulatine
    > What will be the default language of this web site? [English]
    > Do you want to specify a URL prefix? e.g., https://example.com   (Y/n) Y
    > What is your URL prefix? (see above example; no trailing slash) https://simulatine.github.io/100DaysOfCode/
    > Do you want to enable article pagination? (Y/n)
    > How many articles per page do you want? [10]
    > What is your time zone? [Europe/Paris] Europe/London
    > Do you want to generate a tasks.py/Makefile to automate generation and publishing? (Y/n)
    > Do you want to upload your website using FTP? (y/N)
    > Do you want to upload your website using SSH? (y/N)
    > Do you want to upload your website using Dropbox? (y/N)
    > Do you want to upload your website using S3? (y/N)
    > Do you want to upload your website using Rackspace Cloud Files? (y/N)
    > Do you want to upload your website using GitHub Pages? (y/N) Y
    > Is this your personal page (username.github.io)? (y/N) n
    Done. Your new project is available at C:\Users\Simulatine\Documents\Git\100DaysOfCode\web

This created subfolders called `content` and `output`, as well as a Makefile and some default Python scripts `pelicanconf.py`, `publishconf.py` and `tasks.py`.

    dir
    
    Volume in drive C has no label.
    Volume Serial Number is 5C84-C174

    Directory of C:\Users\Simulatine\Documents\Git\100DaysOfCode\web

    2020-05-10  15:34    <DIR>          .
    2020-05-10  15:34    <DIR>          ..
    2020-05-10  15:11    <DIR>          content
    2020-05-10  14:54             2,914 Makefile
    2020-05-10  15:17    <DIR>          output
    2020-05-10  15:23               878 pelicanconf.py
    2020-05-10  14:54               632 publishconf.py
    2020-05-10  14:54             3,615 tasks.py
               4 File(s)          8,039 bytes
               4 Dir(s)  51,526,713,344 bytes free

As suggested in the
[quickstart guide](https://docs.getpelican.com/en/stable/quickstart.html#installation),
I next created a trial web source page `keyboard-review.md` in the `content`
folder, with some markdown content:

    Title: My First Review
    Date: 2020-05-08 10:20
    Category: Review

    Following is a review of my favorite mechanical keyboard.

I attempted to generate the site output by going to the top website folder and
running pelican against the `content` folder.

    pelican content

I received the following notification:

    WARNING: Docutils has no localization for 'english'. Using 'en' instead.
    ERROR: Skipping C:\Users\Simulatine\Documents\Git\100DaysOfCode\web\content\keyboard-review.md: could not find information about 'title'
    Done: Processed 0 articles, 0 drafts, 0 pages, 0 hidden pages and 0 draft pages in 0.62 seconds.

Hmm . Two immediate errors. It turns out that the default language choice
"English" in pelican-quickstart should have been "en". I had to go to
pelicanconf.py, and change the line:

    DEFAULT_LANG = 'English'

To

    DEFAULT_LANG = 'en'

I also realised the pelican was not finding the 'title' metadata in my initial
file. After some investigation, I noticed that when I copied and pasted the
suggested initial file contents from the pelican quickstart guide into my
Markdown editor Typora, it converted it to a code block by automatically adding
triple backticks before and after the pasted text. So my Markdown file
contents in `keyboard-review.md` were actually:

    ```
    Title: My First Review
    Date: 2020-05-08 10:20
    Category: Review
    
    Following is a review of my favorite mechanical keyboard.
    ```

I had to remove the leading and trailing backtick lines and resave the markdown
file. I could then retry generating the site output:

    pelican content
    Done: Processed 1 article, 0 drafts, 0 pages, 0 hidden pages and 0 draft pages in 0.31 seconds.

This time it worked! I had an entire web site in the `output` folder. I was
expecting possibly a single HTML file, but it actually created a significant
amount of boilerplate output. I was able to view a local copy of the website
by launching the pelican built-in web server

    pelican --listen

Once this was running, I could preview the site by navigating to the URL
http://localhost:8000/ on my local browser:

![Pelican Initial Screenshot]({static}/images/2020-05-10_Pelican_Initial_Screenshot.png)

Excellent! I like how this appears, and it took maybe 20-30 minutes to get this
up and running.

## Publish to GitHub Pages ##

I was immediately sold on Pelican - I now wanted to publish this publicly to my
GitHub Pages site.

I followed the instructions in the
[Pelican docs](https://docs.getpelican.com/en/4.2.0/tips.html#project-pages)

First of all, I installed the Python `ghp-import` tool

    pip install ghp-import

I used ghp-import to create a local `gh-pages` branch with the content of the
`output` folder. If the branch already exists, this command will update the
branch with the latest files in `output`.

    ghp-import output

I then pushed the `gh-pages` branch from my local desktop to my GitHub
repository

    git push origin gh-pages

Finally, I went to my GitHub repository and in Settings, GitHub Pages, I
changed the source from the Master branch docs folder (used by Jekyll) to the
gh-pages branch.

My [site](https://simulatine.github.io/100DaysOfCode/) was now visible
at https://simulatine.github.io/100DaysOfCode/

I finally cleaned up my old Jekyll site by deleting everything in the old docs
folder with `git rm`, and resyncing my repository:

    git push origin master

## Conclusion ##

I found Pelican to be simple to use, and a lot more Pythonesque than Jekyll.
I'll be sticking with this for a while.