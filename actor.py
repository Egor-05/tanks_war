import pygame
from image_load import load_image
from bullet import Bullet
import datetime


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
        self.look_dir = (-1, 0)
        self.prev_dir = self.look_dir
        self.targets = sprite_group
        self.bullet_group = bullet_group
        self.width = width
        self.height = height
        self.dir = (0, 0)
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
        dir_x, dir_y = self.dir
        x = self.x + self.vel * dir_x
        y = self.y + self.vel * dir_y
        rect = self.image.get_rect().move(x, y)
        for i in self.walls:
            if rect.colliderect(i):
                return
        for i in self.targets:
            if rect.colliderect(i) and i != self:
                return
        self.rotate_image()
        self.dir = (dir_x, dir_y)
        if self.dir != (0, 0):
            self.prev_dir = self.look_dir
            self.look_dir = self.dir
        self.x += self.vel * dir_x
        self.y += self.vel * dir_y
        self.rect = self.image.get_rect().move(self.x, self.y)

    def rotate_image(self):
        a = (self.look_dir[0] - self.prev_dir[0], self.look_dir[1] - self.prev_dir[1])
        rot = 0
        if a == (0, 0):
            return
        elif abs(a[0]) == 2 or abs(a[1]) == 2:
            rot = 180
        elif (self.prev_dir == (0, -1) and self.look_dir == (-1, 0) or
              self.prev_dir == (-1, 0) and self.look_dir == (0, 1) or
              self.prev_dir == (0, 1) and self.look_dir == (1, 0) or
              self.prev_dir == (1, 0) and self.look_dir == (0, -1)):
            rot = 90
            self.prev_dir = self.look_dir
        elif (self.prev_dir == (0, -1) and self.look_dir == (1, 0) or
              self.prev_dir == (1, 0) and self.look_dir == (0, 1) or
              self.prev_dir == (0, 1) and self.look_dir == (-1, 0) or
              self.prev_dir == (-1, 0) and self.look_dir == (0, -1)):
            rot = -90
            self.prev_dir = self.look_dir
        # if self.look_dir[0] == 1:
        #     rot = 180
        # elif self.look_dir[1] == 1:
        #     rot = 90
        # elif self.look_dir[1] == -1:
        #     rot = 270
        self.rotate(rot)

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def shoot(self):
        if datetime.datetime.now() - self.last_shoot > datetime.timedelta(seconds=1):
            self.last_shoot = datetime.datetime.now()
            self.bullet_group.add(Bullet(*self.rect.center, *self.look_dir, self.width,
                                         self.height, self.walls, self, self.targets))
            self.shoot_sound.play()
