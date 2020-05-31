#!python3
# -*- coding: utf-8 -*-
"""
Langton's Ant Simulation.

See https://en.wikipedia.org/wiki/Langton%27s_ant

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

# Create the core Pygame objects
WIN = None
CLOCK = None
GAME_TITLE = "Langton's Ant"
FONT = None
BOLD_FONT = None

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

    def __init__(self):
        """Initialise the grid."""
        # Grid position on screen
        self.grid = None

        # Dashboard position on screen
        self.dashboard = None

        self.generation = 1
        self.paused = False

        self.buttons = {}
        self.cells = []
        self.set_display_parameters()
        self.create_grid()
        self.create_dashboard()
        self.create_cells()
        self.create_buttons()
        # self.draw_title()

    def set_display_parameters(self):
        """Set the overall display parameters based on the window size."""
        self.window_width = WINDOW_WIDTH
        self.window_height = WINDOW_HEIGHT
        self.margin_x = 10
        self.margin_y = 10
        self.cell_size = 5
        if self.window_width >= self.window_height:
            self.layout = LANDSCAPE
            # Make the main grid 70% of the window width
            self.cell_cols = int((self.window_width * 0.7) / self.cell_size)
            # Make the main grid fill the entire window height, allowing for
            # top and bottom margins
            self.cell_rows = int(
                (self.window_height - self.margin_y * 2) / self.cell_size
            )
        elif self.window_height > self.window_width:
            self.layout = PORTRAIT
            # Make the main grid fill the entire window width, allowing for
            # left and right margins
            self.cell_cols = int(
                (self.window_width - self.margin_x * 2) / self.cell_size
            )
            # Make the main grid 80% of the window height
            self.cell_rows = int((self.window_height * 0.8) / self.cell_size)

    def create_grid(self):
        """Draw the main grid."""
        left = self.margin_x
        width = self.cell_cols * self.cell_size
        top = self.margin_y
        height = self.cell_rows * self.cell_size

        self.grid = pygame.Rect(left, top, width, height)

        # Draw a border around the entire grid
        pygame.draw.rect(
            WIN, BLUE, (left - 1, top - 1, width + 1, height + 1), 2,
        )

        # Draw vertical lines
        for x in range(left, left + width, self.cell_size):
            pygame.draw.line(WIN, LIGHTBLUE, (x, top), (x, top + height))
        # Draw horizontal lines
        for y in range(top, top + height, self.cell_size):
            pygame.draw.line(WIN, LIGHTBLUE, (left, y), (left + width, y))

    def create_dashboard(self):
        """Create a dashboard to the side of, or below, the main grid."""
        if self.layout == LANDSCAPE:
            # Place the dashboard to the right of the main grid
            left = self.grid.right + self.margin_x
            width = self.window_width - self.margin_x - left
            top = self.margin_y
            height = self.grid.bottom - self.margin_y
        else:
            # Place the dashboard below the main grid
            left = self.margin_x
            width = self.grid.right - self.margin_x
            top = self.grid.bottom + self.margin_y
            height = self.window_height - self.margin_y - top

        self.dashboard = pygame.Rect(left, top, width, height)
        # Draw a border around the entire dashboard
        pygame.draw.rect(WIN, BLUE, self.dashboard, 2)

        # Draw the game title at the top of the dashboard
        text_surface = BOLD_FONT.render(GAME_TITLE, True, TEXTCOLOR)
        WIN.blit(
            text_surface, (self.dashboard.left + 5, self.dashboard.top + 5)
        )

    def create_cells(self):
        """Create the initial game grid."""
        # Stop pylint complaining about unused x and y variables:
        # pylint: disable=unused-variable

        for x in range(self.cell_cols):
            column = []
            for y in range(self.cell_rows):
                column.append(False)
            self.cells.append(column)

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
        surface, rect = create_button(QUIT, TEXTCOLOR, DARKGRAY, pos, size)
        self.buttons[QUIT] = [surface, rect]

        # Create a Pause button
        pos = (x + dx, y + dy)
        surface, rect = create_button(PAUSE, TEXTCOLOR, DARKGRAY, pos, size)
        self.buttons[PAUSE] = [surface, rect]

    def draw_buttons(self):
        """Draw control buttons on the screen."""
        for button in self.buttons:
            surface, rect = self.buttons[button][0], self.buttons[button][1]
            WIN.blit(surface, rect)

    def update(self):
        """Update the simulation and update the grid and dashboard."""
        if not self.paused:
            self.update_simulation()
            self.update_grid()
            self.update_dashboard()
            self.generation += 1
        else:
            # The simulation is paused. Display an appropriate message.
            self.update_dashboard("Paused")

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
                    pygame.draw.rect(WIN, WHITE, cell_rect)
                else:
                    # Cell is Off (False).
                    # Leave the cell unfilled.
                    pygame.draw.rect(WIN, BGCOLOR, cell_rect)

    def update_dashboard(self, msg=None):
        """Update the dashboard display.

        This is the default class method: it displays the generation count
        and displays a message. A more detailed update method should be created
        in each child class.
        """
        x = 10
        y = 40
        if self.layout == LANDSCAPE:
            dx = 0
            dy = 20
        else:
            dx = 0
            dy = 20

        # Display the current generation number
        draw_text(
            "Gen:   {}".format(self.generation),
            TEXTCOLOR,
            BGCOLOR,
            self.dashboard.left + x,
            self.dashboard.top + y,
        )
        if msg:
            # Display any status message
            draw_text(
                msg,
                TEXTCOLOR,
                BGCOLOR,
                self.dashboard.left + x + dx,
                self.dashboard.top + y + dy,
            )
        else:
            # Clear the status message area
            draw_text(
                "        ",
                TEXTCOLOR,
                BGCOLOR,
                self.dashboard.left + x + dx,
                self.dashboard.top + y + dy,
            )


class Langton(Grid):
    """Langton's Ant simulation."""

    # Stop pylint complaining about the number of attributes:
    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        """Initialise the simulation."""
        # First, call the parent class __init__() method.
        super().__init__()

        # Game parameters
        self.updated_cells = []
        self.ant_x = int(self.cell_cols / 2)
        self.ant_y = int(self.cell_rows / 2)
        self.ant_init_x = self.ant_x
        self.ant_init_y = self.ant_y
        self.ant_direction = LEFT
        self.out_of_bounds = False

    def update(self):
        """Update the simulation by one generation."""
        if self.paused:
            # The simulation is paused. Display an appropriate message.
            self.update_dashboard("Paused")
        elif self.out_of_bounds:
            # The ant has moved off screen. Display a message and end the
            self.update_dashboard("Completed")
        else:
            # The simulation is proceeding normally.
            self.updated_cells = []
            self.move_ant()
            if not self.out_of_bounds:
                self.update_grid()
                self.update_ant()
                self.update_dashboard()
                self.generation += 1

    def move_ant(self):
        """Update the ant's position."""
        # Record the current position and its value
        self.updated_cells.append(
            [self.ant_x, self.ant_y, self.cells[self.ant_x][self.ant_y]]
        )
        if self.ant_direction == LEFT:
            self.ant_x -= 1
        elif self.ant_direction == RIGHT:
            self.ant_x += 1
        elif self.ant_direction == UP:
            self.ant_y -= 1
        elif self.ant_direction == DOWN:
            self.ant_y += 1

        # Check whether the new ant position is off screen.
        if (
            self.ant_x < 0
            or self.ant_x >= self.cell_cols
            or self.ant_y < 0
            or self.ant_y >= self.cell_rows
        ):
            self.out_of_bounds = True
            return

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

        # Flip the value of the new cell
        cell_value = self.cells[self.ant_x][self.ant_y]
        self.cells[self.ant_x][self.ant_y] = not cell_value
        # Record the new position and its value
        self.updated_cells.append(
            [self.ant_x, self.ant_y, self.cells[self.ant_x][self.ant_y]]
        )

    def update_ant(self):
        """Draw the ant on the main grid."""
        # Make the cell_rect one pixel smaller than the actual grid size in all
        # directions, to prevent drawing over the grid lines.
        cell_x = self.margin_x + self.ant_x * self.cell_size + 1
        cell_y = self.margin_y + self.ant_y * self.cell_size + 1
        cell_rect = pygame.Rect(
            cell_x, cell_y, self.cell_size - 1, self.cell_size - 1
        )
        pygame.draw.rect(WIN, RED, cell_rect)

    def update_grid(self):
        """Draw the current state of the main grid."""
        # This version only draws the two changed cells, so is much faster
        # than iterating across the entire grid.
        for cell in self.updated_cells:
            x = cell[0]
            y = cell[1]
            value = cell[2]
            # Make the cell_rect one pixel smaller than the actual grid
            # size in all directions, to prevent drawing over the grid
            # lines.
            cell_x = self.margin_x + x * self.cell_size + 1
            cell_y = self.margin_y + y * self.cell_size + 1
            cell_rect = pygame.Rect(
                cell_x, cell_y, self.cell_size - 1, self.cell_size - 1
            )
            if value:
                # Cell is On (True).
                # Fill the cell.
                pygame.draw.rect(WIN, WHITE, cell_rect)
            else:
                # Cell is Off (False).
                # Leave the cell unfilled.
                pygame.draw.rect(WIN, BGCOLOR, cell_rect)

    def update_dashboard(self, msg=None):
        """Update the dashboard display."""
        x = 10
        y = 40
        if self.layout == LANDSCAPE:
            dx = 0
            dy = 20
        else:
            dx = 0
            dy = 20

        # Display the current generation number
        draw_text(
            "Gen:  {0:>5}".format(self.generation),
            TEXTCOLOR,
            BGCOLOR,
            self.dashboard.left + x,
            self.dashboard.top + y,
        )
        # Display the ant's X position
        draw_text(
            "Ant X:{0:>5}".format(self.ant_x - self.ant_init_x),
            TEXTCOLOR,
            BGCOLOR,
            self.dashboard.left + x + dx,
            self.dashboard.top + y + dy,
        )
        # Display the ant's Y position
        draw_text(
            "Ant Y:{0:>5}".format(self.ant_y - self.ant_init_y),
            TEXTCOLOR,
            BGCOLOR,
            self.dashboard.left + x + dx * 2,
            self.dashboard.top + y + dy * 2,
        )
        # Display the current simulation update rate in frames per second
        draw_text(
            "FPS:  {0:>5}".format(int(CLOCK.get_fps())),
            TEXTCOLOR,
            BGCOLOR,
            self.dashboard.left + x + dx * 3,
            self.dashboard.top + y + dy * 3,
        )
        if msg:
            # Display any requested status message
            draw_text(
                msg,
                TEXTCOLOR,
                BGCOLOR,
                self.dashboard.left + x + dx * 4,
                self.dashboard.top + y + dy * 4,
                bold=True,
            )
        else:
            # Clear the status message area
            draw_text(
                "        ",
                TEXTCOLOR,
                BGCOLOR,
                self.dashboard.left + x + dx * 4,
                self.dashboard.top + y + dy * 4,
                bold=True,
            )


