Title: Day 8: Using Notepad++ with Markdown
Date: 2020-05-14
Category: Posts


## Notepad++ and Markdown ##

For years, I have used [Notepad++](https://notepad-plus-plus.org) as my primary
Windows text editor. It is well suported, and provides good syntax highlighting
for Python and many other languages. 

Notepad++ includes several different themes, each of which changes the editor
background color and fonts. I prefer a dark style, and use the *Deep black*
theme, which works well with plain text and most programming languages, such as
Python:

![image]({static}/images/2020-05-14_NotepadPlusPlus_Python_with_Deep_black_Theme.png)

However, I had a major issue with displaying and editing Markdown documents.
The default syntax highlighting for Markdown documents is designed for light
background themes:

![image]({static}/images/2020-05-14_NotepadPlusPlus_Markdown_with_Light_Theme.png)

But with a dark theme such as *Deep black*, it looks terrible and is impossible
to edit:

![image]({static}/images/2020-05-14_NotepadPlusPlus_Markdown_with_Dark_Theme.png)


## Solution ##

After some research, I found the
[Edditoria Github repository](https://github.com/Edditoria/markdown-plus-plus),
which contained updated dark syntax highlighting themes for Notepad++,
specifically designed for editing Markdown documents.

To install these, I downloaded the latest
[zip file](https://github.com/Edditoria/markdown-plus-plus/archive/v3.1.0.zip),
and extracted the contents. The `udl` folder in the zip file contained a number
of XML files which had markdown syntax highlighting for each Notepad++ colour
theme:

    markdown.bespin.udl.xml
    markdown.blackboard.udl.xml
    markdown.deep-black.udl.xml
    markdown.default.udl.xml
    markdown.obsidian.udl.xml
    markdown.solarized-light.udl.xml
    markdown.solarized.udl.xml
    markdown.zenburn.udl.xml

I copied the XML files to the `%AppData%\Notepad++\userDefineLangs` folder,
overwriting any existing XML files.

I then restarted Notepad++ and open the source file for this page. From the
**Language** menu, I selected **Markdown (Deep Black)** and saw a properly
formatted Markdown document:

![image]({static}/images/2020-05-14_NotepadPlusPlus_Markdown_with_Edditoria_ULDs.png)


## Conclusion ##
This took me a couple of days to resolve, but the results are worth it. For a
while I was limited to editing .MD Markdown documents in plain old Notepad,
which was a real throwback. Now I can edit them directly in Notepad++.