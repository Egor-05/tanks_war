from find_cell import finder
from random import randint
from actor import Actor
from math import atan2, sin, cos


class Enemy(Actor):
    var = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def __init__(self, field, ind, walls, width, height, tile_size, player, bullet_group, targets):
        self.spawns = {1: (1 * tile_size, 1 * tile_size),
                       2: (9 * tile_size, 1 * tile_size),
                       3: (5 * tile_size, 1 * tile_size)}
        super().__init__(f'enemy{randint(1, 4)}.png', *self.spawns[randint(1, 3)], 2, 1, ind,
                         walls, width, height, bullet_group, targets)
        self.tile_size = tile_size
        self.player = player
        self.field = field
        self.field_list = [[j for j in i] for i in self.field]
        self.route = []

    def can_shoot(self):
        player_pos = finder(self.player, self.width, self.height, self.tile_size, self.ind)
        self_pos = finder(self, self.width, self.height, self.tile_size, self.ind)
        if player_pos[0] == self_pos[0] or player_pos[1] == self_pos[1]:
            while 0 < self_pos[0] < self.width and 0 < self_pos[1] < self.height and \
                    self.field[self_pos[1]][self_pos[0]] != '#':
                self_pos = (self_pos[0] + int(cos(self.dir)), self_pos[1] + int(sin(self.dir)))
                if self_pos == player_pos:
                    self.shoot()
                    return True
        return False

    def points(self, x, y, end_x, end_y):
        res = []
        for i in self.var:
            x1 = x + i[0]
            y1 = y + i[1]
            if 0 <= x1 < self.width and 0 <= y1 < self.height:
                if self.field[y1][x1] != '#':
                    res.append((x1, y1))
        return sorted(res, key=lambda e: abs(end_x - e[0]) + abs(end_y - e[1]))

    def f(self, x, y, end_x, end_y, arr):
        a = self.points(x, y, end_x, end_y)
        if (end_x, end_y) in a:
            return arr + [(end_x, end_y)]
        if len(arr) == 5:
            return arr
        for i in a:
            if i not in arr:
                return self.f(i[0], i[1], end_x, end_y, arr + [i])
        return [(x, y)]

    def change_dir(self):
        self.can_shoot()
        self_pos = finder(self, self.width, self.height, self.tile_size, self.ind)
        player_pos = finder(self.player, self.width, self.height, self.tile_size, self.ind)
        a = self.f(*self_pos, *player_pos, [])
        next_point = a[0]
        self.dir = atan2(next_point[1] - self_pos[1], next_point[0] - self_pos[0])
        self.cur_vel = 1
