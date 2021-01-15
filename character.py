import pygame
from image_load import load_image
from actor import Actor
from bullet import Bullet


class Character(Actor):
    def __init__(self, sprite_group, pos_x, pos_y, width, height, obstacles, bullet_group):
        super().__init__('character.png', pos_x, pos_y, 2, 3, obstacles, width, height, bullet_group, sprite_group)
        self.image = load_image('character.png')

    def change_speed(self, direct):
        self.vx = 10 * direct


