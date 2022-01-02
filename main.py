import pygame
import os
import sys
from random import randrange, choice


class Bird(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__()
        self.frames = []
        self.cut_sheet(sheet, rows, columns, x, y)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.to_start_pos()
        self.iteration = 0
        self.mask = pygame.mask.from_surface(self.image)

    def cut_sheet(self, sheet, rows, columns, x, y):
        self.rect = pygame.Rect(0, 0, x, y)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if not self.iteration:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        self.iteration = (self.iteration + 1) % 9

    def to_start_pos(self):
        self.rect.x = 150
        self.rect.y = 200


class Boost(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        image = choice(('up.jpg', 'down.jpg'))
        self.image = pygame.transform.scale(load_image(image, -1), (95, 50))
        self.rect = self.image.get_rect()
        self.rect.x = 810
        self.rect.y = randrange(50, 600)
        self.is_up = image == 'up.jpg'
        self.mask = pygame.mask.from_surface(self.image)

    def is_on_screen(self):
        return -150 <= self.rect.x

    def update(self):
        if not self.is_on_screen():
            boosts.remove(self)
        else:
            self.rect.x -= V


class Pipe(pygame.sprite.Sprite):
    def __init__(self, height, is_down):
        super().__init__()
        self.image = load_image('pipe.png', (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = 810
        if not is_down:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.y = -self.rect.height + height
        else:
            self.rect.y = 632 - height
        self.mask = pygame.mask.from_surface(self.image)

    def is_on_screen(self):
        return -150 <= self.rect.x

    def update(self):
        if not self.is_on_screen():
            obstacles.remove(self)
        else:
            self.rect.x -= V

    def is_behind_bird(self):
        if self.rect.x < int(276 / 3) - 70:
            return True
        return False


class Button(pygame.sprite.Sprite):
    def __init__(self, image, pos, width, height):
        super().__init__()
        self.image = pygame.transform.scale(load_image(image, -1), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.width, self.height = width, height

    def is_checked(self, x, y):
        return self.rect.x <= x <= self.rect.x + self.width and self.rect.y <= y <= self.rect.y + self.height


class Background(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = load_image(image)
        self.width = self.image.get_rect().width
        self.x1 = 0
        self.x2 = self.width

    def scrolling(self, V):
        self.x1 = 0 if self.x1 - V < -self.width else self.x1 - V
        self.x2 = self.width if self.x2 - V < 0 else self.x2 - V


class LevelDisplay(pygame.sprite.Sprite):
    def __init__(self, levels_images, level):
        super().__init__()
        self.levels_image = levels_images
        self.k_levels = len(levels_images)
        self.level = level - 1
        self.update_image()
        self.rect = self.image.get_rect()
        self.rect.x = 180
        self.rect.y = 200

    def update_image(self):
        self.image = self.levels_image[self.level]

    def next(self):
        self.level = (self.level + 1) % self.k_levels
        self.update_image()

    def previous(self):
        self.level = (self.level - 1) if self.level - 1 > -1 else self.k_levels - 1
        self.update_image()

    def get_level(self):
        return self.level + 1


class RecordsDisplay(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('display.png', -1)
        self.rect = self.image.get_rect()
        self.rect.x = 180
        self.rect.y = 200

    def draw(self):
        font = pygame.font.Font('data/Flappy-Bird.ttf', 70)
        text = font.render(f"best for level 1: {records[0]}", False, (255, 139, 85))
        screen.blit(text, (200, 220))
        text = font.render(f"best for level 2: {records[1]}", False, (255, 139, 85))
        screen.blit(text, (200, 325))
        text = font.render(f"best for level 3: {records[2]}", False, (255, 139, 85))
        screen.blit(text, (200, 430))


class ScoreDisplay(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('display.png', -1)
        self.rect = self.image.get_rect()
        self.rect.x = 180
        self.rect.y = 200

    def draw(self):
        font = pygame.font.Font('data/Flappy-Bird.ttf', 70)
        text = font.render(f"SCORE: {int(score)}", False, (255, 139, 85))
        screen.blit(text, (350, 300))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def init_start_menu():
    global play_button, levels_button, results_button, bird

    buttons.empty()
    widgets.empty()
    birds.empty()
    reset_variables()

    bird.to_start_pos()
    birds.add(bird)

    play_button = Button('play_button.png', (350, 350), 231, 131)
    results_button = Button('results_button.png', (540, 550), 200, 100)
    levels_button = Button('button_level.png', (200, 550), 200, 100)
    buttons.add(play_button)
    buttons.add(levels_button)
    buttons.add(results_button)


def init_levels_menu():
    global btn_left, btn_right, leveldisplay, exit_button
    buttons.empty()
    birds.empty()
    reset_variables()
    leveldisplay = LevelDisplay(
        (load_image('level_menu1.png', -1), load_image('level_menu2.png', -1), load_image('level_menu3.png', -1)),
        level)
    widgets.add(leveldisplay)
    btn_left = Button('btn_left.png', (200, 320), 49, 88)
    btn_right = Button('btn_right.png', (710, 320), 49, 88)
    buttons.add(btn_left)
    buttons.add(btn_right)

    exit_button = Button('btn_exit.png', (730, 205), 45, 45)
    buttons.add(exit_button)


def init_results():
    global exit_button, recordsdisplay
    buttons.empty()
    widgets.empty()
    birds.empty()
    reset_variables()
    recordsdisplay = RecordsDisplay()
    widgets.add(recordsdisplay)
    exit_button = Button('btn_exit.png', (730, 205), 45, 45)
    buttons.add(exit_button)


def reset_variables():
    global play_button, results_button, levels_button, btn_left, btn_right, exit_button, leveldisplay, recordsdisplay, scoredisplay
    play_button = None
    results_button = None
    levels_button = None
    btn_left = None
    btn_right = None
    exit_button = None

    leveldisplay = None
    recordsdisplay = None
    scoredisplay = None


def start_game():
    global Uy, g, score
    reset_variables()
    buttons.empty()
    widgets.empty()
    birds.empty()
    score = 0
    bird.to_start_pos()
    birds.add(bird)
    g = 0.5  # ускорение свободного падения
    Uy = 0  # скорость по оси y


def is_living():
    if not 0 <= bird.rect.y <= 561:
        return False
    for i in obstacles:
        if pygame.sprite.collide_mask(bird, i):
            return False
    return True


def add_pipes():
    dist = 250 if level < 3 else 200
    h1 = randrange(50, 410)  # определяет высоту верхней трубы
    h2 = 652 - dist - h1
    obstacles.add(Pipe(h1, False))
    obstacles.add(Pipe(h2, True))


def add_boost():
    boosts.add(Boost())


def end_game():
    global scoredisplay, exit_button, play_button
    birds.empty()
    obstacles.empty()
    boosts.empty()
    reset_variables()
    scoredisplay = ScoreDisplay()
    update_score()
    exit_button = Button('btn_exit.png', (730, 205), 45, 45)
    play_button = Button('play_button.png', (350, 520), 231, 131)
    widgets.add(scoredisplay)
    buttons.add(exit_button)
    buttons.add(play_button)


def draw_score():
    font = pygame.font.Font('data/Flappy-Bird.ttf', 70)
    text = font.render(f"{int(score)}", False, (255, 255, 255))
    screen.blit(text, (450, 20))


def update_score():
    f = open('data/records.txt', 'w')
    records[level - 1] = str(max(int(records[level - 1]), int(score)))
    f.write('\n'.join(records))
    f.close()


pygame.init()
pygame.display.set_caption('flappy bird')
width, height = 960, 720
size = width, height
screen = pygame.display.set_mode(size)
running = True

bird = Bird(load_image('bird2.png'), 3, 1, int(276 / 3), 64)
birds = pygame.sprite.Group()
buttons = pygame.sprite.Group()
widgets = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
boosts = pygame.sprite.Group()

reset_variables()
init_start_menu()

V = 5
fps = 60
play = False
level = 1
clock = pygame.time.Clock()
bg = Background('bg.png')

NEWPIPE = pygame.USEREVENT + 1
pygame.time.set_timer(NEWPIPE, 1500)
UPDATESCORE = pygame.USEREVENT + 2
pygame.time.set_timer(UPDATESCORE, 500)
NEWBOOST = pygame.USEREVENT + 3
pygame.time.set_timer(NEWBOOST, 5229)

records = [i.strip() for i in open('data/records.txt').readlines()]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not play:
                if play_button is not None and play_button.is_checked(*event.pos):
                    play = True
                    start_game()
                if levels_button is not None and levels_button.is_checked(*event.pos):
                    init_levels_menu()
                if btn_left is not None and btn_left.is_checked(*event.pos):
                    leveldisplay.previous()
                    level = leveldisplay.get_level()
                if btn_right is not None and btn_right.is_checked(*event.pos):
                    leveldisplay.next()
                    level = leveldisplay.get_level()
                if exit_button is not None and exit_button.is_checked(*event.pos):
                    init_start_menu()
                if results_button is not None and results_button.is_checked(*event.pos):
                    init_results()
            else:
                Uy = -10  # движение вверх
        if play:
            if event.type == NEWPIPE:
                add_pipes()
            if event.type == NEWBOOST and level > 1:
                add_boost()
            if event.type == UPDATESCORE:
                for i in obstacles:
                    score += 0.5 * int(i.is_behind_bird())
    screen.blit(bg.image, (bg.x1, 0))
    screen.blit(bg.image, (bg.x2, 0))
    birds.draw(screen)
    boosts.draw(screen)
    obstacles.draw(screen)
    widgets.draw(screen)
    buttons.draw(screen)
    if recordsdisplay is not None:
        recordsdisplay.draw()
    if scoredisplay is not None:
        scoredisplay.draw()
    if play:
        Uy += g
        bird.rect.y += Uy
        for i in boosts:
            if pygame.sprite.collide_mask(bird, i):
                bird.rect.y += 10 * (-1) ** int(i.is_up)
        if not is_living():
            play = False
            end_game()
        draw_score()
    bg.scrolling(V)
    bird.update()
    for i in obstacles:
        i.update()
    for i in boosts:
        i.update()
    pygame.display.flip()
    clock.tick(fps)
