import pygame, sys
from character import Character
from image_load import load_image
from bullet import Bullet
from find_cell import finder
import enemy


FPS = 60


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
                new_player = Character(player_group, x * tile_size, y * tile_size,
                                       ind, width, height, walls_group, bullets_group, targets_group)
    new_player.walls = walls_group
    return new_player


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_size * pos_x + ind, tile_size * pos_y)


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


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры:",
                  "Управление - стрелки, стрельба - пробел.",
                  "Задача игры - выживать в течение определенного количества времени."]

    fon = pygame.transform.scale(load_image('fon.jpeg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    tile_size = 30
    field = 'map1.txt'
    height = len(level_tiles(field)) * tile_size
    width = len([i for i in level_tiles(field)[0]]) * tile_size
    ind = 150
    width += ind * 2

    size = width, height
    fps = 60
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Крест')

    tile_images = {
        'wall': load_image('iron_wall.png'),
        'empty': load_image('iron_road.png')
    }

    player = None
    targets_group = pygame.sprite.Group()
    walls_group = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    bullets_group = pygame.sprite.Group()
    level_map = level_tiles(field)
    enemy_group = pygame.sprite.Group()

    clock = pygame.time.Clock()
    player = generate_level(load_level(field))
    targets_group.add(enemy.Enemy(level_tiles(field), ind, walls_group, width,
                                  height, tile_size, player, bullets_group, enemy_group, targets_group))
    targets_group.add(player)

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
                        player.dir = (-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        player.dir = (1, 0)
                    elif event.key == pygame.K_UP:
                        player.dir = (0, -1)
                    elif event.key == pygame.K_DOWN:
                        player.dir = (0, 1)
                    for i in range(player.hp):
                        hp = pygame.image.load('data/hp.png')
                        hp_rect = hp.get_rect().move(width - ind + 40 * i + 20, 10)
                        screen.blit(hp, hp_rect)
                    tiles_group.draw(screen)
                    player.update()
                    player_group.draw(screen)
                    bullets_group.update()
                    bullets_group.draw(screen)
                    enemy_group.update()
                    enemy_group.draw(screen)

                    clock.tick(FPS)
                    pygame.display.flip()
                    screen.fill('black')
        for i in range(player.hp):
            hp = pygame.image.load('data/hp.png')
            hp_rect = hp.get_rect().move(width - ind + 40 * i + 20, 10)
            screen.blit(hp, hp_rect)
        tiles_group.draw(screen)
        player_group.draw(screen)
        bullets_group.update()
        bullets_group.draw(screen)
        enemy_group.update()
        enemy_group.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
        screen.fill('black')