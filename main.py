import pygame
import os
import sys


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(load_image('bird1.png', -1), (120, 70))
        self.rect = self.image.get_rect()
        self.rect.x = 150
        self.rect.y = 200


class Button(pygame.sprite.Sprite):
    def __init__(self, image, pos, width, height):
        super().__init__()
        self.image = pygame.transform.scale(load_image(image, -1), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.width, self.height = width, height

    def is_checked(self, x, y):
        return (self.rect.x <= x <= self.rect.x + self.width) and (self.rect.y <= y <= self.rect.y + height)


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
    play = False
    all_sprites.empty()
    play_button = Button('play_button.png', (350, 350), 231, 131)
    results_button = Button('results_button.png', (500, 550), 200, 100)
    all_sprites.add(play_button)
    all_sprites.add(results_button)


pygame.init()
pygame.display.set_caption('flappy bird')
width, height = 960, 720
size = width, height
screen = pygame.display.set_mode(size)
running = True
all_sprites = pygame.sprite.Group()
init_start_menu()
V = 20
fps = 60
clock = pygame.time.Clock()
bird = Bird()
all_sprites.add(bird)
bg = load_image('bg.png')
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(bg, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(fps)
