Title: Day 5: Configuring Pelican
Date: 2020-05-11
Category: Posts


## Working with Pelican ##

Yesterday, I moved from the default Jekyll site generator tool provided by
GitHub Pages to the Python based
[Pelican](https://docs.getpelican.com/en/stable/) tool. I was able to quickly
create a blog based site with simple configuration, test it on my Windows
laptop and push the result to GitHub.

Today, I worked through the Pelican documentation ad added some further
site configuration. Nearly all the changes below were to the `pelicanconf.py`
configuration file in the Pelican root folder.


## Adding Footer Links ##

The default template used by Pelican displays some standard links at the bottom
of each page. I changed this to be a list of sites relevant to my site's theme
using the `LINKS` parameter in the pelicanconf.py configuration file:

    LINKS = (('Python', 'https://python.org/'),
             ('Pygame', 'https://www.pygame.org/docs/'),
             ('100DaysOfCode', 'https://www.100daysofcode.com/'),)

I also added a short list of my social website links via the `SOCIAL` option:

    SOCIAL = (('Twitter', 'https://twitter.com/simulatine'),
              ('GitHub', 'https://github.com/simulatine/100DaysOfCode'),)


## Adding Images ##

To show images in my website, I need to add a subfolder in my content folder to
contain the images:

    C:\> mkdir C:\Users\Simulatine\Documents\Scripts\Git\100DaysOfCode\web\content\images

I also need to include this folder in the `STATIC_PATHS` parameter

    STATIC_PATHS = ['images']

I could then copy pictures and screenshots to the `images` folder and run 
`pelican content` to copy these into the output folder.

I can then link to these in my Markdown source using the standard Markdown link
convention:

    ![Image Name]({static}/path/to/image.png)

**Note**: the *{static}* tag is required before the link to the image file - 
this is non-standard Markdown and caught me out for some time before I got used
to it. The is explained in more detail at:

https://docs.getpelican.com/en/4.2.0/content.html#linking-to-static-files


## Favicon ##

Adding a Favicon, which appears in the browser tab, was simple. I created an
`extras` subfolder in my content folder, and copied the favicon.ico file to
that folder.

    C:\> mkdir C:\Users\Simulatine\Documents\Scripts\Git\100DaysOfCode\web\content\extras

I made sure that the new extras folder was in my STATIC_PATHS parameter in `pelicanconf.py`

    STATIC_PATHS = ['images', 'extras']

I also included the following in pelicanconf.py, to ensure that the ICO file
was copied properly to the root of the output folder.

    EXTRA_PATH_METADATA = {
        'extras/favicon.ico': {'path': 'favicon.ico'},
    }

**Note:** This only worked for ICO files. I originally tried with a PNG image
file called favicon.png. PNG files are a valid W3C format for Favicons, but it
seems that Pelican doesn't know that. The PNG file was copied to the output
folder when I ran `pelican content`, but the Pelican web server didn't look for
it.

**Another Note:** I had to force my browser to refresh its cache before I could
see the new favicon. In Chrome, I pressed Ctrl+F5 and then closed and reopened
the browser. 


## Fixing Incorrect Markdown Syntax Highlighting ##

I initially had some problems with Pelican adding red boxes around some code
blocks in my output, and in general incorrectly applying syntax highlighting.
This mainly happened when I included Windows command prompt output text:

![image]({static}/images/2020-05-11_Incorrect_Markdown_Syntax_Highlighting.png)

I found that this was a
[known issue](https://github.com/getpelican/pelican/issues/1170) and that I
needed to change another paramter in `pelicanconf.py`. The issue log mentions
`MD_EXTENSIONS`, but that appears to be out of date. In the current 4.2.0
version of Pelican the parameter I needed to change was `MARKDOWN`,
setting `guess_lang` to `False`.

    MARKDOWN = {
        'extension_configs': {
            'markdown.extensions.codehilite': {'css_class': 'highlight', 'guess_lang':False,},
            'markdown.extensions.extra': {},
            'markdown.extensions.meta': {},
        },
        'output_format': 'html5',
    }

This solved the problem:

![image]({static}/images/2020-05-11_Correct_Markdown_Syntax_Highlighting.png)



## Batching Updates and Publishing ##

I found it useful to create a short three line Windows batch file `update.cmd`
to update the website output, refresh the repository branch with the latest
contents, and publish it to GitHub:

    pelican content
    ghp-import output
    git push origin gh-pages


Running this from my Pelican root folder is all I need to do after making any
content changes to completely refresh and publish the site.


## Conclusion ##

After only two days, I have found Pelican a joy to work with. It is
straightforward, well documented and above all simple. It works well with
GitHub Pages, and integrates well with my personal Pythan based coding
practices.