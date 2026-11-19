import pygame


class Obstacle:

    def __init__(self, x, y, radius):

        self.position = pygame.Vector2(x, y)
        self.radius = radius
        self.color = (105, 105, 110)

    def draw(self, screen):

        pygame.draw.circle(
            screen,
            self.color,
            (int(self.position.x), int(self.position.y)),
            self.radius
        )

        # Add a lighter outline
        pygame.draw.circle(
            screen,
            (150, 150, 155),
            (int(self.position.x), int(self.position.y)),
            self.radius,
            2
        )