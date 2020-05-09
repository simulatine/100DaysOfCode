---
layout: post
title:  "Images on GitHub Pages"
---

I spent my time today learning about GitHub Pages, and trying to get an image to display in my blog post.

My GitHub Pages web site is contained in the `docs` folder in my repository. I create a subfolder `doc/assets` on my local drive, and added a .png image file. After committing this change, and syncing with GitHub, I confirmed that the folder and file were present in my repository. So far, so good.

But the post markdown wasn't displaying properly. In the post markdown, I originally tried

```
![Screenshot](/docs/assets/image1.png "Screenshot")

```
which displayed

![Screenshot](/docs/assets/image1.png "Screenshot")

This didn't work - it seems that the root `/assets` directory that GitHub sees is not the same as the one I created. After some investigation, and searching on StackExchange, I eventually realised that a relative path will work. As my posts are in the _posts folder, I can do the following.

```
![Screenshot](../assets/image1.png "Screenshot")
```

and get

![Screenshot](../assets/image1.png "Screenshot")