def main():
    """Initialise the game and call the main game loop."""
    # Tell pylint to ignore the use of the 'global' statement in this function.
    # pylint: disable=global-statement
    global WINDOW_WIDTH, WINDOW_HEIGHT
    global PYGAME_SDL2, FONT, BOLD_FONT
    # Initialise logging
    config_logging()

    # Standard desktop screen size
    # WINDOW_WIDTH, WINDOW_HEIGHT = start_pygame(640, 480, GAME_TITLE)
    # Larger screen size
    WINDOW_WIDTH, WINDOW_HEIGHT = start_pygame(1024, 768, GAME_TITLE)
    # Android tablet screen size
    # WINDOW_WIDTH, WINDOW_HEIGHT = start_pygame(600, 976, GAME_TITLE)

    FONT = pygame.font.SysFont("Courier", FONT_SIZE)
    BOLD_FONT = pygame.font.SysFont("Courier", FONT_SIZE, bold=True)

    run_game()
    end_pygame()


def run_game():
    """Execute the main game loop."""
    WIN.fill(BGCOLOR)
    simulation = Langton()
    # simulation = Grid()
    simulation.draw_buttons()
    pygame.display.update()
    while True:
        # Handle events
        action = check_user_input(simulation.buttons)
        if action:
            # Process the requested action
            print("The player requested action: {}".format(action))
            if action == QUIT:
                # End the simulation
                end_pygame()
            elif action == PAUSE:
                # Toggled the paused state
                simulation.paused = not simulation.paused
            else:
                # No specific simulation action required for any other input
                pass

        # Update the game position
        simulation.update()
        # Update the display
        pygame.display.update()
        # Update the clock once per game loop.
        CLOCK.tick()
        # CLOCK.tick(simulation.frames_per_second)


