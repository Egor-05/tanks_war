import pygame
from image_load import load_image


class Character(pygame.sprite.Sprite):
    def __init__(self, sprite_group, pos_x, pos_y, obstacles):
        super().__init__(sprite_group)
        self.image = load_image('character.png')
        self.x, self.y = pos_x, pos_y
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.vel = 2
        self.obstacles = obstacles

    def rotate_image(self, dir_x, dir_y):
        rot = 0
        if dir_x == 1:
            rot = 180
        elif dir_y == 1:
            rot = 90
        elif dir_y == -1:
            rot = 270
        self.rotate(rot)

    def rotate(self, angle):
        self.image = pygame.transform.rotate(load_image('character.png'), angle)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
