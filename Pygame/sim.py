#!python3
# -*- coding: utf-8 -*-
"""
Simulation common code.

Contains common functions that can be used across multiple Pygame simulations:

Grid class - a standard grid for cellular automata type simulations.
check_user_input() - a consistent mechanism to get user input.
start_pygame() and end_pygame() - cleanly initialise and close Pygame
config_logging() - establish a standard debugging/logging mechanism.

Simulatine, 28 May, 2020 - Initial version.
Simulatine, 29 May, 2020 - Updates:
                         - Used Pygame rect objects to reduce the number of
                           class attributes within Grid()
                         - Added clock.get_fps() to the dashboard to show the
                           actual frame rate.
                         - Moved initial drawing functions out of main game
                           loop.
                         - Create a subclass of the generic Grid() class to
                           separate out the methods specific to the Langton's
                           Ant simulation. This will allow Grid() to be reused
                           in the future.
Simulatine, 31 May, 2020 - Updates:
                         - Added a Pause button and a status message to the
                           dashboard area.
                         - Checked for ant off screen and added an appropriate
                           "Completed" message.
                         - Added an icon image for the window title bar.
Simulatine, 01 Jun, 2020 - Separated Grid class and generic variables into a
                           module sim.py for reuse with other simulations.

"""
import datetime
import logging
import os
import sys

# Import Pygame, either standard version or SDL2 version depending on the
# platform.
try:
    import pygame_sdl2  # pylint: disable=import-error

    pygame_sdl2.import_as_pygame()
    PYGAME_SDL2 = True
except ModuleNotFoundError:
    PYGAME_SDL2 = False
import pygame

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

# Define the available user actions. These are implemented via the keyboard
# and via on screen button controls.
UP = "Up"
DOWN = "Down"
LEFT = "Left"
RIGHT = "Right"
QUIT = "Quit"
PAUSE = "Pause"

# Cardinal directions in clockwise order
DIRECTIONS = [RIGHT, DOWN, LEFT, UP]

# Screen layouts
LANDSCAPE = "Landscape"
PORTRAIT = "Portrait"


