import pygame
from random import randint
from find_cell import finder
from random import randint
from actor import Actor
from bullet import Bullet
import datetime


class Enemy(Actor):
    routes = []
    var = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def __init__(self, field, walls, width, height, tile_size, player, bullet_group, sprite_group):
        super().__init__(f'enemy{randint(1, 4)}.png', 240, 66, 1, 1, walls, width, height, bullet_group, sprite_group)
        self.x, self.y = 240, 66  # spawns[randint(1, 3)]
        self.tile_size = tile_size
        self.player = player
        self.field = field
        self.last_shoot = datetime.datetime.now()

    def points(self, x, y):
        res = []
        for i in self.var:
            x1 = x + i[0]
            y1 = y + i[1]
            if 0 <= x1 < self.width and 0 <= y1 < self.height:
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

    def can_shoot(self):
        player_pos = finder(self.player, self.width, self.height, self.tile_size)
        self_pos = finder(self, self.width, self.height, self.tile_size)
        if player_pos[0] == self_pos[0] or player_pos[1] == self_pos[1]:
            while 0 < self_pos[0] < self.width and 0 < self_pos[1] < self.height and \
                    self.field[self_pos[1]][self_pos[0]] != '#':
                self_pos = (self_pos[0] + int(self.dir[0]), self_pos[1] + int(self.dir[1]))
                if self_pos == player_pos and datetime.datetime.now() - self.last_shoot > datetime.timedelta(seconds=1):
                    self.last_shoot = datetime.datetime.now()
                    self.shoot()
                    break

    def change_dir(self):
        self.can_shoot()
        self_pos = finder(self.player, self.width, self.height, self.tile_size)
        player_pos = finder(self, self.width, self.height, self.tile_size)
        diff_x, diff_y = abs(player_pos[0] - self_pos[0]), abs(player_pos[1] - self_pos[1])
        if diff_y == diff_x == 0:
            self.dir = (0, 0)
        elif diff_x < diff_y:
            self.dir = (0, (self_pos[1] - player_pos[1]) // diff_y)
        elif diff_x >= diff_y:
            self.dir = ((self_pos[0] - player_pos[0]) / diff_x, 0)




