#!python3
# -*- coding: utf-8 -*-
"""
A simple Pygame example.
Draws a red rectangle which moves horizontally back and forth across the
screen.

Simulatine, 5 May, 2020 - Original version
Simulatine, 7 May, 2020 - Added to my #100DaysOfCode repository
"""

# Load Pygame for both my Windows desktop and my Android tablet.
try:
    import pygame_sdl2
    pygame_sdl2.import_as_pygame()
except:
    pass

import pygame
pygame.init()

# Changed on tablet
screen_width, screen_height = 500, 600
size = (screen_width, screen_height)
screen = pygame.display.set_mode(size)

x, y = screen_width / 2, screen_height / 2

height = 40
width = 60
run = True

velocity = 10
clock = pygame.time.Clock()
# direction = [1, 1]
direction = 'Right'

def animate(x, y, height, width, direction):
    if x < 0:
        direction = 'Right'

    elif x > 500:
        direction = 'Left'

    if direction == 'Right':
        x += velocity

    elif direction == 'Left':
        x -= velocity

    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(x, y, width, height))

    return x, direction

while run:
    for event in pygame.event.get():
        # End the loop if a mouse button is pressed
        # (or the screen is tapped)
        if event.type == pygame.MOUSEBUTTONDOWN:
            run = False
    keys = pygame.key.get_pressed()

    screen.fill((0, 0, 0))


    x, direction = animate(x, y, height, width, direction)
    pygame.display.flip()
    clock.tick()
