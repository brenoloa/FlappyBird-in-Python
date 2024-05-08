import pygame
from pygame.locals import *
import random
import os
#os.chdir('C:/Users/Pichau/PycharmProjects/pythonProject3/games/FlappyBird/')

JANELA_LARGURA = 400
JANELA_ALTURA = 800
SPEED = 10
GRAVITY = 1
GAME_SPEED = 10
SCORE = 0
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

def exibe_mensagem(msg, tamanho, cor):
    fonte = pygame.font.SysFont('comicsansms', tamanho, True, False)
    mensagem = f'{msg}'
    texto_formatado = fonte.render(mensagem, True, cor)
    text_rect = texto_formatado.get_rect(topleft=(110, 420))
    screen.blit(texto_formatado, text_rect)

def exibe_mensagem_novo(msg, tamanho, cor):
    fonte = pygame.font.SysFont('comicsansms', tamanho, True, False)
    mensagem = f'{msg}'
    texto_formatado = fonte.render(mensagem, True, cor)
    text_rect = texto_formatado.get_rect(topleft=(50 , 20))
    screen.blit(texto_formatado, text_rect)

pygame.init()

screen = pygame.display.set_mode((JANELA_LARGURA, JANELA_ALTURA))

pygame.display.set_caption("brenoloa")

BACKGROUND = pygame.image.load('background.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (JANELA_LARGURA, JANELA_ALTURA))

GAME_OVER = pygame.image.load('gameover.png').convert_alpha()
passed_pipes = pygame.sprite.Group()
bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)
#-=-=
font = pygame.font.Font('04B_19__.TTF', 46)
text = font.render("Score: " + str(SCORE), 1, (255, 255, 255))

screen.blit(text, (10, 10))

#-=-=
ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(GROUND_WIDTH * i)
    ground_group.add(ground)

    pipe_group = pygame.sprite.Group()
for i in range(2):
    pipes = get_random_pipes(JANELA_LARGURA * i + 600)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])
game_over = False
clock = pygame.time.Clock()
# looping principal.
while True:
    clock.tick(30) #fps
    exibe_mensagem_novo("github.com/brenoloa", 30, (255, 255, 255))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if not game_over:  # somente pular se o jogo não tiver terminado
                    bird.bump()
                else:  # reiniciar o jogo se o jogo tiver terminado
                    SCORE = 0
                    bird_group.empty()
                    bird = Bird()
                    bird_group.add(bird)

                    pipe_group.empty()
                    for i in range(2):
                        pipes = get_random_pipes(JANELA_LARGURA * i + 600)
                        pipe_group.add(pipes[0])
                        pipe_group.add(pipes[1])

                    game_over = False

    if not game_over:
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
        pipe_group.update()
        ground_group.update()
        passed_pipes.update()

        bird_group.draw(screen)
        pipe_group.draw(screen)
        ground_group.draw(screen)
        text = font.render("" + str(SCORE), 1, (255, 255, 255))
        screen.blit(text, (190, 300))


        # Verifica colisões
        if pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or \
           pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask):
            game_over = True

        # Mostra a mensagem de Game Over
        if game_over:
            screen.blit(GAME_OVER, (JANELA_LARGURA/2 - GAME_OVER.get_width()/2, JANELA_ALTURA/2 - GAME_OVER.get_height()/2))

            exibe_mensagem("Pressione ESPAÇO", 20, (255, 255, 255))
            exibe_mensagem("Pressione ESPAÇO", 20, (255, 255, 255))

    for pipe in pipe_group:
        if pipe.rect.right < bird.rect.left and pipe not in passed_pipes:
            SCORE = (SCORE + 0.5)
            passed_pipes.add(pipe)
            GAME_SPEED = (GAME_SPEED * 1.01)
    pygame.display.update()

