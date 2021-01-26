import pygame
from math import sin, cos


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dir, width, height, walls, obj, targets):
        super().__init__()
        self.radius = 5
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (self.radius, self.radius), self.radius)
        x -= self.radius
        y -= self.radius
        self.x, self.y = x, y
        self.dir = dir
        self.rect = pygame.Rect(x, y, 2 * self.radius, 2 * self.radius)
        self.vel = 8
        self.obj = obj
        self.targets_group = targets
        self.width = width
        self.height = height
        self.walls = walls

    def update(self):
        self.x += self.vel * cos(self.dir)
        self.y += self.vel * sin(self.dir)
        self.rect = self.rect.move(self.vel * cos(self.dir),
                                   self.vel * sin(self.dir))
        for i in self.targets_group:
            if self.rect.colliderect(i) and i != self.obj:
                i.hp -= 1
                self.kill()
        if 0 > self.x or self.x > self.width or 0 > self.y or self.y > self.height:
            self.kill()

        for i in self.walls:
            if self.rect.colliderect(i):
                self.kill()







