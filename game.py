import pygame
import numpy as np
from car import Car

# Initialize Pygame
pygame.init()

# Create the screen and the track
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
track = pygame.Surface((WIDTH, HEIGHT))

# Define the game loop
def game_loop():
    car = Car()
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill((255, 255, 255))  # Fill the screen with white
        track.fill((0, 0, 0))  # Fill the track with black (walls are black)

        # Draw the car on the screen
        car_rect = car.rect
        pygame.draw.rect(screen, (255, 0, 0), car_rect)

        # Get the sensor data and visualize it
        sensors, sensor_info = car.get_sensor_data(car_rect, car.angle)
        for sensor in sensors:
            pygame.draw.line(screen, (0, 255, 0), car_rect.center, sensor[:2])

        # Update the screen
        pygame.display.flip()

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(60)

    pygame.quit()
