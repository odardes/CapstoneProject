import math
import time
import pygame
import config


class Car:

    # The attributes of the car
    def __init__(self, surface, x, y, target, velocity=3, angle=0):
        self.surface = surface
        self.initialY = 0
        self.initialX = 0
        self.x = x
        self.y = y
        self.distance_travelled = 0
        self.target = target
        self.x_velocity = velocity*math.cos(angle)
        self.y_velocity = velocity*math.sin(angle)
        self.angle = angle
        self.prev_angle = 0
        self.img = pygame.transform.scale(
            pygame.image.load(config.image_player_car),
            (200, 100)
        )
        self.smoothing_angle = 0
        self.paths = []
    def reset(self):
        self.x = 0
        self.y = 0
        self.angle = 0
        self.smoothing_angle = 0
        self.distance_travelled = 0
        self.img = pygame.transform.scale(
            pygame.image.load(config.image_player_car),
            (200, 100)
        )
        self.paths = []
        self.smoothing_angle = 0
        self.prev_angle = 0
    # List is created and updated the next speed and calculation of location
    def updateValue(self, newVelocity, newAngle, newTarget):
        # Turns the car as for the new angle
        time.sleep(1)
        self.initialY = self.y
        self.initialX = self.x
        print(math.ceil(self.angle*180/math.pi))
        self.angle = (self.angle + newAngle) % (2*math.pi)
        # Separated by x and y axis geometrically
        rotatedVel = [newVelocity*math.cos(self.angle), newVelocity*math.sin(self.angle)]
        print(f"vx: {self.x_velocity} vy: {self.y_velocity}")

        self.x_velocity = rotatedVel[0]
        self.y_velocity = rotatedVel[1]
        print(self.x_velocity, self.y_velocity)

        self.target = newTarget
        self.distance_travelled = 0

        if newAngle != 0:
            self.img = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(config.image_player_car), (200, 100)), math.ceil(-self.angle * 180 / math.pi))

    def __str__(self):
        return f"Car<target:{self.target}, velocity: {math.sqrt(self.x_velocity**2 + self.y_velocity**2)}, angle: {self.angle}"

    def render(self):
        # pygame.draw.rect(self.surface, (0, 255, 0), (self.x, self.y, self.img.get_width(), self.img.get_height()))
        self.surface.blit(self.img, (self.x, self.y))

    # Takes the hypotenuse of speed
    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity
        self.distance_travelled += math.sqrt(self.x_velocity**2 + self.y_velocity**2)

    def has_reached_target(self):
        return True if self.distance_travelled >= self.target else False
