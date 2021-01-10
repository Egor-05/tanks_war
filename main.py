import pygame, sys
from character import Character
from image_load import load_image


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
                                    tile_size * y + 5, tiles_group, tile_size)
    return new_player


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_size * pos_x, tile_size * pos_y)


class Player(Character):
    def __init__(self, sprite_group, pos_x, pos_y, obstacles, tile_size):
        super().__init__(sprite_group, pos_x, pos_y, obstacles, tile_size)

    def move(self, dif_x, dif_y):
        x = self.x + self.velocity * dif_x
        y = self.y + self.velocity * dif_y
        rect = self.image.get_rect().move(x, y)
        for i in walls_group:
            if rect.colliderect(i):
                return
        self.rotate_image(dif_x, dif_y)
        self.x += self.velocity * dif_x
        self.y += self.velocity * dif_y
        self.rect = self.image.get_rect().move(
            self.x, self.y)

    def change_speed(self, direct):
        self.vx = 10 * direct


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
    size = width, height = len(level_tiles('map.txt')) * tile_size, \
                           len([i[0] for i in level_tiles('map.txt')]) * tile_size
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
    level_map = level_tiles('map.txt')

    clock = pygame.time.Clock()
    player = generate_level(load_level('map.txt'))
    # start_screen()
    tiles_group.draw(screen)
    player_group.draw(screen)

    pygame.display.flip()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
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

                    clock.tick(FPS)
                    pygame.display.flip()
                    screen.fill('black')
