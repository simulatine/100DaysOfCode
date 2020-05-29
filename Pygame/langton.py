#!python3
# -*- coding: utf-8 -*-
"""
Langton's Ant - simulation of
                https://en.wikipedia.org/wiki/Langton%27s_ant

Simulatine, 28 May, 2020 - Initial version.
"""

import datetime
import logging
import os
import sys

# Import Pygame, either standard version or SDL2 version depending on the
# platform.
try:
    import pygame_sdl2 # pylint: disable=import-error

    pygame_sdl2.import_as_pygame()
    PYGAME_SDL2 = True
except ModuleNotFoundError:
    PYGAME_SDL2 = False
import pygame

# Create the core Pygame objects
WIN = None
FPSCLOCK = None
GAME_TITLE = "Langton's Ant"
FONT = None

# Game variables
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FONT_SIZE = 20

# Define some colors to use in the game
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
CYAN = pygame.Color(0, 64, 64)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
LIGHTBLUE = pygame.Color(0, 0, 196)
DARKGREEN = pygame.Color(0, 155, 0)
DARKGRAY = pygame.Color(40, 40, 40)
LIGHTGRAY = pygame.Color(196, 196, 196)
BGCOLOR = BLACK
TEXTCOLOR = WHITE


# Define the available user actions
UP = "Up"
DOWN = "Down"
LEFT = "Left"
RIGHT = "Right"
QUIT = "Quit"

# Cardinal directions in clockwise order
DIRECTIONS = [RIGHT, DOWN, LEFT, UP]

# Screen layouts
LANDSCAPE = "Landscape"
PORTRAIT = "Portrait"


