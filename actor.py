import pygame
from image_load import load_image
from bullet import Bullet
import datetime
from math import sin, cos, degrees


class Actor(pygame.sprite.Sprite):
    def __init__(self, image_name, x, y, vel, hp, ind, walls, width, height, bullet_group, sprite_group):
        super().__init__(sprite_group)
        self.x, self.y = x + ind, y
        self.image_name = image_name
        self.image = load_image(self.image_name)
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.walls = walls
        self.last_shoot = datetime.datetime.now()
        self.ind = ind
        self.vel = vel
        self.targets = sprite_group
        self.bullet_group = bullet_group
        self.width = width
        self.height = height
        self.dir = 0
        self.prev_dir = self.dir
        self.cur_vel = 0
        self.hp = hp
        self.shoot_sound = pygame.mixer.Sound('data/shoot.wav')
        self.exp = False

    def can_shoot(self):
        return False

    def change_dir(self):
        pass

    def update(self):
        if self.hp == 0:
            return
        self.change_dir()
        dir_x = int(cos(self.dir))
        dir_y = int(sin(self.dir))
        x = self.x + self.vel * dir_x
        y = self.y + self.vel * dir_y
        rect = self.image.get_rect().move(x, y)
        for i in self.walls:
            if rect.colliderect(i):
                return
        for i in self.targets:
            if rect.colliderect(i) and i != self:
                return
        self.rotate()
        self.prev_dir = self.dir
        self.x += self.vel * dir_x * self.cur_vel
        self.y += self.vel * dir_y * self.cur_vel
        self.rect = self.image.get_rect().move(self.x, self.y)

    def rotate(self):
        self.image = pygame.transform.rotate(self.image, degrees(self.prev_dir - self.dir))
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def shoot(self):
        if datetime.datetime.now() - self.last_shoot > datetime.timedelta(seconds=1):
            self.last_shoot = datetime.datetime.now()
            self.bullet_group.add(Bullet(*self.rect.center, self.dir, self.width,
                                         self.height, self.walls, self, self.targets))
            self.shoot_sound.play()
