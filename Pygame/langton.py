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
Simulatine, 01 Jun, 2020 - Separated Grid class and generic variables into a
                           module sim.py for reuse with other simulations.
"""
# Import Pygame, either standard version or SDL2 version depending on the
# platform.
try:
    import pygame_sdl2  # pylint: disable=import-error

    pygame_sdl2.import_as_pygame()
    PYGAME_SDL2 = True
except ModuleNotFoundError:
    PYGAME_SDL2 = False
import pygame

import sim


class Langton(sim.Grid):
    """Langton's Ant simulation."""

    # Stop pylint complaining about the number of attributes:
    # pylint: disable=too-many-instance-attributes
    def __init__(self, win, title):
        """Initialise the simulation."""
        # First, call the parent class __init__() method.
        super().__init__(win, title)

        # Game parameters
        self.updated_cells = []
        self.ant_x = int(self.cell_cols / 2)
        self.ant_y = int(self.cell_rows / 2)
        self.ant_init_x = self.ant_x
        self.ant_init_y = self.ant_y
        self.ant_direction = sim.LEFT
        self.out_of_bounds = False

        # Ant movement (x and y values for each direction)
        self.dirs = {
            sim.LEFT: [-1, 0],
            sim.RIGHT: [1, 0],
            sim.UP: [0, -1],
            sim.DOWN: [0, 1],
        }

        # Value to increment population in the move_ant() method.
        # Increase the population by 1 if we switch a cell to True
        # Decrease the population by 1 if we switch a cell to False
        self.update_population = {True: +1, False: -1}

    def update(self):
        """Update the simulation by one generation."""
        if self.paused:
            # The simulation is paused. Display an appropriate message.
            self.update_dashboard("Paused")
        elif self.out_of_bounds:
            # The ant has moved off screen. Display an appropriate message.
            self.update_dashboard("Completed")
        else:
            # The simulation is proceeding normally.
            self.updated_cells = []
            self.move_ant()
            if not self.out_of_bounds:
                self.update_grid()
                self.update_ant()
                self.update_dashboard()
                self.update_langton_dashboard()
                self.generation += 1
                # Update the Pygame clock once per game loop.
                self.clock.tick()

    def move_ant(self):
        """Update the ant's position."""
        # Record the current position and its value
        self.updated_cells.append([self.ant_x, self.ant_y])

        # Move the ant in its current direction
        self.ant_x += self.dirs[self.ant_direction][0]
        self.ant_y += self.dirs[self.ant_direction][1]

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
            index = sim.DIRECTIONS.index(self.ant_direction)
            index = (index - 1) % len(sim.DIRECTIONS)
            self.ant_direction = sim.DIRECTIONS[index]
        else:
            # Cell is Off (False).
            # Turn clockwise
            index = sim.DIRECTIONS.index(self.ant_direction)
            index = (index + 1) % len(sim.DIRECTIONS)
            self.ant_direction = sim.DIRECTIONS[index]

        # Flip the value of the new cell
        new_cell_value = not self.cells[self.ant_x][self.ant_y]
        self.cells[self.ant_x][self.ant_y] = new_cell_value
        self.population += self.update_population[new_cell_value]
        # Record the new position and its value
        self.updated_cells.append([self.ant_x, self.ant_y])

    def update_ant(self):
        """Draw the ant on the main grid."""
        # Make the cell_rect one pixel smaller than the actual grid size in all
        # directions, to prevent drawing over the grid lines.
        cell_x = self.margin_x + self.ant_x * self.cell_size + 1
        cell_y = self.margin_y + self.ant_y * self.cell_size + 1
        cell_rect = pygame.Rect(
            cell_x, cell_y, self.cell_size - 1, self.cell_size - 1
        )
        pygame.draw.rect(self.win, sim.RED, cell_rect)

    def update_grid(self):
        """Draw the current state of the main grid."""
        # This version only draws the two changed cells, so is much faster
        # than iterating across the entire grid.
        for cell in self.updated_cells:
            x = cell[0]
            y = cell[1]
            value = self.cells[x][y]
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
                pygame.draw.rect(self.win, sim.WHITE, cell_rect)
            else:
                # Cell is Off (False).
                # Leave the cell unfilled.
                pygame.draw.rect(self.win, sim.BGCOLOR, cell_rect)

    def update_langton_dashboard(self):
        """Update the dashboard display with status for the simulation."""
        # Display the ant's X position
        self.draw_text(
            "Ant X: {:>5}".format(self.ant_x - self.ant_init_x),
            sim.TEXTCOLOR,
            sim.BGCOLOR,
            self.dashboard.left + self.dash_pos_x,
            self.dashboard.top + self.dash_pos_y,
        )
        # Display the ant's Y position
        self.draw_text(
            "Ant Y: {:>5}".format(self.ant_y - self.ant_init_y),
            sim.TEXTCOLOR,
            sim.BGCOLOR,
            self.dashboard.left + self.dash_pos_x + self.dash_offset_x,
            self.dashboard.top + self.dash_pos_y + self.dash_offset_y,
        )


def main():
    """Initialise the game and call the main game loop."""
    title = "Langton's Ant"
    # Initialise logging
    sim.config_logging(title)

    # Standard desktop screen size
    # display_surface = sim.start_pygame(640, 480, title)
    # Larger screen size
    display_surface = sim.start_pygame(1024, 768, title)
    # Android tablet screen size
    # display_surface = start_pygame(600, 976, title)

    run_game(display_surface, title)


def run_game(display_surface, title):
    """Execute the main game loop."""
    simulation = Langton(display_surface, title)
    simulation.draw_buttons()
    pygame.display.update()
    while True:
        # Handle events
        action = sim.check_user_input(
            simulation.buttons, simulation.keyboard_actions
        )
        if action:
            # Process the requested action
            if action == sim.QUIT:
                # End the simulation
                sim.end_pygame()
            elif action == sim.PAUSE:
                # Toggled the paused state
                simulation.paused = not simulation.paused
            else:
                # No specific simulation action required for any other input
                pass

        # Update the game position
        simulation.update()
        # Update the display
        pygame.display.update()
        # CLOCK.tick(simulation.frames_per_second)


if __name__ == "__main__":
    main()
