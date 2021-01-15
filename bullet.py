import pygame
from image_load import load_image


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dir_x, dir_y, width, height, walls):
        super().__init__()
        self.radius = 5
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (self.radius, self.radius), self.radius)
        x -= self.radius
        y -= self.radius
        self.x, self.y = x, y
        self.dir_x, self.dir_y = dir_x, dir_y
        self.rect = pygame.Rect(x, y, 2 * self.radius, 2 * self.radius)
        self.vel = 6
        self.width = width
        self.height = height
        self.walls = walls

    def update(self):
        self.x += self.vel * self.dir_x
        self.y += self.vel * self.dir_y
        if 0 > self.x or self.x > self.width or 0 > self.y or self.y > self.height:
            self.kill()

        for i in self.walls:
            if self.rect.colliderect(i):
                self.kill()
        self.rect = self.rect.move(self.vel * self.dir_x, self.vel * self.dir_y)