class Grid:
    """Create and update the grid simulation."""

    # Stop pylint complaining about the number of attributes:
    # pylint: disable=too-many-instance-attributes

    def __init__(self):
        """Initialise the grid."""

        # Grid position
        self.grid_left = 0
        self.grid_right = 0
        self.grid_top = 0
        self.grid_bottom = 0

        # Dashboard position
        self.dashboard_left = 0
        self.dashboard_right = 0
        self.dashboard_top = 0
        self.dashboard_bottom = 0

        # Game parameters
        self.generation = 1
        self.ant_x = 0
        self.ant_y = 0
        self.ant_init_x = self.ant_x
        self.ant_init_y = self.ant_y
        self.ant_direction = LEFT

        self.buttons = {}
        self.cells = []
        self.set_display_parameters()
        self.set_game_parameters()
        self.create_grid()

    def set_display_parameters(self):
        """Set the overall display parameters based on the window size."""
        self.window_width = WINDOW_WIDTH
        self.window_height = WINDOW_HEIGHT
        if (self.window_width, self.window_height) == (640, 480):
            # Landscape layout
            self.layout = LANDSCAPE
            self.cell_size = 10
            self.grid_width = 48
            self.grid_height = 42
            self.margin_x = 10
            self.margin_y = 40
            self.frames_per_second = 15
        if (self.window_width, self.window_height) == (1000, 800):
            # Landscape layout
            self.layout = LANDSCAPE
            self.cell_size = 10
            self.grid_width = 80
            self.grid_height = 75
            self.margin_x = 10
            self.margin_y = 40
            self.frames_per_second = 15
        elif (self.window_width, self.window_height) == (600, 960):
            # Portrait layout - for use on Android tablet
            self.layout = PORTRAIT
            self.cell_size = 10
            self.grid_width = 56
            self.grid_height = 72
            self.margin_x = 10
            self.margin_y = 40
            self.frames_per_second = 15

    def set_game_parameters(self):
        """Set the initial game parameters."""
        self.generation = 1
        self.ant_x = int(self.grid_width / 2)
        self.ant_y = int(self.grid_height / 2)
        self.ant_init_x = self.ant_x
        self.ant_init_y = self.ant_y
        self.ant_direction = LEFT

    def create_grid(self):
        """Create the initial game grid."""
        # Stop pylint complaining about unused x and y variables:
        # pylint: disable=unused-variable

        for x in range(self.grid_width):
            column = []
            for y in range(self.grid_height):
                column.append(False)
            self.cells.append(column)

    def update(self):
        """Update the simulation by one generation."""
        self.move_ant()
        self.update_grid()
        self.draw_ant()
        self.update_dashboard()
        self.generation += 1

    def move_ant(self):
        """Update the ant's position."""
        if self.ant_direction == LEFT:
            self.ant_x -= 1
        elif self.ant_direction == RIGHT:
            self.ant_x += 1
        elif self.ant_direction == UP:
            self.ant_y -= 1
        elif self.ant_direction == DOWN:
            self.ant_y += 1

        # Check the color of the new cell:
        if self.cells[self.ant_x][self.ant_y]:
            # Cell is On (True).
            # Turn counter-clockwise
            index = DIRECTIONS.index(self.ant_direction)
            index = (index - 1) % len(DIRECTIONS)
            self.ant_direction = DIRECTIONS[index]
        else:
            # Cell is Off (False).
            # Turn clockwise
            index = DIRECTIONS.index(self.ant_direction)
            index = (index + 1) % len(DIRECTIONS)
            self.ant_direction = DIRECTIONS[index]

        # Flip the value of the current cell
        cell_value = self.cells[self.ant_x][self.ant_y]
        self.cells[self.ant_x][self.ant_y] = not cell_value

    def update_grid(self):
        """Update the main grid."""
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if self.cells[x][y]:
                    # Cell is On (True).
                    # Fill the cell.
                    cell_x = self.margin_x + x * self.cell_size
                    cell_y = self.margin_y + y * self.cell_size
                    cell_rect = pygame.Rect(
                        cell_x, cell_y, self.cell_size, self.cell_size
                    )
                    pygame.draw.rect(WIN, WHITE, cell_rect)
                else:
                    # Cell is Off (False).
                    # Leave the cell unfilled.
                    pass

    def draw_ant(self):
        """Draw the ant on the main grid."""
        cell_x = self.margin_x + self.ant_x * self.cell_size
        cell_y = self.margin_y + self.ant_y * self.cell_size
        cell_rect = pygame.Rect(cell_x, cell_y, self.cell_size, self.cell_size)
        pygame.draw.rect(WIN, RED, cell_rect)

    def update_dashboard(self):
        """Update the dashboard display."""
        if self.layout == LANDSCAPE:
            dx = 0
            dy = 20
        else:
            dx = 0
            dy = 20

        x = 10
        y = 10
        draw_text(
            "Gen:   {}".format(self.generation),
            TEXTCOLOR,
            self.dashboard_left + x,
            self.dashboard_top + y,
        )
        draw_text(
            "Ant X: {}".format(self.ant_x - self.ant_init_x),
            TEXTCOLOR,
            self.dashboard_left + x + dx,
            self.dashboard_top + y + dy,
        )
        draw_text(
            "Ant Y: {}".format(self.ant_y - self.ant_init_y),
            TEXTCOLOR,
            self.dashboard_left + x + dx * 2,
            self.dashboard_top + y + dy * 2,
        )

    def draw_title(self):
        """Draw the game title at the top of the screen."""
        text_surface = FONT.render(GAME_TITLE, True, TEXTCOLOR)
        WIN.blit(text_surface, (self.margin_x, 5))

    def draw_grid_lines(self):
        """Draw the main grid."""
        left = self.margin_x
        right = self.margin_x + self.grid_width * self.cell_size
        top = self.margin_y
        bottom = self.margin_y + self.grid_height * self.cell_size

        # Draw vertical lines
        for x in range(left, right, self.cell_size):
            pygame.draw.line(WIN, LIGHTBLUE, (x, top), (x, bottom))
        # Draw horizontal lines
        for y in range(top, bottom, self.cell_size):
            pygame.draw.line(WIN, LIGHTBLUE, (left, y), (right, y))

        # Draw a border around the entire grid
        pygame.draw.rect(
            WIN,
            BLUE,
            (left - 1, top - 1, right - left + 1, bottom - top + 1),
            2,
        )

        # Save the grid position
        self.grid_left = left
        self.grid_right = right
        self.grid_top = top
        self.grid_bottom = bottom

    def draw_dashboard(self):
        """Draw a dashboard to the side of, or below, the main grid."""

        if self.layout == LANDSCAPE:
            # Place the dashboard to the right of the main grid
            left = self.grid_right + self.margin_x
            top = self.margin_y
            right = self.window_width - self.margin_x
            bottom = self.grid_bottom
        else:
            # Place the dashboard below the main grid
            left = self.margin_x
            top = self.grid_bottom + self.margin_y
            right = self.grid_right
            bottom = self.window_height - self.margin_y

        # Draw a border around the entire dashboard
        pygame.draw.rect(WIN, BLUE, (left, top, right - left, bottom - top), 2)

        # Save the dashboard position
        self.dashboard_left = left
        self.dashboard_right = right
        self.dashboard_top = top
        self.dashboard_bottom = bottom

    def create_buttons(self):
        """Create control button surfaces and their locations."""
        size = (width, height) = (100, 50)

        if self.layout == LANDSCAPE:
            # Place the button at the bottom middle of the dashboard
            x = self.dashboard_left + int(
                (self.dashboard_right - self.dashboard_left) / 2
            )
        else:
            # Place the button at the bottom right of the dashboard
            x = self.dashboard_right - 10 - int(width) / 2
        y = self.dashboard_bottom - 10 - int(height / 2)

        pos = (x, y)
        surface, rect = create_button(QUIT, TEXTCOLOR, DARKGRAY, pos, size)
        self.buttons[QUIT] = [surface, rect]

    def draw_buttons(self):
        """Draw control buttons on the screen."""
        for button in self.buttons:
            surface, rect = self.buttons[button][0], self.buttons[button][1]
            WIN.blit(surface, rect)


