import pygame
import os
import sys


class Bird(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, rows, columns, x, y)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect.x = 150
        self.rect.y = 200
        self.iteration = 0

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
    def __init__(self, levels_images):
        super().__init__()
        self.levels_image = levels_images
        self.k_levels = len(levels_images)
        self.level = 0
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

    play = False
    buttons.empty()
    widgets.empty()
    all_sprites.empty()

    bird = Bird(load_image('bird2.png'), 3, 1, int(276 / 3), 64)
    all_sprites.add(bird)

    play_button = Button('play_button.png', (350, 350), 231, 131)
    results_button = Button('results_button.png', (540, 550), 200, 100)
    levels_button = Button('button_level.png', (200, 550), 200, 100)
    buttons.add(play_button)
    buttons.add(levels_button)
    buttons.add(results_button)


def init_levels_menu():
    global btn_left, btn_right, leveldisplay, exit_button
    buttons.empty()
    all_sprites.empty()
    leveldisplay = LevelDisplay(
        (load_image('level_menu1.png'), load_image('level_menu2.png'), load_image('level_menu3.png')))
    widgets.add(leveldisplay)
    btn_left = Button('btn_left.png', (200, 320), 49, 88)
    btn_right = Button('btn_right.png', (710, 320), 49, 88)
    buttons.add(btn_left)
    buttons.add(btn_right)

    exit_button = Button('btn_exit.png', (730, 205), 45, 45)
    buttons.add(exit_button)


pygame.init()
pygame.display.set_caption('flappy bird')
width, height = 960, 720
size = width, height
screen = pygame.display.set_mode(size)
running = True
all_sprites = pygame.sprite.Group()
buttons = pygame.sprite.Group()
# создеём переменные, которые будут ссылаться на кнопки
play_button = None
results_button = None
levels_button = None
btn_left = None
btn_right = None
exit_button = None

widgets = pygame.sprite.Group()
leveldisplay = None

init_start_menu()
V = 5
fps = 60
clock = pygame.time.Clock()
bg = Background('bg.png')

level = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if play_button.is_checked(*event.pos):
                play = True
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
    bg.scrolling(V)
    bird.update()
    screen.blit(bg.image, (bg.x1, 0))
    screen.blit(bg.image, (bg.x2, 0))
    all_sprites.draw(screen)
    widgets.draw(screen)
    buttons.draw(screen)
    pygame.display.flip()
    clock.tick(fps)
