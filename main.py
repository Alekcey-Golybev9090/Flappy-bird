import pygame
import os
import sys


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(load_image('bird1.png'), (85, 60))
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 300


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


pygame.init()
pygame.display.set_caption('flappy bird')
width, height = 960, 720
size = width, height
screen = pygame.display.set_mode(size)
running = True
V = 20
fps = 60
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
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
