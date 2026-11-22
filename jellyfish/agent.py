import pygame
import math
import random

from config import EnvironmentConfig


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

        # Normal movement parameters
        self.max_speed = 2
        self.base_max_speed = 2
        self.max_force = 0.05

        self.perception = 100

        self.pulse = 0

        self.color = (180, 120, 255)

        # Environmental response variables
        self.environmental_stress = 0.0

        self.swimming_speed = self.base_max_speed

        self.current_influence = pygame.Vector2(0, 0)

        # Pollution response
        self.pollution_stress = 0.0
        self.pollution_exposure = 0.0
        self.normal_color = self.color


    # Environmental response
    def apply_environment(self, ocean):

        temperature = EnvironmentConfig.TEMPERATURE
        ph = EnvironmentConfig.PH

        # --------------------------------
        # Temperature influence
        # --------------------------------

        temperature_factor = 1 + (temperature - 20) * 0.01

        temperature_factor = max(
            0.75,
            min(1.25, temperature_factor)
        )

        # --------------------------------
        # pH influence on environmental stress
        # --------------------------------

        ph_stress = abs(ph - 8.1) / 1.5

        ph_stress = max(0, min(1, ph_stress))

        self.environmental_stress = ph_stress

        # --------------------------------
        # Calculate swimming speed
        # --------------------------------

        stress_factor = 1 - (0.25 * self.environmental_stress)

        self.swimming_speed = (
            self.base_max_speed
            * temperature_factor
            * stress_factor
        )

        self.max_speed = max(
            EnvironmentConfig.MIN_SWIMMING_SPEED,
            min(
                EnvironmentConfig.MAX_SWIMMING_SPEED,
                self.swimming_speed
            )
        )

        # --------------------------------
        # Ocean current influence
        # --------------------------------

        current = ocean.get_current(self.position)

        self.current_influence = current

        self.acceleration += current * 0.04


    def apply_pollution(self, hotspots, dt):

        exposure = 0.0
        avoidance = pygame.Vector2(0, 0)

        for hotspot in hotspots:

            distance = self.position.distance_to(hotspot.position)
            radius = hotspot.detection_radius

            if distance < radius:

                hotspot.detect(self)

                level = max(0, min(1, hotspot.pollution_level))

                influence = level * (1 - distance / radius)

                exposure = max(exposure, influence)

                if distance > 0:
                    direction = self.position - hotspot.position
                    avoidance += direction.normalize() * influence

        self.pollution_exposure = exposure

        # Pollution stress builds up and gradually recovers
        if exposure > 0:
            self.pollution_stress += exposure * 0.25 * dt
        else:
            self.pollution_stress -= 0.08 * dt

        self.pollution_stress = max(
            0.0, min(1.0, self.pollution_stress)
        )

        # Pollution reduces swimming speed
        speed_factor = (
            1 - 0.35 * exposure - 0.20 * self.pollution_stress
        )

        self.max_speed = max(
            EnvironmentConfig.MIN_SWIMMING_SPEED,
            min(
                EnvironmentConfig.MAX_SWIMMING_SPEED,
                self.swimming_speed * speed_factor
            )
        )

        # Mild movement away from polluted areas
        if avoidance.length() > 0:
            avoidance.scale_to_length(0.04 * exposure)
            self.acceleration += avoidance

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

        # Boundary steering
        boundary_margin = 80

        if self.position.x < boundary_margin:
            self.acceleration.x += 0.08

        elif self.position.x > width - boundary_margin:
            self.acceleration.x -= 0.08
        
        self.velocity += self.acceleration

        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        self.position += self.velocity

        self.acceleration = pygame.Vector2(0, 0)

        # Boundary control
        if self.position.x < 20:
            self.position.x = 20
            if self.velocity.x < 0:
                self.velocity.x *= -1

        elif self.position.x > width - 20:
            self.position.x = width - 20
            if self.velocity.x > 0:
                self.velocity.x *= -1

        if self.position.y < 100:
            self.position.y = 100
            if self.velocity.y < 0:
                self.velocity.y *= -1

        elif self.position.y > height - 60:
            self.position.y = height - 60
            if self.velocity.y > 0:
                self.velocity.y *= -1

        self.pulse += 0.1

    # Draw jellyfish
    def draw(self, screen):

        x = int(self.position.x)
        y = int(self.position.y)

        size = self.radius + math.sin(self.pulse) * 3

        display_color = (
            int(180 + 75 * self.pollution_stress),
            int(120 - 70 * self.pollution_stress),
            int(255 - 200 * self.pollution_stress)
        )
        pygame.draw.circle(
            screen,
            display_color,
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