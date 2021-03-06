import pygame
from actor import Actor
from image_load import load_image
from enemy import Enemy
from explosion import AnimatedExplosion
import datetime
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QLineEdit, QLabel
import sqlite3
from math import pi


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.s = 0

    def initUI(self):
        self.setGeometry(220, 110, 220, 110)
        self.setWindowTitle('Фокус со словами')

        self.label = QLabel(self)
        self.label.setText('Введите ваше имя')
        self.label.resize(150, 20)
        self.label.move(50, 10)

        self.btn = QPushButton('Ok', self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(85, 75)
        self.btn.resize(50, 30)
        self.btn.clicked.connect(self.get_user_name)

        self.line = QLineEdit(self)
        self.line.resize(200, 25)
        self.line.move(10, 40)

    def get_user_name(self):
        global user_name
        user_name = self.line.text()
        self.close()


def add_player(user_name, result):
    with sqlite3.connect('users_db.sqlite') as con:
        cur = con.cursor()
        cur.execute("""INSERT INTO users (   
                                          name,
                                          result
                                          )
                                           VALUES (?, ?)""", [user_name, result])
        con.commit()


def end_game(filename):
    all_sprites = pygame.sprite.Group()
    sprite = pygame.sprite.Sprite(all_sprites)
    sprite.image = load_image(filename)
    sprite.rect = sprite.image.get_rect()
    sprite.rect.x = -sprite.rect.w
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        if sprite.rect.x < 0:
            sprite.rect.x += 200 / fps
            all_sprites.draw(screen)
        else:
            show_result()
        pygame.display.flip()
        clock.tick(fps)


def generate_level(level):
    new_player = None
    walls_group = pygame.sprite.Group()
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                walls_group.add(Tile('wall', x, y))
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Actor('character.png', x * tile_size, y * tile_size, 3, 3, ind, walls_group,
                                   width, height, bullets_group, targets_group)
    return new_player, walls_group


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_size * pos_x + ind, tile_size * pos_y)


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
    intro_text = ["ТАНКОВЫЙ БОЙ", "",
                  "Правила игры:",
                  "Управление - стрелки, стрельба - пробел.",
                  "Задача игры - выжить определенное количество времени."]

    fon = pygame.transform.scale(load_image('fon.jpeg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(fps)


def check_win(sec):
    if time_to_live == sec:
        return True


def show_result():
    with sqlite3.connect('users_db.sqlite') as con:
        cur = con.cursor()
        result = cur.execute(f"""SELECT name
                                 FROM users
                                 order by result DESC""").fetchall()
        for i in range(len(result)):
            if result[i][0] == user_name:
                result = i + 1
                break
        font = pygame.font.Font(None, 50)
        text = font.render(f"Ваш номер в списке результатов: {result}", True, (100, 255, 100))
        text_x = width // 2 - text.get_width() // 2
        text_y = height // 2 - text.get_height() // 2
        text_w = text.get_width()
        text_h = text.get_height()
        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                               text_w + 20, text_h + 20), 1)


def print_time(sec):
    font = pygame.font.Font(None, 20)
    text = font.render('Осталось ', True, (255, 255, 255))
    text_x = width - ind + 45
    text_y = 60
    screen.blit(text, (text_x, text_y))
    text = font.render('продержаться:', True, (255, 255, 255))
    text_x = width - ind + 25
    text_y = 80
    screen.blit(text, (text_x, text_y))
    sec = time_to_live - sec
    time = f'{str(sec // 60).rjust(2, "0")}:{str(sec % 60).rjust(2, "0")}'
    font = pygame.font.Font(None, 30)
    text = font.render(time, True, (255, 255, 255))
    text_x = width - ind + 50
    text_y = 100
    screen.blit(text, (text_x, text_y))


if __name__ == '__main__':
    user_name = ''
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec()
    pygame.init()
    time_to_live = 300
    tile_size = 30
    exp_sound = pygame.mixer.Sound('data/expl6.wav')
    exps = []
    field = 'map1.txt'
    height = len(level_tiles(field)) * tile_size
    width = len([i for i in level_tiles(field)[0]]) * tile_size
    ind = 150
    width += ind * 2
    s = 0
    size = width, height
    fps = 30
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Крест')

    tile_images = {
        'wall': load_image('iron_wall.png'),
        'empty': load_image('iron_road.png')
    }

    targets_group = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    bullets_group = pygame.sprite.Group()
    explosion_group = pygame.sprite.Group()
    level_map = level_tiles(field)

    clock = pygame.time.Clock()
    player, walls_group = generate_level(level_map)
    targets_group.add(player)

    KEYS_DEFS = {pygame.K_LEFT: pi,
                 pygame.K_RIGHT: 0,
                 pygame.K_UP: -pi / 2,
                 pygame.K_DOWN: pi / 2
                 }

    start_screen()
    tiles_group.draw(screen)
    targets_group.draw(screen)
    last_spawn = datetime.datetime.now()
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
                elif event.key in KEYS_DEFS.keys():
                    player.cur_vel = 1
                    player.dir = KEYS_DEFS[event.key]
            elif event.type == pygame.KEYUP:
                if event.key in KEYS_DEFS.keys():
                    player.cur_vel = 0
        for i in range(player.hp):
            hp = pygame.image.load('data/hp.png')
            hp_rect = hp.get_rect().move(width - ind + 40 * i + 20, 10)
            screen.blit(hp, hp_rect)
        tiles_group.draw(screen)
        bullets_group.update()
        bullets_group.draw(screen)
        targets_group.update()
        targets_group.draw(screen)
        sec = datetime.timedelta(milliseconds=pygame.time.get_ticks()).seconds
        end = False
        for i in targets_group:
            if i.hp == 0:
                exp_sound.play()
                AnimatedExplosion(load_image('exp.png'), 4, 2, i.rect.center, explosion_group)
                player_killed = i == player
                i.kill()
                if player_killed:
                    for j in range(8):
                        tiles_group.draw(screen)
                        targets_group.draw(screen)
                        explosion_group.update()
                        explosion_group.draw(screen)

                        clock.tick(fps)
                        pygame.display.flip()

                    add_player(user_name, sec)
                    end_game('gameover.png')

        explosion_group.update()
        explosion_group.draw(screen)

        print_time(sec)
        if check_win(sec):
            add_player(user_name, sec)
            end_game('win.jpeg')

        if datetime.datetime.now() - last_spawn > datetime.timedelta(seconds=5):
            last_spawn = datetime.datetime.now()
            targets_group.add(Enemy(level_tiles(field),
                                    ind,
                                    walls_group,
                                    width,
                                    height,
                                    tile_size,
                                    player,
                                    bullets_group,
                                    targets_group))
        clock.tick(fps)
        pygame.display.flip()
        screen.fill('black')

