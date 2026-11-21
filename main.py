import random
import pygame
import sys
import math

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

# --------------------------------------
# SIMULATION CONFIGURATION MENU
# --------------------------------------

jellyfish_count = 20
hotspot_count = 4
temperature = 20.0
ph = 8.1

menu_running = True
simulation_started = False

menu_font = pygame.font.Font(None, 40)
small_font = pygame.font.Font(None, 32)

while menu_running:

    screen.fill(OCEAN_BLUE)

    title = menu_font.render(
        "Jellyfish Simulator Configuration",
        True,
        WHITE
    )

    screen.blit(title, (220, 70))

    # Display selected values
    settings = [
        ("Jellyfish", jellyfish_count),
        ("Pollution Hotspots", hotspot_count),
        ("Temperature", f"{temperature:.1f} C"),
        ("Ocean pH", f"{ph:.1f}")
    ]

    y_positions = [180, 270, 360, 450]

    for i, (label, value) in enumerate(settings):

        text = menu_font.render(
            f"{label}: {value}",
            True,
            WHITE
        )

        screen.blit(text, (250, y_positions[i]))

        # Minus button
        minus_button = pygame.Rect(
            650, y_positions[i], 50, 40
        )

        # Plus button
        plus_button = pygame.Rect(
            720, y_positions[i], 50, 40
        )

        pygame.draw.rect(screen, LIGHT_BLUE, minus_button)
        pygame.draw.rect(screen, LIGHT_BLUE, plus_button)

        minus_text = small_font.render("-", True, WHITE)
        plus_text = small_font.render("+", True, WHITE)

        screen.blit(minus_text, (665, y_positions[i] + 5))
        screen.blit(plus_text, (735, y_positions[i] + 5))

    # Start button
    start_button = pygame.Rect(400, 540, 200, 60)

    pygame.draw.rect(screen, (40, 180, 80), start_button)

    start_text = menu_font.render(
        "START",
        True,
        WHITE
    )

    screen.blit(start_text, (440, 550))

    pygame.display.flip()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:

            mouse_pos = event.pos

            # Jellyfish controls
            if pygame.Rect(650, 180, 50, 40).collidepoint(mouse_pos):
                jellyfish_count = max(1, jellyfish_count - 1)

            elif pygame.Rect(720, 180, 50, 40).collidepoint(mouse_pos):
                jellyfish_count += 1

            # Hotspot controls
            elif pygame.Rect(650, 270, 50, 40).collidepoint(mouse_pos):
                hotspot_count = max(1, hotspot_count - 1)

            elif pygame.Rect(720, 270, 50, 40).collidepoint(mouse_pos):
                hotspot_count += 1

            # Temperature controls
            elif pygame.Rect(650, 360, 50, 40).collidepoint(mouse_pos):
                temperature = max(
                    EnvironmentConfig.MIN_TEMPERATURE,
                    temperature - 1
                )

            elif pygame.Rect(720, 360, 50, 40).collidepoint(mouse_pos):
                temperature = min(
                    EnvironmentConfig.MAX_TEMPERATURE,
                    temperature + 1
                )

            # pH controls
            elif pygame.Rect(650, 450, 50, 40).collidepoint(mouse_pos):
                ph = max(
                    EnvironmentConfig.MIN_PH,
                    round(ph - 0.1, 1)
                )

            elif pygame.Rect(720, 450, 50, 40).collidepoint(mouse_pos):
                ph = min(
                    EnvironmentConfig.MAX_PH,
                    round(ph + 0.1, 1)
                )

            # Start simulation
            elif start_button.collidepoint(mouse_pos):

                simulation_started = True
                menu_running = False


# Apply selected environmental conditions
EnvironmentConfig.TEMPERATURE = temperature
EnvironmentConfig.PH = ph

# Create a swarm of 20 jellyfish
jellyfish_swarm = []

for i in range(jellyfish_count):

    x = random.randint(50, WIDTH - 50)
    y = random.randint(120, HEIGHT - 80)

    jellyfish_swarm.append(Jellyfish(x, y))

# Create ocean environment
ocean = Ocean()

# Random object placement
objects = []


def get_random_position(radius):

    x = random.randint(radius + 20, 900 - radius)
    y = random.randint(radius + 20, 500 - radius)

    return x, y


def position_is_valid(x, y, radius):

    for ox, oy, other_radius in objects:

        distance = math.sqrt((x - ox) ** 2 + (y - oy) ** 2)

        if distance < radius + other_radius + 20:
            return False

    return True


def generate_object(object_class, radius):

    for _ in range(10000):

        x, y = get_random_position(radius)

        if position_is_valid(x, y, radius):

            objects.append((x, y, radius))

            return object_class(x, y, radius)

    raise RuntimeError("Unable to place object without overlap")


# Create underwater obstacles
obstacles = []

for _ in range(4):

    radius = random.randint(30, 45)

    obstacles.append(generate_object(Obstacle, radius))



# Create pollution hotspots
pollution_hotspots = []

for _ in range(hotspot_count):

    radius = random.randint(20, 40)

    pollution_hotspots.append(
        generate_object(PollutionHotspot, radius)
    )

# Initialize coverage tracker

coverage_tracker = CoverageTracker(WIDTH, HEIGHT)

# Track pollution detection over time
detection_history = []
detection_time_history = []
last_detection_recorded_time = 0

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

    ocean.draw_waves(screen)

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

     # Record pollution detection history
    elapsed = coverage_tracker.get_elapsed_time()

    if elapsed - last_detection_recorded_time >= 1:

        detection_history.append(detected_count if 'detected_count' in locals() else sum(
            1 for hotspot in pollution_hotspots if hotspot.detected
        ))

        detection_time_history.append(elapsed)

        last_detection_recorded_time = elapsed

    font = pygame.font.Font(None, 28)

    status = font.render(
        f"Pollution Hotspots Detected: {detected_count}/{hotspot_count}",
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

    if detected_count == hotspot_count:
        running = False
plot_coverage(
    coverage_tracker.time_history,
    coverage_tracker.coverage_history,
    detection_time_history,
    detection_history
)

# Close pygame
pygame.quit()
sys.exit()
