"""test123"""
import pygame
import os

pygame.init()

screen = pygame.display.set_mode((1280, 720))
carimg = pygame.image.load("img\siep.jpg")
clock = pygame.time.Clock()

pygame.mouse.set_visible(0)

while True:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    # Do logical updates here.
    # ...
    surface = pygame.image.load(os.path.join(os.getcwd(), "img\siep.jpg")).convert()
    screen.fill(
        "purple", screen.blit(surface, (10, 10))
    )  # Fill the display with a solid color

    # Render the graphics here.
    def car(x, y):
        screen.blit(carimg, (0, 0))

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)  # wait until next frame (at 60 FPS)
    car(0, 0)