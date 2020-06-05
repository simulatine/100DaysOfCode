#!python3
# -*- coding: utf-8 -*-
"""
Voting Game Simulation.
This cellular automata is from Scientific American article by A.K. Dewdney,
originally published in April 1985, and also included in his book
The Armchair Universe published in 1988.

The simulation begins with a rectangular grid (representing a country) covered
in a random mix of two cell types, shown as Blue and Red on the screen, and
tracked as 0 and 1 in the code. Each cell represents the voting preferences of
an individual voter.

In each generation, one cell (voter) chosen at random changes its voting
preference to that of one of its neighbors, also chosen at random.

Over time, large blocks of votes develop within the grid. The blocks are
geographic areas where everyone has the same opinion. Then the blocks migrate
around the grid, and for a while two blocks struggle for dominance. Finally the
two-party system collapses as everyone ends up voting the same way. The smaller
block vanishes as democracy votes itself out of existence - or does it?

Simulatine, 01 Jun, 2020 - Initial version.
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


class VotingGame(sim.Grid):
    """
    Voting Game cellular automata.
    
    All cells in the grid are initially either 0 or 1 at random. In each
    generation, a cell is selected at random, and takes on the value of one its
    eight neighbors also selected at random.
    After time blocks of single colors should start to form. Eventually the
    entire grid switches to either 0 or 1, and the other value disappears
    entirely.
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

        # Pick a random neighbor of the cell
        dx, dy = 0, 0
        while (dx, dy) == (0, 0):
            dx = random.randint(-1, 1)
            dy = random.randint(-1, 1)
        neighbor_x = (x + dx) % self.cell_cols
        neighbor_y = (y + dy) % self.cell_rows

        # Voting game
        new_value = self.cells[neighbor_x][neighbor_y]
        # Anti-voting game
        # new_value = int(not self.cells[neighbor_x][neighbor_y])

        # They may be the same, in which case there is nothing to change.
        if old_value != new_value:
            # Update the population counts for the old value and the new value
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
    title = "Voting Game"
    # Initialise logging
    sim.config_logging(title)

    # Standard desktop screen size
    display_surface = sim.start_pygame(640, 440, title)
    # Larger screen size
    # display_surface = sim.start_pygame(1024, 768, title)
    # Android tablet screen size
    # display_surface = start_pygame(600, 976, title)

    run_game(display_surface, title)


def run_game(display_surface, title):
    """Execute the main game loop."""
    simulation = VotingGame(display_surface, title)
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
