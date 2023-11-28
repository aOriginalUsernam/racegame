"""test123"""
import pygame
import os


pygame.init()

pygame.display.set_mode()
surface = pygame.image.load(os.path.join(os.getcwd(), "img\siep.jpg")).convert()
pygame.Surface.convert(surface)

sample_surface = pygame.display.set_mode((400, 300))
# Choosing red color for the rectangle
color = (255, 255, 0)

# Drawing Rectangle
pygame.draw.rect(sample_surface, color, pygame.Rect(30, 30, 60, 60))

pygame.display.flip()
