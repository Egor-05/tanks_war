import pygame
from image_load import load_image
from bullet import Bullet
import datetime


class Actor(pygame.sprite.Sprite):
    def __init__(self, image_name, x, y, vel, hp, ind, walls, width, height, bullet_group, sprite_group, targets):
        super().__init__(sprite_group)
        self.x, self.y = x + ind, y
        self.image_name = image_name
        self.image = load_image(self.image_name)
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.walls = walls
        self.last_shoot = datetime.datetime.now()
        self.ind = ind
        self.vel = vel
        self.targets = targets
        self.bullet_group = bullet_group
        self.width = width
        self.height = height
        self.dir = (-1, 0)
        self.hp = hp

    def update(self):
        if self.can_shoot():
            return
        if self.hp == 0:
            self.kill()
        if 'enemy' in self.image_name:
            self.change_dir()
        dir_x, dir_y = self.dir
        x = self.x + self.vel * dir_x
        y = self.y + self.vel * dir_y
        rect = self.image.get_rect().move(x, y)
        for i in self.walls:
            if rect.colliderect(i):
                return
        self.dir = (dir_x, dir_y)
        self.rotate_image(dir_x, dir_y)
        self.x += self.vel * dir_x
        self.y += self.vel * dir_y
        self.rect = self.image.get_rect().move(
            self.x, self.y)

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
        self.image = pygame.transform.rotate(load_image(self.image_name), angle)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def shoot(self):
        if datetime.datetime.now() - self.last_shoot > datetime.timedelta(seconds=1):
            self.last_shoot = datetime.datetime.now()
            self.bullet_group.add(Bullet(*self.rect.center, *self.dir, self.width, self.height, self.walls, self, self.targets))
