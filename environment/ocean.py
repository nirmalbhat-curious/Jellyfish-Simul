import pygame
import math


class Ocean:

    def __init__(self):

        from config import EnvironmentConfig

        self.config = EnvironmentConfig

        self.current_strength = self.config.CURRENT_STRENGTH

        self.time = 0.0

    # Update ocean environment continuously
    def update(self, dt):
        self.time += dt
    
    
     # Calculate wave intensity based on temperature
    def get_wave_amplitude(self):

        temperature = self.config.TEMPERATURE

        return 8 + (temperature * 0.4)

    # Calculate wave speed based on temperature
    def get_wave_speed(self):

        temperature = self.config.TEMPERATURE

        return 1 + (temperature * 0.05)
    # Calculate dynamic ocean current
    def get_current(self, position):

        x = position.x
        y = position.y

        t = self.time

        strength = self.current_strength

        horizontal = (
            self.config.CURRENT_VARIABILITY
            * math.sin(y * 0.015 + t * 0.5)
        )

        vertical = (
            self.config.CURRENT_VARIABILITY
            * math.sin(x * 0.01 + t * 0.7)
        )

        return pygame.Vector2(horizontal, vertical)


        # Draw dynamic ocean waves
    def draw_waves(self, screen):

        amplitude = self.get_wave_amplitude()
        speed = self.get_wave_speed()

        for x in range(0, 1000, 5):

            y = 400 + amplitude * math.sin(
                x * 0.02 + self.time * speed
            )

            pygame.draw.circle(
                screen,
                (40, 100, 160),
                (x, int(y)),
                2
            )


    # Display current direction using arrows
    def draw_currents(self, screen):

        for x in range(100, 1000, 150):

            for y in range(150, 600, 100):

                position = pygame.Vector2(x, y)

                current = self.get_current(position)

                if current.length() == 0:
                    continue

                direction = current.normalize() * 35

                end = position + direction

                pygame.draw.line(
                    screen,
                    (65, 135, 175),
                    position,
                    end,
                    2
                )

                # Arrowhead
                back = -direction.normalize() * 9

                p1 = end + back.rotate(30)
                p2 = end + back.rotate(-30)

                pygame.draw.polygon(
                    screen,
                    (65, 135, 175),
                    [end, p1, p2]
                )

class PollutionHotspot:

    def __init__(self, x, y, pollution_level):

        self.position = pygame.Vector2(x, y)

        self.pollution_level = pollution_level

        self.detection_radius = 65

        self.detected = False

        self.detected_by = set()

    # Check whether a jellyfish detects pollution
    def detect(self, jellyfish):

        distance = self.position.distance_to(
            jellyfish.position
        )

        if distance < self.detection_radius:

            self.detected = True

            self.detected_by.add(id(jellyfish))

            return True

        return False

    # Display pollution hotspot
    def draw(self, screen):

        if self.detected:
            color = (255, 180, 40)
        else:
            color = (220, 60, 60)

        # Detection area
        surface = pygame.Surface(
            (self.detection_radius * 2,
             self.detection_radius * 2),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            surface,
            (*color, 45),
            (self.detection_radius, self.detection_radius),
            self.detection_radius
        )

        screen.blit(
            surface,
            (
                int(self.position.x - self.detection_radius),
                int(self.position.y - self.detection_radius)
            )
        )

        # Hotspot centre
        pygame.draw.circle(
            screen,
            color,
            (int(self.position.x), int(self.position.y)),
            12
        )

        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (int(self.position.x), int(self.position.y)),
            12,
            2
        )