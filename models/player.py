from models.Entity import Entity
import pygame
import os


class Player(Entity):
    def __init__(self, x: int, y: int) -> None:
        image = pygame.image.load(os.path.join(os.getcwd(), "image\player.png"))
        self.default_image: pygame.Surface = image.copy()
        self.degree: int = 0
        super().__init__(x, y, image)
        self.default_image: pygame.Surface = self.image.copy()

    def turn(self, degree: int) -> None:
        if degree % 360 == 0 or degree == 0:
            return
        self.degree += degree
        if degree > 0:
            degree = 360 - degree
        self.image = pygame.transform.rotate(self.default_image, degree)
