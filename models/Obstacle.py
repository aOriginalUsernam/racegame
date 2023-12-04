from models.entity import Entity
import pygame
import os


class Obstacle(Entity):
    def __init__(self, x: int, y: int, image: pygame.surface) -> None:
        super().__init__(x, y, image)

    def move(
        self,
        entities: pygame.sprite.Group,
        dx: int,
        dy: int,
        animations: pygame.sprite.Group,
    ) -> None:
        collisions: tuple[Entity] = super().move(entities, dx, dy)
        if len(collisions) != 0:
            for collision in collisions:
                if collision != None:
                    collision.explode(animations)
                    break
