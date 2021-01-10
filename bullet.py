import pygame
from image_load import load_image


class Bullet(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image('bullet.png')
        self.rect = self.image.get_rect()



