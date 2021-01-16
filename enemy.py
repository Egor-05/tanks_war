from random import randint
from find_cell import finder
from random import randint
from actor import Actor
from path_finder import main


class Enemy(Actor):
    def __init__(self, field, ind, walls, width, height, tile_size, player, bullet_group, sprite_group, targets):
        self.spawns = {1: (1 * tile_size, 1 * tile_size),
                       2: (9 * tile_size, 1 * tile_size),
                       3: (5 * tile_size, 1 * tile_size)}
        super().__init__(f'enemy{randint(1, 4)}.png', *self.spawns[randint(1, 3)], 1, 1, ind,
                         walls, width, height, bullet_group, sprite_group, targets)
        self.tile_size = tile_size
        self.player = player
        self.field = field
        self.route = []

    def can_shoot(self):
        player_pos = finder(self.player, self.width, self.height, self.tile_size, self.ind)
        self_pos = finder(self, self.width, self.height, self.tile_size, self.ind)
        if player_pos[0] == self_pos[0] or player_pos[1] == self_pos[1]:
            while 0 < self_pos[0] < self.width and 0 < self_pos[1] < self.height and \
                    self.field[self_pos[1]][self_pos[0]] != '#':
                self_pos = (self_pos[0] + int(self.dir[0]), self_pos[1] + int(self.dir[1]))
                if self_pos == player_pos:

                    self.shoot()
                    return True

    def change_dir(self):
        self.can_shoot()
        self_pos = finder(self, self.width, self.height, self.tile_size, self.ind)
        if self.route == [] or \
                self.route[-1] != finder(self.player, self.width, self.height, self.tile_size, self.ind):
            player_pos = finder(self.player, self.width, self.height, self.tile_size, self.ind)
            self.route = main(self.field, self_pos[::-1], player_pos[::-1])
            try:
                self.dir = (self.route[1][0] - self.route[0][0],
                            self.route[1][1] - self.route[0][1])
            except Exception:
                pass
        print(self.dir)

        if self_pos[0] == self.route[0][0] and \
           self_pos[1] == self.route[0][1]:
            if len(self.route) > 1:
                self.dir = (self.route[1][0] - self.route[0][0],
                            self.route[1][1] - self.route[0][1])
                self.route = self.route[1:]
            else:
                self.dir = (0, 0)




