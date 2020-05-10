---
layout: post
title:  "Python on my Android Tablet"
---

## Mobile Python Graphics ##

One of my goals is to be able to code on the go ... once lockdown ends

For many years I had [Pythonista](http://omz-software.com/pythonista/) on my iPhone. This is a full implementation of Python, and is a very powerful tool, but its graphics capabilities are limited to customized [Scene](http://omz-software.com/pythonista/docs/ios/scene.html) and [UI](http://omz-software.com/pythonista/docs/ios/ui.html) modules. It doesn't support any desktop graphics library, which meant that any graphical programs I developed on my desktop simply would not run on the iPhone.

I recently discovered that the Tkinter and Pygame run on Android devices, with [Pydroid3](https://play.google.com/store/apps/details?id=ru.iiec.pydroid3&hl=en_GB). This has [Pygame_SDL2](https://pygame-sdl2.readthedocs.io/en/latest/) built-in - a version of Pygame that is almost entirely compatible with the standard desktop version of Pygame.

I didn't own any Android devices, so decided to invest as cheaply as possible.  I wanted something

- Cheap. I didn't want to invest a huge amount.
- Small. My goal is to program on the go, on a train or bus. I'd ideally like a smartphone sized or small tablet, with a screen in the 5 to 7 inch range.

My choice quickly narrowed to 7 inch tablets, and after looking at the Lenovo Tab E7 and the Dragon Touch Y88X Pro, I settled on the Vankyo MatrixPad S7. This has 2GB of RAM and 32GB of storage, not much compared to my iPhone, but enough to experiment with. Most importantly, it was a mere £64.99, an absolute bargain.

![Vankyo S7 Tablet](../../../assets/Vankyo_S7_Tablet.jpg)

## Installing Python on an Android Device ##

Installing Python was easy - I was up and running within 10 minutes.

### Installing Pydroid3

- I opened the Play Store app and searched for "pydroid"
- Once I found the correct app, I tapped on Install

![Pydroid3 in the Google Play Store](../../../assets/Pydroid3_Install_Step_1.png)

- The app downloaded and installed
- When I first opened it, I was asked if I wanted to also install an IDE for Java. I tapped on Not Interested
- The app then downloaded the latest version of Python before starting
- The app finally opened with a blank file

![Pydroid3 Initial Screen](../../../assets/Pydroid3_Install_Step_2.png)

### Configuring the App's Appearance

After starting Pydroid, I immediately changed the editor appearance to the dark theme:

- I tapped on the menu button in the top left and scroll down to Settings
- I then tapped on Appearance and changed the Editor Theme to Dark

![Pydroid3 with Dark Theme](../../../assets/Pydroid3_Install_Step_3.png)


## Pygame ##

Pydroid3 has some built in Pygame examples. Simply tap on the menu button in the top left, tap on Samples and open the Pygame folder. There are also several Kivy, Tkinter and PyQt5 examples as well.

*The fun starts now!*


![Pygame Sample Program](../../../assets/Pydroid3_Install_Step_4.png)
