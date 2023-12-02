import pygame
import os
from models.Animation import Animation


class Entity(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, image: pygame.Surface, scale: int = 100) -> None:
        pygame.sprite.Sprite.__init__(self)

        # scale image
        image_scale = scale / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image: pygame.Surface = pygame.transform.scale(
            image, (new_width, new_height)
        )

        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.center = [x, y]

    """
moves entity based on dx and dy, and returns all entities it colides with.
    """

    def move(self, entities: pygame.sprite.Group, dx: int = 0, dy: int = 0) -> tuple:
        # Move each axis separately. check for collision both times.
        to_return: list = []
        if dx != 0:
            to_return.append(self.move_single_axis(entities.sprites(), dx, 0))
        if dy != 0:
            to_return.append(self.move_single_axis(entities.sprites(), 0, dy))
        return to_return

    def move_single_axis(
        self, entities: list, dx: int = 0, dy: int = 0
    ) -> pygame.sprite.Sprite | None:
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        to_return = None

        # If you collide with a wall, move out based on velocity
        for entity in entities:
            if self.rect.colliderect(entity.rect):
                to_return = entity
                if dx > 0:  # if Moving right; Hit the left side of the entity
                    self.rect.right = entity.rect.left
                if dx < 0:  # if Moving left; Hit the right side of the entity
                    self.rect.left = entity.rect.right
                if dy > 0:  # if Moving down; Hit the top side of the entity
                    self.rect.bottom = entity.rect.top
                if dy < 0:  # if Moving up; Hit the bottom side of the entity
                    self.rect.top = entity.rect.bottom
        return to_return

    def explode(self) -> Animation:
        boomframes: list[pygame.Surface] = []
        for i in range(0, 26):
            str_i = str(i)
            if len(str_i) == 1:
                str_i = f"0{str_i}"
            boomframes.append(
                pygame.image.load(
                    os.path.join(
                        os.getcwd(), f"image\\explosion\\frame_{str_i}_delay-0.1s.png"
                    )
                )
            )
        nuke = Animation(boomframes)
        nuke.play(100)
        return nuke
