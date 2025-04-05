import pygame
import math

class Car:
    def __init__(self, track):
        self.track = track  # Track (road) surface to be used for sensor data
        self.width = 50
        self.height = 90
        self.x = 400  # Starting X position of the car
        self.y = 300  # Starting Y position of the car
        self.angle = 0  # Initial angle of the car (0 degrees)
        self.speed = 0
        self.max_speed = 10
        self.acceleration = 0.2
        self.deceleration = 0.05
        self.car_color = (0, 0, 255)  # Blue color for the car
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.car_color)  # Filling car with blue color

    def move(self):
        """Update car's position based on speed and angle."""
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))
        self.rect.center = (self.x, self.y)

    def update(self):
        """Handle car movement based on user input or AI controls."""
        # Adjust speed based on the user input or AI decision
        if self.speed < self.max_speed:
            self.speed += self.acceleration
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        if self.speed > 0:
            self.speed -= self.deceleration
        self.move()

    def rotate(self, angle_change):
        """Rotate the car around its center."""
        self.angle += angle_change
        self.angle = self.angle % 360  # Keep the angle between 0 and 360 degrees

    def get_sensor_data(self, car_rect, car_angle):
        """
        Returns the sensor data of the car, which includes the distance
        to the objects (road boundaries or obstacles) around the car.
        """
        sensors = []
        sensor_info = []

        # Place sensors at 8 different angles around the car (360 degrees)
        for sensor in range(8):
            # Calculate the sensor's position based on the car's position and angle
            sensor_x = int(car_rect.centerx + 100 * math.cos(math.radians(car_angle + (sensor * 45))))
            sensor_y = int(car_rect.centery + 100 * math.sin(math.radians(car_angle + (sensor * 45))))

            # Get the pixel color at the sensor's position on the track (the road)
            try:
                pixel = self.track.get_at((sensor_x, sensor_y))
                # If pixel is non-white (indicating an obstacle or boundary)
                if pixel != (255, 255, 255):  # Assume white is the road
                    sensors.append(255)  # Close object
                else:
                    sensors.append(0)  # Clear road
            except IndexError:
                # If the sensor goes out of bounds, treat it as an obstacle
                sensors.append(255)  # Out of bounds, treat as close obstacle

            sensor_info.append((sensor_x, sensor_y))

        return sensors, sensor_info

    def draw(self, screen):
        """Draw the car onto the screen."""
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, new_rect.topleft)
