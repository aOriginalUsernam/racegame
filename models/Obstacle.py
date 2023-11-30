from models.Entity import Entity
import pygame
import os


class Obstacle(Entity):
    def __init__(self, x: int, y: int) -> None:
        image: pygame.Surface = pygame.image.load(os.path.join(os.getcwd(), "image\enemy car.jpg"))
        pygame.transform.rotate(image, 180)
        super().__init__(x, y, image)
