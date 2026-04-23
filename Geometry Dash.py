from PyQt5.QtWidgets import *
from Results import ReturnResults
import pygame
import os
import sys
import random
import sqlite3
import time


pygame.init()

SIZE = WIDTH, HEIGHT = 800, 500
size = width, height = 500, 500
screen_rect = (0, 0, width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_icon(pygame.image.load("data\\icon.png"))

tile_width = tile_height = 50
all_sprites = pygame.sprite.Group()
platforms_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
obstacle_cactus_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()
light_group = pygame.sprite.Group()
button_group = pygame.sprite.Group()

sound_click = pygame.mixer.Sound('data\\button.wav')
clock = pygame.time.Clock()
FPS = 60
START = 0
PLAY = 1
FAIL = 2
WIN = 3
GRAVITY = 1
MUSIC_START = pygame.mixer.Sound('data\\gala.wav')
MUSIC_END = pygame.mixer.Sound('data\\vivaeve.wav')
MUSIC_LEVEL = pygame.mixer.Sound('data\\music.wav')
MUSIC_CACTUS = pygame.mixer.Sound('data\\music_c.wav')
MUSIC_WIN = pygame.mixer.Sound('data\\rihanna.wav')
MUSIC_C_WIN = pygame.mixer.Sound('data\\cry_baby.wav')


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
        return image


def delete():
    for x in platforms_group.sprites():
        platforms_group.remove(x)
    for x in obstacle_group.sprites():
        obstacle_group.remove(x)
    for x in obstacle_cactus_group.sprites():
        obstacle_cactus_group.remove(x)
    for x in hero_group.sprites():
        hero_group.remove(x)
    for x in light_group.sprites():
        light_group.remove(x)
    for x in button_group.sprites():
        button_group.remove(x)


IMAGE = {'alpaca': load_image('alpaca.png'),
         'light': load_image('light.png'),
         'hero_1': load_image('hero3.png'),
         'hero_2': load_image('hero4.png'),
         'hero_3': load_image('hero5.png'),
         'hero_4': load_image('hero6.png'),
         'hero_5': load_image('hero7.png'),
         'hero_6': load_image('hero8.png'),
         'hero_7': load_image('hero9.png'),
         'hero_8': load_image('hero10.png'),
         'hero_9': load_image('hero11.png'),
         'hero_10': load_image('hero12.png'),
         'hero_11': load_image('hero13.png'),
         'hero_12': load_image('hero14.png'),
         'hero_13': load_image('hero15.png'),
         'hero_14': load_image('hero16.png'),
         'hero_15': load_image('hero17.png'),
         'hero_16': load_image('hero18.png'),
         'hero_17': load_image('hero19.png'),
         'hero_c1': load_image('cactus_1.png'),
         'hero_c2': load_image('cactus_2.png'),
         'hero_c3': load_image('cactus_3.png'),
         'fon_0': load_image('fon7.jpg'),
         'fon_1': load_image('fon5.jpg'),
         'fon_2': load_image('fon6.jpg'),
         'fon_3': load_image('fon9.jpg'),
         'fon_4': load_image('fon10.jpg'),
         'fon_с': load_image('fon2.jpg'),
         'obs_c11': load_image('cactus7.png'),
         'obs_c12': load_image('cactus10.png'),
         'obs_c13': load_image('cactus3.png'),
         'obs_c21': load_image('cactus9.png'),
         'obs_c22': load_image('cactus8.png'),
         'obs_c23': load_image('cactus4.png'),
         'plat_1': load_image('platform3.png'),
         'plat_2': load_image('platform4.png'),
         'plat_3': load_image('platform5.png'),
         'monster_1': load_image('monster1.png'),
         'monster_2': load_image('monster2.png'),
         'cursor_1': load_image('arrow.png'),
         'cursor_2': load_image('arrow_click.png')}


OBSTACLE_C = {'1': IMAGE['obs_c11'],
              '2': IMAGE['obs_c12'],
              '3': IMAGE['obs_c13'],
              '4': IMAGE['obs_c21'],
              '5': IMAGE['obs_c22'],
              '6': IMAGE['obs_c23']}


BUTTONS = {'start': load_image('start.png'),
           'control': load_image('control.png'),
           'leader': load_image('leader.png'),
           'restart': load_image('restart.png'),
           'player': load_image('player.png')}


w_btn = 50
h_btn = 50

now_hero = 'hero_15'


class Hero(pygame.sprite.Sprite):
    def __init__(self, what):
        super().__init__(hero_group)
        self.image = what
        self.not_jump = True
        self.pos_y = 400
        self.rect = self.image.get_rect().move(-50, self.pos_y)

    def do_jump(self, jump, count_jump):
        if self.not_jump:
            if count_jump >= -22:
                self.rect.y -= count_jump / 2.5
                count_jump -= 1
                if len(pygame.sprite.groupcollide(platforms_group, hero_group, False, False)) != 0:
                    jump = False
                    count_jump = 20
                    return jump, count_jump
            else:
                jump = False
                count_jump = 20
        else:
            jump = False
            count_jump = 20
        return jump, count_jump

    def falling(self, jump):
        if len(pygame.sprite.groupcollide(platforms_group, hero_group, False, False)) == 0 \
                and jump is False and self.rect.y != 400:
            if self.rect.y + 7 >= 400:
                self.rect.y = 400
                self.not_jump = True
            else:
                self.rect.y += 7
                self.not_jump = False
                if len(pygame.sprite.groupcollide(platforms_group, hero_group, False, False)) != 0:
                    self.not_jump = True


class CactusHero(pygame.sprite.Sprite):
    def __init__(self, what):
        super().__init__(hero_group)
        self.image = what
        self.rect = self.image.get_rect().move(150, 350)

    def do_jump(self, jump, count_jump):
        if count_jump >= -31:
            self.rect.y -= count_jump / 2
            count_jump -= 1
        else:
            jump = False
            count_jump = 30
        return jump, count_jump


class Button(pygame.sprite.Sprite):
    def __init__(self, what):
        super().__init__(button_group)
        self.image = BUTTONS[what]
        self.status = what
        if what == 'start':
            self.rect = self.image.get_rect().move(50, 100)
        elif what == 'control':
            self.rect = self.image.get_rect().move(50, 200)
        elif what == 'leader':
            self.rect = self.image.get_rect().move(50, 300)
        elif what == 'restart':
            self.rect = self.image.get_rect().move(200, 200)
        self.width = w_btn
        self.height = h_btn

    def status(self):
        return self.status


class Particle(pygame.sprite.Sprite):
    fire = [load_image("star.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position):
    particle_count = 20
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


class Light(pygame.sprite.Sprite):
    move = 5

    def __init__(self, pos_x, pos_y):
        super().__init__(light_group)
        self.image = IMAGE['light']
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.rect_x = -50
        self.score = 0

    def update(self, hero, music):
        if self.rect_x <= self.rect.x:
            self.rect.x -= Light.move
            self.score += 1
        else:
            light_group.remove(self)
        if pygame.sprite.collide_rect(self, hero) == 1:
            pygame.mixer.Sound.stop(music)
            MainWindow().win_screen(self.score)


class Platforms(pygame.sprite.Sprite):
    move = 5

    def __init__(self, what, pos_x, pos_y):
        super().__init__(platforms_group)
        self.image = IMAGE[what]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        if what == 'plat_1':
            self.rect_x = -100
        else:
            self.rect_x = -50
        self.dont_touch = True
        self.score = 0

    def update(self, hero, jump, music):
        if self.rect_x <= self.rect.x:
            self.rect.x -= Platforms.move
            self.score += 1
        else:
            obstacle_cactus_group.remove(self)
        if self.dont_touch:
            if pygame.sprite.collide_rect(self, hero) == 1:
                if self.rect.y - 1 <= hero.rect.y < self.rect.y + 50:
                    if pygame.sprite.collide_mask(self, hero) is not None:
                        pygame.mixer.Sound.stop(music)
                        MainWindow().end_screen(self.score)


class ObstacleLittle(pygame.sprite.Sprite):
    move = 5

    def __init__(self, what, pos_x, pos_y):
        super().__init__(obstacle_group)
        self.image = IMAGE[what]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        if what == 'monster_2':
            self.rect_x = -100
        else:
            self.rect_x = -50
        self.dont_touch = True
        self.score = 0

    def update(self, hero, music):
        if self.rect_x <= self.rect.x:
            self.rect.x -= ObstacleLittle.move
            self.score += 1
        else:
            obstacle_cactus_group.remove(self)
        if self.dont_touch:
            if pygame.sprite.collide_mask(self, hero) is not None:
                pygame.mixer.Sound.stop(music)
                MainWindow().end_screen(self.score)


class ObstacleLittleCactus(pygame.sprite.Sprite):
    c1 = 800, 350
    c2 = 800, 250
    move = 5

    def __init__(self, what):
        super().__init__(obstacle_cactus_group)
        self.image = OBSTACLE_C[what]
        self.dont_touch = True
        self.score = 0

        if 1 <= int(what) <= 3:
            self.x = 82 * int(what)
            self.rect = self.image.get_rect().move(ObstacleLittleCactus.c1)
        else:
            self.x = 82 * (int(what) - 3)
            self.rect = self.image.get_rect().move(ObstacleLittleCactus.c2)

    def update(self, hero, music):
        if -self.x <= self.rect.x:
            self.rect.x -= ObstacleLittleCactus.move
            self.score += 1
        else:
            obstacle_cactus_group.remove(self)
        if self.dont_touch:
            if pygame.sprite.collide_mask(self, hero) is not None:
                pygame.mixer.Sound.stop(music)
                MainWindow().win_c_screen(self.score)


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '1':
                ObstacleLittle('monster_1', x, y)
            elif level[y][x] == '2':
                ObstacleLittle('monster_2', x, y)
            elif level[y][x] == '#':
                Platforms('plat_1', x, y)
            elif level[y][x] == '@':
                Platforms('plat_2', x, y)
            elif level[y][x] == '*':
                Platforms('plat_3', x, y)
            elif level[y][x] == '?':
                Light(x, y)


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def rules():
    text = ["Правила", "",
            "Space - прыгать",
            "Escape - вернуться назад/выйти",
            "При соприкосновении",
            "с препятсвиями герой умирает"]
    fon = pygame.transform.scale(IMAGE['fon_0'], (width, height))
    screen.blit(fon, (0, 0))
    running = True
    img = IMAGE['cursor_1']
    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_focused() == 1:
                    pygame.mouse.set_visible(False)
                    screen.blit(fon, (0, 0))
                    screen.blit(img, event.pos)
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                create_particles(pygame.mouse.get_pos())
                img = IMAGE['cursor_2']
            elif event.type == pygame.MOUSEBUTTONUP:
                img = IMAGE['cursor_1']
        if keys[pygame.K_ESCAPE]:
            MainWindow().start_screen()
        if pygame.mouse.get_focused() == 0:
            screen.blit(fon, (0, 0))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 40)
        text_coord = 50
        for line in text:
            string_rendered = font.render(line, 1, pygame.Color('#FE2810'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 50
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        all_sprites.update()
        all_sprites.draw(screen)
        screen.blit(img, (pygame.mouse.get_pos()))
        pygame.display.flip()
        clock.tick(50)


def first_level():
    delete()

    screen = pygame.display.set_mode(SIZE)
    fon = pygame.transform.scale(IMAGE['fon_1'], SIZE)
    screen.blit(fon, (0, 0))

    field = load_level('map.txt')
    generate_level(field)

    music = MUSIC_LEVEL
    pygame.mixer.Sound.play(music)

    running = True

    jump = False
    count_jump = 20

    start = False
    score = 0
    img = IMAGE['cursor_1']
    flor = load_image('flor.jpg')
    hero = Hero(IMAGE[now_hero])
    hero_group.draw(screen)
    start_time = int(time.time())
    while running:
        keys = pygame.key.get_pressed()
        score += 1

        font = pygame.font.Font(None, 30)
        text = font.render(str(score), 1, pygame.Color('white'))

        t = int(time.time()) - start_time
        m = t // 60
        s = t % 60

        font1 = pygame.font.Font(None, 30)
        text1 = font1.render(f'{m}:{s}', 1, pygame.Color('white'))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_focused() == 1:
                    pygame.mouse.set_visible(False)
                    screen.blit(fon, (0, 0))
                    screen.blit(img, event.pos)
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                create_particles(pygame.mouse.get_pos())
                img = IMAGE['cursor_2']
                jump = True
            elif event.type == pygame.MOUSEBUTTONUP:
                img = IMAGE['cursor_1']
        if keys[pygame.K_SPACE]:
            jump = True
        if jump:
            jump, count_jump = hero.do_jump(jump, count_jump)
        if pygame.mouse.get_focused() == 0:
            screen.blit(fon, (0, 0))
        if keys[pygame.K_ESCAPE]:
            pygame.mixer.Sound.stop(music)
            MainWindow().start_screen()
        if hero.rect.x != 150:
            hero.rect.x += 5
            start = True

        screen.blit(fon, (0, 0))
        screen.blit(flor, (0, 450))
        screen.blit(text, (10, 10))
        screen.blit(text1, (700, 10))
        hero_group.draw(screen)
        hero.falling(jump)
        if start:
            platforms_group.draw(screen)
            platforms_group.update(hero, jump, music)
            obstacle_group.draw(screen)
            obstacle_group.update(hero, music)
            light_group.draw(screen)
            light_group.update(hero, music)
        all_sprites.update()
        all_sprites.draw(screen)
        screen.blit(img, (pygame.mouse.get_pos()))
        pygame.display.update()
        pygame.display.flip()
        clock.tick(FPS)


def timer(start_time):
    t = int(time.time()) - start_time
    s = t % 60
    if s % 10 == 0:
        return True
    return False


def cactus_level():
    delete()

    screen = pygame.display.set_mode(SIZE)
    fon = pygame.transform.scale(IMAGE['fon_с'], SIZE)
    screen.blit(fon, (0, 0))

    music = MUSIC_CACTUS
    pygame.mixer.Sound.play(music)

    obs = ['1']

    jump = False
    count_jump = 30

    running = True

    img = IMAGE['cursor_1']
    tr = load_image('trava.png')
    hero = CactusHero(IMAGE['hero_c1'])
    hero_group.draw(screen)

    ObstacleLittleCactus(random.choice(obs))
    score = 0
    repetition = 0
    start_time = int(time.time())
    while running:
        if timer(start_time) and score % 60 == 0:
            ObstacleLittleCactus.move += 1
        keys = pygame.key.get_pressed()
        score += 1
        font = pygame.font.Font(None, 30)
        text = font.render(str(score), 1, pygame.Color('black'))

        t = int(time.time()) - start_time
        m = t // 60
        s = t % 60

        font1 = pygame.font.Font(None, 30)
        text1 = font1.render(f'{m}:{s}', 1, pygame.Color('black'))

        if len(obstacle_cactus_group.sprites()) == 0:
            ObstacleLittleCactus(random.choice(obs))
        if score % 300 == 0:
            num = score // 300 - 6 * repetition
            if num == 6:
                repetition += 1
            obs.append(str(num))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_focused() == 1:
                    pygame.mouse.set_visible(False)
                    screen.blit(fon, (0, 0))
                    screen.blit(img, event.pos)
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                create_particles(pygame.mouse.get_pos())
                img = IMAGE['cursor_2']
            elif event.type == pygame.MOUSEBUTTONUP:
                img = IMAGE['cursor_1']
        if keys[pygame.K_SPACE]:
            jump = True
        if jump:
            jump, count_jump = hero.do_jump(jump, count_jump)
        if pygame.mouse.get_focused() == 0:
            screen.blit(fon, (0, 0))
        if keys[pygame.K_ESCAPE]:
            pygame.mixer.Sound.stop(music)
            MainWindow().start_screen()
        screen.blit(fon, (0, 0))
        screen.blit(tr, (0, 450))
        screen.blit(text, (10, 10))
        screen.blit(text1, (700, 10))
        hero_group.draw(screen)
        obstacle_cactus_group.draw(screen)
        obstacle_cactus_group.update(hero, music)
        all_sprites.update()
        all_sprites.draw(screen)
        screen.blit(img, (pygame.mouse.get_pos()))
        pygame.display.update()
        pygame.display.flip()
        clock.tick(FPS)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.con = sqlite3.connect("Stats.db")

    def start_screen(self):
        delete()

        pygame.mixer.Sound.stop(MUSIC_START)
        font = pygame.font.Font(None, 40)
        text = font.render("Приветствуем вас в GRAVIS", 1, pygame.Color("#004DFF"))

        screen = pygame.display.set_mode((width, height))
        fon = pygame.transform.scale(IMAGE['fon_0'], (width, height))
        screen.blit(fon, (0, 0))

        img = IMAGE['cursor_1']

        pygame.mixer.Sound.play(MUSIC_START)
        Button('start')
        Button('control')
        Button('leader')
        while True:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    if pygame.mouse.get_focused() == 1:
                        pygame.mouse.set_visible(False)
                        screen.blit(fon, (0, 0))
                        screen.blit(img, event.pos)
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    create_particles(pygame.mouse.get_pos())
                    mouse = pygame.mouse.get_pos()
                    if 50 < mouse[0] < 250 and 100 < mouse[1] < 160:
                        pygame.mixer.Sound.stop(MUSIC_START)
                        first_level()
                    elif 50 < mouse[0] < 250 and 200 < mouse[1] < 260:
                        pygame.mixer.Sound.play(sound_click)
                        rules()
                    elif 50 < mouse[0] < 250 and 300 < mouse[1] < 360:
                        pygame.mixer.Sound.play(sound_click)
                        self.return_results()
            if keys[pygame.K_ESCAPE]:
                terminate()
            if keys[pygame.K_s] and keys[pygame.K_e] and keys[pygame.K_c]:
                pygame.mixer.Sound.stop(MUSIC_START)
                cactus_level()
            if pygame.mouse.get_focused() == 0:
                screen.blit(fon, (0, 0))
            screen.blit(fon, (0, 0))
            all_sprites.update()
            screen.blit(text, (40, 35))
            button_group.draw(screen)
            all_sprites.draw(screen)
            screen.blit(img, (pygame.mouse.get_pos()))
            pygame.display.update()
            pygame.display.flip()
            clock.tick(50)

    def end_screen(self, score):
        delete()

        pygame.mixer.Sound.stop(MUSIC_END)

        font = pygame.font.Font(None, 70)
        text = font.render("Вы проиграли(", 1, pygame.Color('violet'))

        screen = pygame.display.set_mode(size)
        fon = pygame.transform.scale(IMAGE['fon_2'], (width, height))
        screen.blit(fon, (0, 0))
        self.score = score
        self.name = "admin"

        pygame.mixer.Sound.play(MUSIC_END)

        i, okBtnPressed = QInputDialog.getText(self, "Введите имя",
                                               "Как тебя зовут?")
        if okBtnPressed:
            self.name = i
        self.save_results()

        img = IMAGE['cursor_1']
        Button('restart')
        while True:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    if pygame.mouse.get_focused() == 1:
                        pygame.mouse.set_visible(False)
                        screen.blit(fon, (0, 0))
                        screen.blit(img, event.pos)
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    create_particles(pygame.mouse.get_pos())
                    mouse = pygame.mouse.get_pos()
                    if 200 < mouse[0] < 300 and 200 < mouse[1] < 300:
                        pygame.mixer.Sound.stop(MUSIC_END)
                        first_level()
            if keys[pygame.K_ESCAPE]:
                terminate()
            if pygame.mouse.get_focused() == 0:
                screen.blit(fon, (0, 0))
            screen.blit(fon, (0, 0))
            all_sprites.update()
            screen.blit(text, (50, 50))
            button_group.draw(screen)
            all_sprites.draw(screen)
            screen.blit(img, (pygame.mouse.get_pos()))
            pygame.display.update()
            pygame.display.flip()
            clock.tick(50)

    def win_screen(self, score):
        delete()

        pygame.mixer.Sound.stop(MUSIC_WIN)

        font = pygame.font.Font(None, 55)
        text = font.render("Поздравляю с победой!)", 1, pygame.Color('blue'))

        screen = pygame.display.set_mode(size)
        fon = pygame.transform.scale(IMAGE['fon_3'], (width, height))
        screen.blit(fon, (0, 0))
        self.score = score
        self.name = "admin"

        pygame.mixer.Sound.play(MUSIC_WIN)

        i, okBtnPressed = QInputDialog.getText(self, "Введите имя",
                                               "Как тебя зовут?")
        if okBtnPressed:
            self.name = i
        self.save_results()

        img = IMAGE['cursor_1']
        Button('restart')
        while True:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    if pygame.mouse.get_focused() == 1:
                        pygame.mouse.set_visible(False)
                        screen.blit(fon, (0, 0))
                        screen.blit(img, event.pos)
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    create_particles(pygame.mouse.get_pos())
                    mouse = pygame.mouse.get_pos()
                    if 200 < mouse[0] < 300 and 200 < mouse[1] < 300:
                        pygame.mixer.Sound.stop(MUSIC_WIN)
                        first_level()
            if keys[pygame.K_ESCAPE]:
                terminate()
            if pygame.mouse.get_focused() == 0:
                screen.blit(fon, (0, 0))
            screen.blit(fon, (0, 0))
            all_sprites.update()
            screen.blit(text, (10, 50))
            button_group.draw(screen)
            all_sprites.draw(screen)
            screen.blit(img, (pygame.mouse.get_pos()))
            pygame.display.update()
            pygame.display.flip()
            clock.tick(50)

    def win_c_screen(self, score):
        delete()

        pygame.mixer.Sound.stop(MUSIC_C_WIN)

        font = pygame.font.Font(None, 70)
        text = font.render("Попробуйте снова", 1, pygame.Color('violet'))

        screen = pygame.display.set_mode(size)
        fon = pygame.transform.scale(IMAGE['fon_4'], (width, height))
        screen.blit(fon, (0, 0))
        self.score = score
        self.name = "admin"

        pygame.mixer.Sound.play(MUSIC_C_WIN)

        i, okBtnPressed = QInputDialog.getText(self, "Введите имя",
                                               "Как тебя зовут?")
        if okBtnPressed:
            self.name = i
        self.save_results()

        img = IMAGE['cursor_1']
        Button('restart')
        while True:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    if pygame.mouse.get_focused() == 1:
                        pygame.mouse.set_visible(False)
                        screen.blit(fon, (0, 0))
                        screen.blit(img, event.pos)
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    create_particles(pygame.mouse.get_pos())
                    mouse = pygame.mouse.get_pos()
                    if 200 < mouse[0] < 300 and 200 < mouse[1] < 300:
                        pygame.mixer.Sound.stop(MUSIC_C_WIN)
                        cactus_level()
            if keys[pygame.K_ESCAPE]:
                terminate()
            if pygame.mouse.get_focused() == 0:
                screen.blit(fon, (0, 0))
            screen.blit(fon, (0, 0))
            all_sprites.update()
            screen.blit(text, (40, 50))
            button_group.draw(screen)
            all_sprites.draw(screen)
            screen.blit(img, (pygame.mouse.get_pos()))
            pygame.display.update()
            pygame.display.flip()
            clock.tick(50)

    def save_results(self):
        cur = self.con.cursor()
        result = cur.execute("""INSERT INTO Data(Name, Score) VALUES(?, ?)""", (self.name, self.score)).fetchall()
        self.con.commit()

    def return_results(self):
        results = ReturnResults(self).show()


app = QApplication(sys.argv)
window = MainWindow()
window.start_screen()

pygame.quit()

# просто дополнила записку