class Grid:
    """Create and update the grid simulation."""

    # Stop pylint complaining about the number of attributes:
    # pylint: disable=too-many-instance-attributes

    def __init__(self, display_surface, title):
        """Initialise the grid."""
        # Main display surface
        self.win = display_surface

        # Grid position on screen
        self.grid = None

        # Dashboard position on screen
        self.dashboard = None
        self.dash_pos_x = 10
        self.dash_pos_y = 40
        self.dash_offset_x = 0
        self.dash_offset_y = 0

        self.generation = 1
        self.population = 0
        self.paused = False

        self.buttons = {}
        self.cells = []
        self.set_display_parameters()
        self.create_fonts()
        self.create_grid()
        self.create_dashboard(title)
        self.create_cells()
        self.create_buttons()
        self.create_keyboard_actions()

        # Initialise a Pygame clock timer. This helps calculate the frame rate.
        self.clock = pygame.time.Clock()

    def create_fonts(self):
        """Create Pygame font objects for use when drawing text."""
        self.font_size = 20
        self.font = pygame.font.SysFont("Courier", 20)
        self.bold_font = pygame.font.SysFont("Courier", 20, bold=True)

    def set_display_parameters(self):
        """Set the overall display parameters based on the display size."""
        # Check the actual display size
        # On a desktop running standard Pygame, the width and height used in
        # start_pygame() function will be used. On an Android device running
        # Pydroid3 and pygame_sdl2, the requested values are ignored and the
        # full device screen size is used instead, so we need to recheck
        # the actual display size here.
        self.display_width = pygame.display.Info().current_w
        self.display_height = pygame.display.Info().current_h

        self.margin_x = 10
        self.margin_y = 10
        self.cell_size = 5
        if self.display_width >= self.display_height:
            self.layout = LANDSCAPE
            # Make the main grid 70% of the window width
            self.cell_cols = int((self.display_width * 0.7) / self.cell_size)
            # Make the main grid fill the entire window height, allowing for
            # top and bottom margins
            self.cell_rows = int(
                (self.display_height - self.margin_y * 2) / self.cell_size
            )
        elif self.display_height > self.display_width:
            self.layout = PORTRAIT
            # Make the main grid fill the entire window width, allowing for
            # left and right margins
            self.cell_cols = int(
                (self.display_width - self.margin_x * 2) / self.cell_size
            )
            # Make the main grid 80% of the window height
            self.cell_rows = int((self.display_height * 0.8) / self.cell_size)

    def create_buttons(self):
        """
        Create standard control button surfaces and their locations.

        On screen buttons are required on tablet devices as keyboard control
        is not available.

        This function defines a Quit and Pause buttons. Child classes may
        want to add additional buttons.
        """
        # This size is sufficient for buttons up to 4-5 characters.
        size = (width, height) = (100, 50)

        if self.layout == LANDSCAPE:
            # Place the first button at the bottom middle of the dashboard
            x = self.dashboard.left + int(
                (self.dashboard.right - self.dashboard.left) / 2
            )
            # Place additional buttons above the first one, with a 10 pixel gap
            # between each button
            dx = 0
            dy = -(height + 10)
        else:
            # Place the first button at the bottom right of the dashboard
            x = self.dashboard.right - 10 - int(width) / 2
            # Place additional buttons to the left of the the first one, with a
            # 10 pixel gap between each button
            dx = -(width + 10)
            dy = 0

        y = self.dashboard.bottom - 10 - int(height / 2)

        # Create a Quit button
        pos = (x, y)
        self.buttons[QUIT] = self.create_button(
            QUIT, TEXTCOLOR, DARKGRAY, pos, size
        )

        # Create a Pause button
        pos = (x + dx, y + dy)
        self.buttons[PAUSE] = self.create_button(
            PAUSE, TEXTCOLOR, DARKGRAY, pos, size
        )

    def create_button(self, text, color, bgcolor, pos, size):
        """Create Surface and Rect objects for an on screen button."""
        width, height = size[0], size[1]
        # First, create the button surface
        button_surface = pygame.Surface(size)
        button_surface.fill(bgcolor)
        button_rect = button_surface.get_rect()
        button_rect.center = (int(pos[0]), int(pos[1]))

        # Draw a shadow
        shadow_color = (bgcolor.r * 1.5, bgcolor.g * 1.5, bgcolor.b * 1.5)
        pygame.draw.rect(
            button_surface, shadow_color, (0, 0, width - 4, height - 4)
        )

        # Next, create a surface with the rendered text
        text_surface = self.font.render(text, True, color)
        # Get the size of the rendered text in pixels
        text_size = self.font.size(text)
        # Determine where to place the text on the button, so that it appears
        # to be centered
        text_x = int((width - text_size[0]) / 2)
        text_y = int((height - text_size[1]) / 2)

        button_surface.blit(text_surface, (text_x, text_y))
        return (button_surface, button_rect)

    def create_cells(self):
        """Create the initial game grid."""
        # Stop pylint complaining about unused x and y variables:
        # pylint: disable=unused-variable

        for x in range(self.cell_cols):
            column = []
            for y in range(self.cell_rows):
                column.append(False)
            self.cells.append(column)

    def create_dashboard(self, title):
        """Create a dashboard to the side of, or below, the main grid."""
        if self.layout == LANDSCAPE:
            # Place the dashboard to the right of the main grid
            left = self.grid.right + self.margin_x
            width = self.display_width - self.margin_x - left
            top = self.margin_y
            height = self.grid.bottom - self.margin_y
            # Offset for each subsequent dashboard item
            self.dash_offset_x = 0
            self.dash_offset_y = 20
        else:
            # Place the dashboard below the main grid
            left = self.margin_x
            width = self.grid.right - self.margin_x
            top = self.grid.bottom + self.margin_y
            height = self.display_height - self.margin_y - top
            self.dash_offset_x = 0
            self.dash_offset_y = 20

        self.dashboard = pygame.Rect(left, top, width, height)
        # Draw a border around the entire dashboard
        pygame.draw.rect(self.win, BLUE, self.dashboard, 2)

        # Draw the simulation title at the top of the dashboard
        self.draw_text(
            title,
            TEXTCOLOR,
            BGCOLOR,
            self.dashboard.left + 5,
            self.dashboard.top + 5,
            bold=True,
        )

    def create_grid(self):
        """Draw the main grid."""
        left = self.margin_x
        width = self.cell_cols * self.cell_size
        top = self.margin_y
        height = self.cell_rows * self.cell_size

        self.grid = pygame.Rect(left, top, width, height)

        # Draw a border around the entire grid
        pygame.draw.rect(
            self.win, BLUE, (left - 1, top - 1, width + 1, height + 1), 2,
        )

        # Draw vertical lines
        for x in range(left, left + width, self.cell_size):
            pygame.draw.line(self.win, LIGHTBLUE, (x, top), (x, top + height))
        # Draw horizontal lines
        for y in range(top, top + height, self.cell_size):
            pygame.draw.line(self.win, LIGHTBLUE, (left, y), (left + width, y))

    def create_keyboard_actions(self):
        """Create a dictionary of standard keyboard actions."""
        self.keyboard_actions = {
            # Arrow keys
            pygame.K_LEFT: LEFT,
            pygame.K_RIGHT: RIGHT,
            pygame.K_UP: UP,
            pygame.K_DOWN: DOWN,
            # WASD keys
            pygame.K_a: LEFT,
            pygame.K_d: RIGHT,
            pygame.K_w: UP,
            pygame.K_s: DOWN,
            # Pause (Space or P key)
            pygame.K_SPACE: PAUSE,
            pygame.K_p: PAUSE,
            # Quit (ESC or Q key)
            pygame.K_ESCAPE: QUIT,
            pygame.K_q: QUIT,
        }

    def draw_buttons(self):
        """Draw control buttons on the screen."""
        for button in self.buttons:
            surface, rect = self.buttons[button][0], self.buttons[button][1]
            self.win.blit(surface, rect)

    def update(self):
        """Update the simulation and update the grid and dashboard."""
        if not self.paused:
            self.update_simulation()
            self.update_grid()
            self.update_dashboard()
            self.generation += 1
            # Update the Pygame clock once per game loop.
            self.clock.tick()
        else:
            # The simulation is paused. Display an appropriate message.
            self.update_dashboard("Paused")

    def draw_text(self, text, color, bgcolor, top, left, bold=False):
        """Create Surface and Rect objects for on screen text."""
        if bold:
            text_surface = self.bold_font.render(text, True, color, bgcolor)
        else:
            text_surface = self.font.render(text, True, color, bgcolor)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (top, left)
        self.win.blit(text_surface, (top, left))

    def update_simulation(self):
        """Update the simulation by one generation.

        This is the default class method and just refreshes the generation
        count. A more detailed update method should be created in each child
        function.
        """
        self.generation += 1

    def update_grid(self):
        """Draw the current state of the main grid."""
        for x in range(self.cell_cols):
            for y in range(self.cell_rows):
                # Make the cell_rect one pixel smaller than the actual grid
                # size in all directions, to prevent drawing over the grid
                # lines.
                cell_x = self.margin_x + x * self.cell_size + 1
                cell_y = self.margin_y + y * self.cell_size + 1
                cell_rect = pygame.Rect(
                    cell_x, cell_y, self.cell_size - 1, self.cell_size - 1
                )
                if self.cells[x][y]:
                    # Cell is On (True).
                    # Fill the cell.
                    pygame.draw.rect(self.win, WHITE, cell_rect)
                else:
                    # Cell is Off (False).
                    # Leave the cell unfilled.
                    pygame.draw.rect(self.win, BGCOLOR, cell_rect)

    def update_dashboard(self, msg=None):
        """Update the dashboard display.

        This is the default class method: it displays any passed status
        message, as well as the generation count, population and refresh rate.
        A more specific dashboard method should be created for each child
        class, displaying updates specific to that simulation.
        """
        x = 10
        y = 40

        if msg:
            # Display any status message
            self.draw_text(
                msg,
                TEXTCOLOR,
                BGCOLOR,
                self.dashboard.left + x,
                self.dashboard.top + y,
                bold=True,
            )
        else:
            # Clear the status message area
            self.draw_text(
                "        ",
                TEXTCOLOR,
                BGCOLOR,
                self.dashboard.left + x,
                self.dashboard.top + y,
                bold=True,
            )

        # Display the current generation number
        self.draw_text(
            "Gen:   {:>5}".format(self.generation),
            TEXTCOLOR,
            BGCOLOR,
            self.dashboard.left + x + self.dash_offset_x,
            self.dashboard.top + y + self.dash_offset_y,
        )
        # Display the current population
        self.draw_text(
            "Pop:   {:>5}".format(self.population),
            TEXTCOLOR,
            BGCOLOR,
            self.dashboard.left + x + self.dash_offset_x * 2,
            self.dashboard.top + y + self.dash_offset_y * 2,
        )
        # Display the current simulation update rate in frames per second
        self.draw_text(
            "FPS:   {:>5}".format(int(self.clock.get_fps())),
            TEXTCOLOR,
            BGCOLOR,
            self.dashboard.left + x + self.dash_offset_x * 3,
            self.dashboard.top + y + self.dash_offset_y * 3,
        )
        # Set the position on the dashboard for any subsequent messages.
        # This can be used by any further dashboard updates in a
        # child class.
        self.dash_pos_x = x + self.dash_offset_x * 4
        self.dash_pos_y = y + self.dash_offset_y * 4


