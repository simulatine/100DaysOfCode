#!python3
# -*- coding: utf-8 -*-
"""
Majority Rule Simulation.

The simulation begins with a rectangular grid (representing a country) covered
in a random mix of two cell types, shown as Blue and Red on the screen, and
tracked as 0 and 1 in the code. Each cell represents the voting preferences of
an individual voter.

In each generation, one cell (voter) chosen at random changes its voting
preference to the view held by the majority of its 8 neighbors.

Over time, large blocks of votes develop within the grid. The blocks are
geographic areas where everyone has the same opinion. The blocks start to
solidify until there are two roughly equal size areas of Red and Blue.
Occasional changes will then happen around the edges of each block as they
straighten out.

Simulatine, 02 Jun, 2020 - Initial version.
"""

import random

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


class MajorityRule(sim.Grid):
    """
    Majority Rule cellular automata.
    
    All cells in the grid are initially either 1 or 0 at random. In each
    generation, a cell is selected at random, and takes on the majority value
    of its eight neighbors. After time blocks of single colors will form,
    and start to harden into straight lines.
    """

    # Stop pylint complaining about the number of attributes:
    # pylint: disable=too-many-instance-attributes
    def __init__(self, win, title):
        """Initialise the simulation."""
        # Game parameters
        self.populations = [0, 0]

        # Call the parent class __init__() method.
        super().__init__(win, title)

    def create_cells(self):
        """Create the initial game grid."""
        # Stop pylint complaining about unused x and y variables:
        # pylint: disable=unused-variable

        self.updated_cells = []
        for x in range(self.cell_cols):
            column = []
            for y in range(self.cell_rows):
                value = random.randint(0, 1)
                column.append(value)
                self.populations[value] += 1
                self.updated_cells.append([x, y])
            self.cells.append(column)

    def update(self):
        """Update the simulation by one generation."""
        if self.paused:
            # The simulation is paused. Display an appropriate message.
            self.update_dashboard("Paused")
        else:
            # The simulation is proceeding normally.
            self.update_cell()
            self.update_grid()
            self.update_dashboard()
            self.update_voting_dashboard()
            self.generation += 1
            # Update the Pygame clock once per game loop.
            self.clock.tick()

    def update_cell(self):
        # Pick a random cell
        self.updated_cells = []
        x = random.randrange(self.cell_cols)
        y = random.randrange(self.cell_rows)
        old_value = self.cells[x][y]
        
        # Get the total value of all the neighboring cells
        neighbor_values = 0
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if not (dx, dy) == (0, 0):
                    neighbor_x = (x + dx) % self.cell_cols
                    neighbor_y = (y + dy) % self.cell_rows
                    neighbor_values += self.cells[neighbor_x][neighbor_y]
        if neighbor_values > 4:
            # Majority of neighbors are 1. Set this cell to 1.
            new_value = 1
        elif neighbor_values < 4:
            # Majority of neighbors are 0. Set this cell to 0.
            new_value = 0
        else:
            # Neighbors are evenly split between 0's and 1's. Make no change.
            new_value = old_value

        if old_value != new_value:
            self.populations[old_value] -= 1
            self.populations[new_value] += 1
            # Assign the value of the neighbor to this cell
            self.cells[x][y] = new_value
            # Note that the cell value has changed
            self.updated_cells = [[x, y]]

    def update_grid(self):
        """Draw the current state of the main grid."""
        # This only draws changed cells, which is much faster
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
                # Cell is On (1).
                # Fill the cell with blue.
                pygame.draw.rect(self.win, sim.BLUE, cell_rect)
            else:
                # Cell is Off (0).
                # Fill the cell with red.
                pygame.draw.rect(self.win, sim.RED, cell_rect)

    def update_voting_dashboard(self):
        """Update the dashboard display with status for the simulation."""
        # Display the red (0) and blue (1) population
        self.draw_text(
            "Red: {:>7}".format(self.populations[0]),
            sim.TEXTCOLOR,
            sim.BGCOLOR,
            self.dashboard.left + self.dash_pos_x,
            self.dashboard.top + self.dash_pos_y,
        )
        self.draw_text(
            "Blue:{:>7}".format(self.populations[1]),
            sim.TEXTCOLOR,
            sim.BGCOLOR,
            self.dashboard.left + self.dash_pos_x + self.dash_offset_x,
            self.dashboard.top + self.dash_pos_y + self.dash_offset_y,
        )


def main():
    """Initialise the game and call the main game loop."""
    title = "Majority Rule"
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
    simulation = MajorityRule(display_surface, title)
    simulation.draw_buttons()
    simulation.update_grid()
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
        # Check if either population has reduced to zero.
        if simulation.populations[0] == 0 or simulation.populations[1] == 0:
            simulation.paused = True
        
        # Update the display
        pygame.display.update()
        # CLOCK.tick(simulation.frames_per_second)


if __name__ == "__main__":
    main()