def check_user_input(buttons):
    """Check for any user input and return the requested action."""
    # Tell pylint to ignore no-member errors.
    # These occur as pylint cannot find the various pygame event types used
    # below.
    # pylint: disable=no-member
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
            # The user clicked a key. Check which key was pressed and assign
            # the appropriate action.
            if event.key in (pygame.K_LEFT, pygame.K_a):
                action = LEFT
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                action = RIGHT
            elif event.key in (pygame.K_UP, pygame.K_w):
                action = UP
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                action = DOWN
            elif event.key in (pygame.K_SPACE, pygame.K_p):
                action = PAUSE
            elif event.key in (pygame.K_ESCAPE, pygame.K_q):
                action = QUIT
    return action


def create_button(text, color, bgcolor, pos, size):
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
    text_surface = FONT.render(text, True, color)
    # Get the size of the rendered text in pixels
    text_size = FONT.size(text)
    # Determine where to place the text on the button, so that it appears to
    # be centered
    text_x = int((width - text_size[0]) / 2)
    text_y = int((height - text_size[1]) / 2)

    button_surface.blit(text_surface, (text_x, text_y))
    return (button_surface, button_rect)


def draw_text(text, color, bgcolor, top, left, bold=False):
    """Create Surface and Rect objects for on screen text."""
    if bold:
        text_surface = BOLD_FONT.render(text, True, color, bgcolor)
    else:
        text_surface = FONT.render(text, True, color, bgcolor)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (top, left)
    WIN.blit(text_surface, (top, left))


