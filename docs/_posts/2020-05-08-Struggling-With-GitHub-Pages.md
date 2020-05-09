---
layout: post
title:  "Images on GitHub Pages"
---

I spent my time today learning about GitHub Pages, and trying to get an image to display in my blog post.

I create a folder `assets` on my local drive, and added a .png image file. After committing this change, and syncing with GitHub, I confirmed that the folder and file were present in my repository. So far, so good.

But the post markdown wasn't displaying properly. In the post markdown, I originally tried

​	![Image alt text](/assets/image1.png)

This displayed

![Image alt text](/assets/image1.png)

This didn't work - it seems that the root `/assets` directory that GitHub sees is not the same as the one I created. After some investigation, and searching on StackExchange, I eventually realised I didn't need the initial "/" on my path to the image.

​	![Image alt text](assets/image1.png)

This worked:

![Image alt text](assets/image1.png)


