import pygame
from image_load import load_image


class Destroyer(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image('destroyer.png')
        self.rect = self.image.get_rect()
        self.damage = 10
        self.hp = 100
        self.vel = 10