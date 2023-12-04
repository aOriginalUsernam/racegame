import pygame


class button(pygame.sprite.Sprite):
    def __init__(self, font: pygame.font.Font, name: str, x: int, y: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(name, True, "white").convert_alpha()
        self.rect = pygame.Rect(
            x,
            y,
            self.image.get_width() + 10,
            self.image.get_height() + 10,
        )
