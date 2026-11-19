import pygame
import math
import random


class Jellyfish:

    def __init__(self, x, y):

        self.position = pygame.Vector2(x, y)

        self.velocity = pygame.Vector2(
            random.uniform(-1, 1),
            random.uniform(-1, 1)
        )

        if self.velocity.length() == 0:
            self.velocity = pygame.Vector2(1, 0)

        self.velocity = self.velocity.normalize()

        self.acceleration = pygame.Vector2(0, 0)

        self.radius = 12
        self.max_speed = 2
        self.max_force = 0.05

        self.perception = 100

        self.pulse = 0

        self.color = (180, 120, 255)

    # Separation: Avoid crowding
    def separation(self, swarm):

        steering = pygame.Vector2(0, 0)
        total = 0

        for other in swarm:

            distance = self.position.distance_to(other.position)

            if other != self and 0 < distance < 35:

                difference = self.position - other.position

                difference = difference.normalize() / distance

                steering += difference
                total += 1

        if total > 0:

            steering /= total

            if steering.length() > 0:
                steering = steering.normalize() * self.max_speed
                steering -= self.velocity
                steering = steering.normalize() * min(
                    steering.length(), self.max_force
                )

        return steering

    # Alignment: Match neighbours' direction
    def alignment(self, swarm):

        average = pygame.Vector2(0, 0)
        total = 0

        for other in swarm:

            distance = self.position.distance_to(other.position)

            if other != self and distance < self.perception:

                average += other.velocity
                total += 1

        if total > 0:

            average /= total

            if average.length() > 0:
                average = average.normalize() * self.max_speed
                average -= self.velocity

                if average.length() > self.max_force:
                    average.scale_to_length(self.max_force)

        return average

    # Cohesion: Move towards the group
    def cohesion(self, swarm):

        centre = pygame.Vector2(0, 0)
        total = 0

        for other in swarm:

            distance = self.position.distance_to(other.position)

            if other != self and distance < self.perception:

                centre += other.position
                total += 1

        if total > 0:

            centre /= total

            direction = centre - self.position

            if direction.length() > 0:
                direction = direction.normalize() * self.max_speed
                direction -= self.velocity

                if direction.length() > self.max_force:
                    direction.scale_to_length(self.max_force)

            return direction

        return pygame.Vector2(0, 0)


    # Obstacle avoidance
    def avoid_obstacles(self, obstacles):

        steering = pygame.Vector2(0, 0)

        for obstacle in obstacles:

            distance = self.position.distance_to(obstacle.position)

            safe_distance = self.radius + obstacle.radius + 45

            if 0 < distance < safe_distance:

                difference = self.position - obstacle.position

                difference = difference.normalize()

                steering += difference * (
                    (safe_distance - distance) / safe_distance
            )

        if steering.length() > 0:

            steering = steering.normalize() * self.max_speed

            steering -= self.velocity

            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)

        return steering

    # Apply swarm behaviours
    def flock(self, swarm):

        sep = self.separation(swarm)
        ali = self.alignment(swarm)
        coh = self.cohesion(swarm)

        self.acceleration += sep * 1.5
        self.acceleration += ali * 1.0
        self.acceleration += coh * 1.0

    # Update movement
    def update(self, width, height):

        self.velocity += self.acceleration

        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        self.position += self.velocity

        self.acceleration = pygame.Vector2(0, 0)

        # Boundary control
        if self.position.x < 20 or self.position.x > width - 20:
            self.velocity.x *= -1

        if self.position.y < 100 or self.position.y > height - 60:
            self.velocity.y *= -1

        self.position.x = max(20, min(width - 20, self.position.x))
        self.position.y = max(100, min(height - 60, self.position.y))

        self.pulse += 0.1

    # Draw jellyfish
    def draw(self, screen):

        x = int(self.position.x)
        y = int(self.position.y)

        size = self.radius + math.sin(self.pulse) * 3

        pygame.draw.circle(
            screen,
            self.color,
            (x, y),
            int(size)
        )

        for i in range(4):

            offset = (i - 1.5) * 6

            pygame.draw.line(
                screen,
                (220, 200, 255),
                (int(x + offset), int(y + size)),
                (int(x + offset), int(y + size + 20)),
                2
            )