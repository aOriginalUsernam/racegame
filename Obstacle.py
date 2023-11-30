from models.Entity import Entity
import pygame
import os


class Obstacle(Entity):
    def __init__(self, x, y, image):
        super().__init__()
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def move(self, speed):
        self.rect.move_ip(0, speed)

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Load obstacle image
obstacle_image = pygame.image.load(os.path.join(os.getcwd(), "image\player.png"))

# Create an instance of Obstacle
obstacle = Obstacle(400, 100, obstacle_image)

    screen.blit(obstacle.image, obstacle.rect.topleft)
