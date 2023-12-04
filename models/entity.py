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
        self.to_busy_exploding = False
        self.explode_animation = self.load_animation()

    """
moves entity based on dx and dy, and returns all entities it colides with.
    """

    def move(self, entities: pygame.sprite.Group, dx: int = 0, dy: int = 0) -> tuple:
        # Move each axis separately. check for collision both times.
        to_return: list = []
        if not self.to_busy_exploding:
            if dx != 0:
                to_return.append(self.__move_single_axis__(entities.sprites(), dx, 0))
            if dy != 0:
                to_return.append(self.__move_single_axis__(entities.sprites(), 0, dy))
        return tuple(to_return)

    def __move_single_axis__(
        self, entities: list, dx: int = 0, dy: int = 0
    ) -> pygame.sprite.Sprite | None:
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        to_return = None

        # If you collide with another entity, move out based on velocity
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

    def load_animation(self) -> Animation:
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
        return Animation(boomframes)

    def explode(self, animations: pygame.sprite.Group) -> None:
        self.to_busy_exploding = True

        # set x + y of animation
        self.explode_animation.rect.centerx = self.rect.centerx - 50
        self.explode_animation.rect.centery = self.rect.centery - 80

        # play animation & sound
        self.explode_animation.play()
        animations.add(self.explode_animation)
        kaboom = pygame.mixer.Sound(os.path.join(os.getcwd(), "data\sounds\kaboom.wav"))
        pygame.mixer.Sound.play(kaboom)

        # oof self
        self.kill()