def check_user_input(buttons, keyboard_actions):
    """Check for any user input and return the requested action."""
    # Tell pylint to ignore no-member errors.
    # These occur as pylint cannot find the various pygame event types used
    # below.
    # pylint: disable=no-member
    action = None
    for event in pygame.event.get():  # event handling loop
        if event.type == pygame.MOUSEBUTTONUP:
            action = check_button_press(event.pos, buttons)
        elif event.type == pygame.KEYDOWN:
            action = check_keyboard_press(event.key, keyboard_actions)
    return action


def check_button_press(mouse_position, buttons):
    """Check if the user pressed an on screen button."""
    # The user clicked the mouse (or touched the screen).
    # Check if they clicked an onscreen button and return the
    # appropriate action.
    action = None
    for button in buttons:
        if buttons[button][1].collidepoint(mouse_position):
            logging.debug("Player clicked on button %s", button)
            # Take the appropriate action depending on which button
            # was clicked.
            action = button
    return action


def check_keyboard_press(key, keyboard_actions):
    """Check if the user pressed a key with a define action."""
    # The user clicked a key. Check which key was pressed and assign
    # the appropriate action.
    try:
        action = keyboard_actions[key]
    except KeyError:
        # Ignore key presses for which no action has been defined
        action = None
    return action


