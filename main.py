import pygame
from pygame.locals import *
import random
JANELA_LARGURA = 400
JANELA_ALTURA = 800
SPEED = 10
GRAVITY = 1
GAME_SPEED = 10

GROUND_WIDTH = 2 * JANELA_LARGURA
GROUND_HEIGHT = 100

PIPE_WIDTH = 120
PIPE_HEIGHT = 500
PIPE_GAP = 200
class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('bluebird-upflap.png').convert_alpha(),
                        pygame.image.load('bluebird-midflap.png').convert_alpha(),
                        pygame.image.load('bluebird-downflap.png').convert_alpha()]

        self.speed = SPEED  # velocidade do bird

        self.current_image = 0  # img now

        self.image = pygame.image.load('bluebird-upflap.png').convert_alpha() #força a usar a area do png
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = JANELA_LARGURA / 2.2
        self.rect[1] = JANELA_ALTURA / 2  # MANEIRA DE POSICIONAR NO MEIO DA TELA.

    def update(self):
        self.current_image = (self.current_image + 1) % 3  #quando virar img 3 ele volta pra 0
        self.image = self.images[self.current_image]

        self.speed += GRAVITY

        # Update de Height
        self.rect[1] += self.speed

    def bump(self): #pulo
        self.speed = - SPEED

class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('pipe.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True) #inverter o cano pra cima
            self.rect[1] = -(self.rect[3] - ysize)
        else:
            self.rect[1] = JANELA_ALTURA - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED

class Ground(pygame.sprite.Sprite):

    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('ground.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))
        self.mask = pygame.mask.from_surface(self.image)


        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = JANELA_ALTURA - GROUND_HEIGHT
    def update(self):
        self.rect[0] -= GAME_SPEED

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2]) # verifica se o chão ta fora da tela

def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, JANELA_ALTURA - size - PIPE_GAP)
    return (pipe, pipe_inverted)

pygame.init()

screen = pygame.display.set_mode((JANELA_LARGURA, JANELA_ALTURA))

pygame.display.set_caption("brenoloa")

BACKGROUND = pygame.image.load('background.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (JANELA_LARGURA, JANELA_ALTURA))

bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(GROUND_WIDTH * i)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
for i in range(2):
    pipes = get_random_pipes(JANELA_LARGURA * i + 600)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])

clock = pygame.time.Clock()
# looping principal.
while True:
    clock.tick(30) #fps
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                bird.bump()

    screen.blit(BACKGROUND, (0, 0))

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(GROUND_WIDTH - 20)
        ground_group.add(new_ground)

    if is_off_screen(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])
    
        pipes = get_random_pipes(JANELA_LARGURA * 2)

        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

    bird_group.update()
    ground_group.update()
    pipe_group.update()

    bird_group.draw(screen)
    ground_group.draw(screen)
    pipe_group.draw(screen)

    pygame.display.update()
    if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
        pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):

        # GAME OVER
        break

