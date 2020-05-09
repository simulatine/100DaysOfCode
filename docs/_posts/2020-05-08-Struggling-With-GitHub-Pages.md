---
layout: post
title:  "Images in GitHub Blog Pages"
---

I spent my time today learning about GitHub Pages, and trying to get an image to display in my blog post.

My GitHub Pages web site is contained in the `docs` folder in my repository. I create a subfolder `doc/assets` on my local drive, and added a .png image file. After committing this change, and syncing with GitHub, I confirmed that the folder and file were present in my repository. So far, so good.

I was able to display this easily enough from a [standard page](https://simulatine.github.io/100DaysOfCode/showimage.html "Show Image") in the root of my website with a Markdown image link::

```
![Python code screenshot](assets/image1.png "Python code screenshot")
```

But the same link wasn't displaying properly in my blog post:

![Python code screenshot](assets/image1.png "Python code screenshot")

OK, so blog post files are in a different folder `_posts`.  Maybe I need to use a rooted path:

```
![Python code screenshot](/assets/image1.png "Python code screenshot")

```

which displayed

![Python code screenshot](/assets/image1.png "Python code screenshot")

This didn't work - it seems that the root `/assets` directory that GitHub sees is not the same as the one I created. Neither did assuming the website root was one level up, at the root of the entire repository
```
![Python code screenshot](/docs/assets/image1.png "Python code screenshot")

```

After some investigation, I paid attention to the blog post URL in my brower's address bar, and realised my post is buried three levels down:

```
https://simulatine.github.io/100DaysOfCode/2020/05/08/Struggling-With-GitHub-Pages.html
```

Aha! Maybe a relative path would work.:

```
![Python code screenshot](../../../assets/image1.png "Python code screenshot")
```

This gives me

![Python code screenshot](../../../assets/image1.png "Python code screenshot")