def start_pygame(width, height, title):
    """Start Pygame and create the Pygame window."""
    # Initialise the Pygame display window
    pygame.init()

    # Set the window title. This has no effect on Android.
    pygame.display.set_caption(title)

    # Set the window icon
    icon = pygame.image.load("langton_icon.png")
    pygame.display.set_icon(icon)

    # Create the Pygame window with the requested width and height.
    # Note that on Android devices running Pydroid3 and pygame_sdl2, the
    # requested values are ignored and the full device screen size is used.
    # We will later need to check the actual display size.
    window = pygame.display.set_mode((width, height))
    return window


def end_pygame():
    """Close the Pygame window and exit the program."""
    pygame.quit()
    print("Thanks for playing!")
    logging.debug("Exiting program")
    sys.exit()


def config_logging(title):
    """Configure the logging system."""
    # Logging levels are: DEBUG, INFO, WARNING, ERROR, CRITICAL
    # Use logging.debug(...) for general debugging.
    # Use logging.info(...) to focus debugging on a specific area of code.
    # Set the logging level to DEBUG to catch all messages.
    log_file_msg_level = logging.DEBUG

    # Build the log file name, including the game title and the current time.
    cur_date = datetime.datetime.now().strftime("%Y_%m_%d")
    logfile = os.path.expanduser(title + "_log_{}.txt".format(cur_date))

    # Define a log handler to writes messages to a log file.
    logging.basicConfig(
        filename=logfile,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(asctime)s:%(levelname)s:%(funcName)s():" " %(message)s",
        level=log_file_msg_level,
    )

    # Write some initial log messages
    logging.debug("")
    logging.debug("")
    logging.debug("Python %s", sys.version)
    logging.debug("Platform %s", sys.platform)
    logging.debug("Starting %s", title)


def main():
    """Initialise the game and call the main game loop."""
    title = "Simulation"
    # Initialise logging
    config_logging(title)

    # Intialise Pygame with a standard desktop window size
    display_surface = start_pygame(640, 480, title)

    # Run the simulation for one second.
    # Note that the default Grid class does nothing.
    simulation = Grid(display_surface, title)
    simulation.draw_buttons()
    pygame.display.update()

    # Wait for one second
    pygame.time.wait(1000)
    end_pygame()


if __name__ == "__main__":
    main()
