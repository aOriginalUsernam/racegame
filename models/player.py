from models.Entity import Entity
import pygame
import os


class Player(Entity):
    def __init__(self, x: int, y: int) -> None:
        image = pygame.image.load(os.path.join(os.getcwd(), "image\player.png"))
        self.degree: int = 0
        super().__init__(x, y, image)
