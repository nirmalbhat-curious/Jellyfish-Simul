import random
import pygame
import sys

from jellyfish.agent import Jellyfish
from environment.ocean import Ocean
from environment.obstacles import Obstacle
from environment.ocean import PollutionHotspot
from analysis.metrics import CoverageTracker
from analysis.graphs import plot_coverage
from config import EnvironmentConfig


# Initialize pygame
pygame.init()

# Window dimensions
WIDTH = 1000
HEIGHT = 650

# Create simulation window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Biohybrid Jellyfish Swarm Simulator")

# Colours
OCEAN_BLUE = (10, 35, 75)
LIGHT_BLUE = (30, 100, 160)
WHITE = (255, 255, 255)

# Clock controls frame rate
clock = pygame.time.Clock()

# Create a swarm of 20 jellyfish
jellyfish_swarm = []

for i in range(20):

    x = random.randint(50, WIDTH - 50)
    y = random.randint(120, HEIGHT - 80)

    jellyfish_swarm.append(Jellyfish(x, y))

# Create ocean environment
ocean = Ocean()

# Create underwater obstacles
obstacles = [

    Obstacle(250, 250, 35),

    Obstacle(500, 400, 45),

    Obstacle(750, 230, 30),

    Obstacle(850, 480, 40)

]

# Create pollution hotspots

pollution_hotspots = [

    PollutionHotspot(350, 200, 80),

    PollutionHotspot(650, 350, 60),

    PollutionHotspot(800, 500, 95),

    PollutionHotspot(200, 450, 70)

]

# Initialize coverage tracker

coverage_tracker = CoverageTracker(WIDTH, HEIGHT)

running = True

# Main simulation loop
# Main simulation loop

while running:

    # Calculate time elapsed between frames
    dt = clock.tick(60) / 1000.0

    # Update ocean environment
    ocean.update(dt)

    # Handle events

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            # Temperature controls
            if event.key == pygame.K_UP:
                EnvironmentConfig.TEMPERATURE = min(
                    35, EnvironmentConfig.TEMPERATURE + 1
                )

            elif event.key == pygame.K_DOWN:
                EnvironmentConfig.TEMPERATURE = max(
                    0, EnvironmentConfig.TEMPERATURE - 1
                )

            # pH controls
            elif event.key == pygame.K_RIGHT:
                EnvironmentConfig.PH = min(
                    9.0, round(EnvironmentConfig.PH + 0.1, 1)
                )

            elif event.key == pygame.K_LEFT:
                EnvironmentConfig.PH = max(
                    6.0, round(EnvironmentConfig.PH - 0.1, 1)
                )

            # Reset environment
            elif event.key == pygame.K_r:
                EnvironmentConfig.TEMPERATURE = 20.0
                EnvironmentConfig.PH = 8.1

    # Background
    screen.fill(OCEAN_BLUE)

    # Ocean surface
    pygame.draw.rect(
        screen,
        LIGHT_BLUE,
        (0, 0, WIDTH, 80)
    )

    # Seabed
    pygame.draw.rect(
        screen,
        (110, 90, 55),
        (0, HEIGHT - 40, WIDTH, 40)
    )

    # Display ocean currents
    ocean.draw_currents(screen)

    # Title
    font = pygame.font.Font(None, 36)
    title = font.render(
        "Jellyfish Swarm Simulation",
        True,
        WHITE
    )

    screen.blit(title, (WIDTH // 2 - 190, 25))

    # Calculate swarm behaviour
    for jellyfish in jellyfish_swarm:

        # Apply normal flocking
        jellyfish.flock(jellyfish_swarm)

        # Apply environmental effects
        jellyfish.apply_environment(ocean)

        jellyfish.apply_pollution(pollution_hotspots, dt)

        # Apply obstacle avoidance
        avoidance = jellyfish.avoid_obstacles(obstacles)

        jellyfish.acceleration += avoidance * 3.0

    # Draw underwater obstacles
    for obstacle in obstacles:

        obstacle.draw(screen)

    # Draw pollution hotspots

    for hotspot in pollution_hotspots:

        hotspot.draw(screen)


    # Update and draw jellyfish

    for jellyfish in jellyfish_swarm:

        jellyfish.update(WIDTH, HEIGHT)

        jellyfish.draw(screen)

    # Update coverage information

    coverage_tracker.update(jellyfish_swarm)

    # Display pollution detection statistics

    detected_count = sum(
        1 for hotspot in pollution_hotspots
        if hotspot.detected
    )

    font = pygame.font.Font(None, 28)

    status = font.render(
        f"Pollution Hotspots Detected: {detected_count}/4",
        True,
        WHITE
    )

    screen.blit(status, (20, 100))

    # Display coverage percentage

    coverage = coverage_tracker.get_coverage()

    coverage_text = font.render(
        f"Ocean Coverage: {coverage:.2f}%",
        True,
        WHITE
    )

    screen.blit(coverage_text, (20, 130))

    # Display elapsed time

    elapsed = coverage_tracker.get_elapsed_time()

    time_text = font.render(
        f"Simulation Time: {elapsed:.1f} seconds",
        True,
        WHITE
    )

    screen.blit(time_text, (20, 160))


    # Environmental dashboard

    temperature_text = font.render(
        f"Temperature: {EnvironmentConfig.TEMPERATURE:.1f} C",
        True,
        WHITE
    )

    ph_text = font.render(
        f"Ocean pH: {EnvironmentConfig.PH:.1f}",
        True,
        WHITE
    )

    average_stress = sum(
        jellyfish.pollution_stress for jellyfish in jellyfish_swarm
    ) / len(jellyfish_swarm)

    stress_text = font.render(
        f"Average Pollution Stress: {average_stress:.2f}",
        True,
        WHITE
    )

    screen.blit(temperature_text, (20, 200))
    screen.blit(ph_text, (20, 230))
    screen.blit(stress_text, (20, 260))

     # Update display
    pygame.display.flip()

plot_coverage(
    coverage_tracker.time_history,
    coverage_tracker.coverage_history
)

# Close pygame
pygame.quit()
sys.exit()
