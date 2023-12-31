import pygame
import os


class Animation(pygame.sprite.Sprite):
    def __init__(self, frames: list[pygame.Surface], x: int = 0, y: int = 0):
        pygame.sprite.Sprite.__init__(self)
        self.frames = frames  # save the images in here
        self.current = 0  # idx of current image of the animation
        self.image = frames[0]  # just to prevent some errors
        self.rect = self.image.get_rect()  # same here
        self.rect.center = [x, y]
        self.playing = False
        self.times_run = 0
        self.play_until = 0

    def update(self, *args):
        if self.playing:  # only update the animation if it is playing
            self.current += 1
            if self.current == len(self.frames):
                self.current = 0
                self.play_until -= 1
                if self.play_until == 0:
                    self.kill()
                    self.playing = False
                    return
            self.image = self.frames[self.current]
            # only needed if size changes within the animation
            self.rect = self.image.get_rect(center=self.rect.center)

    def play(self, count: int = 1):
        self.playing = True
        self.play_until = count