def start_pygame(width, height, title):
    """Start Pygame and create the Pygame window."""
    # Tell pylint to ignore the use of the 'global' statement in this function.
    # pylint: disable=global-statement
    global WIN, CLOCK

    # Initialise the Pygame display window
    pygame.init()
    # Initialise a Pygame clock timer. This helps calculate the frame rate.
    CLOCK = pygame.time.Clock()

    # Set the window title. This has no effect on Android.
    pygame.display.set_caption(title)
    
    # Set the window icon
    icon = pygame.image.load('langton_icon.png')
    pygame.display.set_icon(icon)

    # Create the Pygame window. On a desktop running standard Pygame, the
    # requested width and height will be used. On an Android device running
    # Pydroid3 and pygame_sdl2, the requested values are ignored and the full
    # device screen size is used instead, so we will need to recheck the actual
    # window size after it is created.
    WIN = pygame.display.set_mode((width, height))

    # Check the actual window size
    width = pygame.display.Info().current_w
    height = pygame.display.Info().current_h
    logging.debug("Pygame window size: (%s, %s)", width, height)
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
    logging.debug("")
    logging.debug("Python %s", sys.version)
    logging.debug("Platform %s", sys.platform)
    logging.debug("Starting %s", GAME_TITLE)


if __name__ == "__main__":
    main()
