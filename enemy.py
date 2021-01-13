import pygame
from find_cell import finder
from random import randint
from image_load import load_image
from find_cell import finder
from random import randint


class Enemy(pygame.sprite.Sprite):
    routes = []
    var = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def __init__(self, player, width, height, tile_size, field, group):
        super().__init__(group)
        self.x, self.y = 240, 66  # spawns[randint(1, 3)]
        self.image_name = f'enemy{randint(1, 4)}.png'
        self.image = load_image(self.image_name)
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.vel = 1
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.player = player
        self.field = field
        self.direct = (-1, 0)
        self.turns = []

    def points(self, x, y):
        res = []
        for i in self.var:
            x1 = x + i[0]
            y1 = y + i[1]
            if 0 <= x1 < self.width and 0 <= y1 < self.height:
                if y1 == 3 and x1 == 7:
                    print()
                if self.field[y1][x1] != '#':
                    res.append((x1, y1))
        return res

    def f(self, arr, x='', y=''):
        if x == '' and y == '':
            self.routes.clear()
            x, y = finder(self, self.width, self.height, self.tile_size)
            arr = [(x, y)]
        a = self.points(x, y)
        if (self.end_x, self.end_y) in a:
            self.routes = arr + [(self.end_x, self.end_y)]
            return
        for i in a:
            if i not in arr:
                self.f(arr + [i], i[0], i[1])
                if len(self.routes) > 0:
                    return

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


