#!python3
# -*- coding: utf-8 -*-

import sys
import time
import pygame
from pygame.locals import *

# Set up the colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED =   (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE =  (  0,   0, 255)

# Initialise Pygame
pygame.init()

# Set up the window
DISPLAYSURF = pygame.display.set_mode((500, 400), 0, 32)

# Fill the display background in white
DISPLAYSURF.fill(WHITE)

# Load and play a sound
soundObj = pygame.mixer.Sound("matrix_music.wav")
soundObj.play()

# Wait for one second, then stop the sound playing
time.sleep(3)
soundObj.stop()

# Run the game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()