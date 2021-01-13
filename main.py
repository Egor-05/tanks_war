import pygame, sys
from character import Character
from image_load import load_image
from bullet import Bullet
from find_cell import finder
import enemy


class Enemy(enemy.Enemy):
    def __init__(self, player, width, height, tile_size, field, group):
        super().__init__(player, width, height, tile_size, field, group)

    def update(self):
        if self.routes == [] or \
                self.routes[-1] != finder(self.player, self.width, self.height, self.tile_size):
            self.end_x, self.end_y = finder(self.player, self.width, self.height, self.tile_size)
            self.f([])
            direct = (self.routes[1][0] - self.routes[0][0],
                      self.routes[1][1] - self.routes[0][1])
            prev_value = self.routes[1]
            self.turns.clear()
            for i in self.routes[2:]:
                a = (i[0] - prev_value[0], i[1] - prev_value[1])
                if a != direct:
                    self.turns.append((direct, prev_value))
                    direct = a
                prev_value = i
            self.turns.append((direct, self.routes[-1]))
            self.direct = self.turns[0][0]
            print(self.turns)
        player_pos = finder(self.player, width, height, tile_size)
        self_pos = finder(self, width, height, tile_size)
        if player_pos[0] == self_pos[0] or player_pos[1] == self_pos[1]:
            s = (abs(player_pos[0] - self_pos[0]), abs(player_pos[1] - self_pos[1]))
            while 0 < s[0] < width and 0 < s[1] < height and self.field[s[1]][s[0]] != '#':
                s = (s[0] + int(self.direct[0]), s[1] + int(self.direct[1]))
                if s == player_pos:
                    bullets_group.add(Shot(*self.rect.center, *self.direct))
                    break
        if self.rect.centerx == (self.turns[0][1][0] * tile_size + tile_size // 2) and \
           self.rect.centery == (self.turns[0][1][1] * tile_size + tile_size // 2):
            if len(self.turns) > 1:
                self.turns = self.turns[1:]
                self.direct = [str(i) for i in self.turns[0][0]]
            else:
                self.direct = (0, 0)
        self.x += self.vel * int(self.direct[0])
        self.y += self.vel * int(self.direct[1])
        self.rect = self.image.get_rect().move(
            self.x, self.y)


FPS = 60
WIDTH = HEIGHT = 500


def generate_level(level):
    new_player, player_x, player_y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                walls_group.add(Tile('wall', x, y))
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(player_group, tile_size * x,
                                    tile_size * y + 5, tiles_group)
    return new_player


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_size * pos_x, tile_size * pos_y)


class Player(Character):
    def __init__(self, sprite_group, pos_x, pos_y, obstacles):
        super().__init__(sprite_group, pos_x, pos_y, obstacles)
        self.dir = (-1, 0)

    def move(self, dir_x, dir_y):
        x = self.x + self.vel * dir_x
        y = self.y + self.vel * dir_y
        rect = self.image.get_rect().move(x, y)
        for i in walls_group:
            if rect.colliderect(i):
                return
        self.dir = (dir_x, dir_y)
        self.rotate_image(dir_x, dir_y)
        self.x += self.vel * dir_x
        self.y += self.vel * dir_y
        self.rect = self.image.get_rect().move(
            self.x, self.y)

    def change_speed(self, direct):
        self.vx = 10 * direct

    def shoot(self):
        bullets_group.add(Shot(*self.rect.center, *self.dir))


class Shot(Bullet):
    def __init__(self, x, y, dir_x, dir_y):
        super().__init__(x, y, dir_x, dir_y)
        self.width = width
        self.height = height

    def update(self):
        self.x += self.vel * self.dir_x
        self.y += self.vel * self.dir_y
        if 0 > self.x or self.x > self.width or 0 > self.y or self.y > self.height:
            self.kill()

        for i in walls_group:
            if self.rect.colliderect(i):
                self.kill()
        self.rect = self.rect.move(self.vel * self.dir_x, self.vel * self.dir_y)


def terminate():
    pygame.quit()
    sys.exit()


def level_tiles(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map


def load_level(filename):
    level_map = level_tiles(filename)
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))
#
#
# def start_screen():
#     intro_text = ["ЗАСТАВКА", "",
#                   "Правила игры",
#                   "Если в правилах несколько строк,",
#                   "приходится выводить их построчно"]
#
#     fon = pygame.transform.scale(load_image('fon.jpeg'), (WIDTH, HEIGHT))
#     screen.blit(fon, (0, 0))
#     font = pygame.font.Font(None, 30)
#     text_coord = 50
#     for line in intro_text:
#         string_rendered = font.render(line, True, pygame.Color('black'))
#         intro_rect = string_rendered.get_rect()
#         text_coord += 10
#         intro_rect.top = text_coord
#         intro_rect.x = 10
#         text_coord += intro_rect.height
#         screen.blit(string_rendered, intro_rect)
#
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 terminate()
#             elif event.type == pygame.KEYDOWN or \
#                     event.type == pygame.MOUSEBUTTONDOWN:
#                 return  # начинаем игру
#         pygame.display.flip()
#         clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    tile_size = 30
    field = 'map.txt'
    size = width, height = (len(level_tiles(field)) * tile_size,
                            len([i[0] for i in level_tiles(field)]) * tile_size)

    fps = 60
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Крест')

    tile_images = {
        'wall': load_image('iron_wall.png'),
        'empty': load_image('iron_road.png')
    }

    player = None
    walls_group = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    bullets_group = pygame.sprite.Group()
    level_map = level_tiles(field)
    enemy_group = pygame.sprite.Group()

    clock = pygame.time.Clock()
    player = generate_level(load_level(field))
    enemy = Enemy(player, width, height, tile_size, level_tiles(field), enemy_group)
    # start_screen()
    tiles_group.draw(screen)
    player_group.draw(screen)

    pygame.display.flip()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
                    break
                c = True
                while c:
                    for i in pygame.event.get():
                        if i.type == pygame.QUIT:
                            pygame.quit()
                        if i.type == pygame.KEYUP:
                            c = False
                    if event.key == pygame.K_LEFT:
                        player.move(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        player.move(1, 0)
                    elif event.key == pygame.K_UP:
                        player.move(0, -1)
                    elif event.key == pygame.K_DOWN:
                        player.move(0, 1)
                    tiles_group.draw(screen)
                    player_group.draw(screen)
                    bullets_group.update()
                    bullets_group.draw(screen)
                    enemy_group.update()
                    enemy_group.draw(screen)

                    clock.tick(FPS)
                    pygame.display.flip()
                    screen.fill('black')
        tiles_group.draw(screen)
        player_group.draw(screen)
        bullets_group.update()
        bullets_group.draw(screen)
        enemy_group.update()
        enemy_group.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()