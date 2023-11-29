import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, image: pygame.Surface) -> None:
        pygame.sprite.Sprite.__init__(self)

        # scale image
        image_scale = 45 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image: pygame.Surface = pygame.transform.scale(
            image, (new_width, new_height)
        )

        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.center = [x, y]
