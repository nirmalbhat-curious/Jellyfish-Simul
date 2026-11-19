import pygame
import math


class CoverageTracker:

    def __init__(self, width, height):
        
        self.width = width
        self.height = height

        self.cell_size = 25
        self.sensor_radius = 45

        self.min_y = 80
        self.max_y = height - 40

        self.columns = math.ceil(width / self.cell_size)

        self.rows = math.ceil(
            (self.max_y - self.min_y) / self.cell_size
        )

        # Store explored regions
        self.visited_cells = set()

        # Record simulation start time
        self.start_time = pygame.time.get_ticks()

        self.coverage_history = []
        self.time_history = []

        self.last_recorded_time = 0

    def update(self, swarm):

        for jellyfish in swarm:

            x = jellyfish.position.x
            y = jellyfish.position.y

            # Find nearby grid cells
            min_col = max(
                0,
                int((x - self.sensor_radius) / self.cell_size)
            )

            max_col = min(
                self.columns - 1,
                int((x + self.sensor_radius) / self.cell_size)
            )

            min_row = max(
                0,
                int((y - self.sensor_radius - self.min_y) / self.cell_size)
            )

            max_row = min(
                self.rows - 1,
                int((y + self.sensor_radius - self.min_y) / self.cell_size)
            )

            for row in range(min_row, max_row + 1):

                for col in range(min_col, max_col + 1):

                    cell_x = col * self.cell_size + self.cell_size / 2

                    cell_y = (
                        self.min_y
                        + row * self.cell_size
                        + self.cell_size / 2
                    )

                    distance = math.sqrt(
                        (x - cell_x) ** 2 +
                        (y - cell_y) ** 2
                    )

                    if distance <= self.sensor_radius:

                        self.visited_cells.add((row, col))
        elapsed = self.get_elapsed_time()

        if elapsed - self.last_recorded_time >= 1:

            self.coverage_history.append(
                self.get_coverage()
            )

            self.time_history.append(elapsed)

            self.last_recorded_time = elapsed           

    def get_coverage(self):

        total_cells = self.columns * self.rows

        if total_cells == 0:
            return 0

        percentage = (
            len(self.visited_cells) / total_cells
        ) * 100

        return percentage

    def get_elapsed_time(self):

        elapsed = (
            pygame.time.get_ticks() - self.start_time
        ) / 1000

        return elapsed