def main():
    """Initialise the game and execute the main game loop."""
    global WINDOW_WIDTH, WINDOW_HEIGHT
    global FONT
    # Initialise logging
    config_logging()

    # WINDOW_WIDTH, WINDOW_HEIGHT = start_pygame(640, 480, GAME_TITLE)
    WINDOW_WIDTH, WINDOW_HEIGHT = start_pygame(1000, 800, GAME_TITLE)
    # WINDOW_WIDTH, WINDOW_HEIGHT = start_pygame(600, 960, GAME_TITLE)
    FONT = pygame.font.Font("freesansbold.ttf", FONT_SIZE)

    run_game()
    end_pygame()


def run_game():
    """Main game loop."""
    simulation = Grid()
    while True:
        WIN.fill(BGCOLOR)
        simulation.draw_title()
        simulation.draw_grid_lines()
        simulation.draw_dashboard()
        simulation.create_buttons()
        simulation.draw_buttons()
        # Handle events
        action = check_user_input(simulation.buttons)
        if action:
            # Process the requested action
            print("The player requested action: {}".format(action))
            if action == QUIT:
                end_pygame()
            else:
                pass

        # Update the game position
        simulation.update()
        # Update the display
        pygame.display.update()
        # Pause the game to meet the appropriate frame rate
        # FPSCLOCK.tick(simulation.frames_per_second)


def check_user_input(buttons):
    """Check for any user input and return the requested action."""
    action = None
    for event in pygame.event.get():  # event handling loop
        if event.type == pygame.QUIT:
            end_pygame()
            action = QUIT
        elif event.type == pygame.MOUSEBUTTONUP:
            # The user clicked the mouse (or touched the screen).
            # Check if they clicked an onscreen button and return the
            # appropriate action.
            for button in buttons:
                if buttons[button][1].collidepoint(event.pos):
                    logging.debug("Player clicked on button %s", button)
                    # Take the appropriate action depending on which button
                    # was clicked.
                    action = button
        elif event.type == pygame.KEYDOWN:
            # The user clicked a key. Check which key was pressed and return
            # the appropriate action.
            if event.key in (pygame.K_LEFT, pygame.K_a):
                action = LEFT
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                action = RIGHT
            elif event.key in (pygame.K_UP, pygame.K_w):
                action = UP
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                action = DOWN
            elif event.key in (pygame.K_ESCAPE, pygame.K_q):
                action = QUIT
    return action


def create_button(text, color, bgcolor, pos, size):
    """Create Surface and Rect objects for an on screen button."""

    x, y = pos[0], pos[1]
    width, height = size[0], size[1]
    # First, create the button surface
    button_surface = pygame.Surface(size)
    button_surface.fill(bgcolor)
    button_rect = button_surface.get_rect()
    button_rect.center = (int(x), int(y))

    # Draw a shadow
    shadow_color = (bgcolor.r * 1.5, bgcolor.g * 1.5, bgcolor.b * 1.5)
    pygame.draw.rect(
        button_surface, shadow_color, (0, 0, width - 4, height - 4)
    )

    # Next, create a surface with the rendered text
    text_surface = FONT.render(text, True, color)
    # Get the size of the rendered text in pixels
    text_size = FONT.size(text)
    # Determine where to place the text on the button, so that it appears to
    # be centered
    text_x = int((width - text_size[0]) / 2)
    text_y = int((height - text_size[1]) / 2)

    button_surface.blit(text_surface, (text_x, text_y))
    return (button_surface, button_rect)


def draw_text(text, color, top, left):
    """Create Surface and Rect objects for on screen text."""
    text_surface = FONT.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (top, left)
    WIN.blit(text_surface, (top, left))


def start_pygame(width, height, title):
    """Start Pygame and create the Pygame window."""
    global WIN, FPSCLOCK

    # Initialise the Pygame display window.
    pygame.init()
    FPSCLOCK = pygame.time.Clock()

    # Set the window title. This has no effect on Android.
    pygame.display.set_caption(title)

    # Create the Pygame window. On a desktop running standard Pygame, the
    # requested width and height will be used. On an Android device running
    # Pydroid3 and pygame_sdl2, the requested values are ignored and the full
    # device screen size is used instead, so we will need to recheck the actual
    # window size after it is created.
    WIN = pygame.display.set_mode((width, height))

    # Check the actual window size
    width = pygame.display.Info().current_w
    height = pygame.display.Info().current_h
    return (width, height)


def end_pygame():
    """Close the Pygame window and exit the program."""
    pygame.quit()
    print("Thanks for playing!")
    logging.debug("Exiting program")
    sys.exit()


def config_logging():
    """Configure the logging system."""
    # Logging levels are: DEBUG, INFO, WARNING, ERROR, CRITICAL
    # Use logging.debug(...) for general debugging.
    # Use logging.info(...) to focus debugging on a specific area of code.
    # Set the logging level to DEBUG to catch all messages.
    log_file_msg_level = logging.DEBUG

    # Build the log file name, including the game title and the current time.
    cur_date = datetime.datetime.now().strftime("%Y_%m_%d")
    logfile = os.path.expanduser(GAME_TITLE + "_log_{}.txt".format(cur_date))

    # Define a log handler to writes messages to a log file.
    logging.basicConfig(
        filename=logfile,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(asctime)s:%(levelname)s:%(funcName)s():" " %(message)s",
        level=log_file_msg_level,
    )

    # Write some initial log messages
    logging.debug("")
    logging.debug("Starting %s", GAME_TITLE)


if __name__ == "__main__":
    main()
