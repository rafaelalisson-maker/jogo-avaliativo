import pygame
import random

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1024, 1024))
pygame.display.set_caption("A CANETADA")

fundo = pygame.image.load("fundo.png")
jogador = pygame.image.load("Ganoel Mones.png")
menu_jogo = pygame.image.load("menu.png")
inimigo_amarelo_img = pygame.image.load("Livro amarelo inimigo.png")
inimigo_vermelho_img = pygame.image.load("Livro vermelho.png")

vida_jogador = 100
dano_inimigo = 20
ultimo_dano = 0
tempo_invencibilidade = 1000  # 1 segundo

def menu():
    botao_jogar = pygame.Rect(380, 520, 260, 80)

    while True:
        clock.tick(60)
        screen.blit(menu_jogo, (0, 0))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_jogar.collidepoint(evento.pos):
                    return

        pygame.display.flip()

class Projetil:
    def __init__(self, x, y, direcao):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.velocidade = 10
        self.direcao = direcao

    def mover(self):
        if self.direcao == "esq":
            self.rect.x -= self.velocidade
        elif self.direcao == "dir":
            self.rect.x += self.velocidade

    def desenhar(self, tela):
        pygame.draw.rect(tela, (255, 0, 0), self.rect)

class Inimigo:
    def __init__(self, x, y, imagem):
        self.image = imagem
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocidade = 2

    def mover(self, jogador_rect):
        if jogador_rect.centerx < self.rect.centerx:
            self.rect.x -= self.velocidade
        elif jogador_rect.centerx > self.rect.centerx:
            self.rect.x += self.velocidade

    def desenhar(self, tela):
        tela.blit(self.image, self.rect)

def spawn_inimigo():
    lado = random.choice(["esq", "dir"])

    if lado == "esq":
        x = -60
    else:
        x = 1084

    y = 720
    imagem = random.choice([inimigo_amarelo_img, inimigo_vermelho_img])

    inimigos.append(Inimigo(x, y, imagem))

rect = jogador.get_rect()
rect.midbottom = (512, 780)

velocidade = 5
gravidade = 1
forca_pulo = -20
vel_y = 0
no_chao = False

direcao_jogador = "dir"

tiros = []

inimigos = []

tempo_spawn = 0
intervalo_spawn = 2000

paredes = [
    pygame.Rect(0, 780, 1024, 40),
    pygame.Rect(0, 0, 1024, 40),
    pygame.Rect(0, 0, 40, 1024),
    pygame.Rect(984, 0, 40, 1024),
]

menu()
running = True

while running:
    clock.tick(60)

    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - tempo_spawn > intervalo_spawn:
        spawn_inimigo()
        tempo_spawn = tempo_atual

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_f:
                tiro = Projetil(rect.centerx, rect.centery, direcao_jogador)
                tiros.append(tiro)

            if evento.key == pygame.K_w and no_chao:
                vel_y = forca_pulo
                no_chao = False

    teclas = pygame.key.get_pressed()

    dx = 0
    if teclas[pygame.K_a]:
        dx = -velocidade
        direcao_jogador = "esq"
    if teclas[pygame.K_d]:
        dx = velocidade
        direcao_jogador = "dir"

    rect.x += dx
    for parede in paredes:
        if rect.colliderect(parede):
            if dx > 0:
                rect.right = parede.left
            if dx < 0:
                rect.left = parede.right

    vel_y += gravidade
    rect.y += vel_y

    no_chao = False
    for parede in paredes:
        if rect.colliderect(parede):
            if vel_y > 0:
                rect.bottom = parede.top
                vel_y = 0
                no_chao = True
            elif vel_y < 0:
                rect.top = parede.bottom
                vel_y = 0

    screen.blit(fundo, (0, 0))
    screen.blit(jogador, rect)

    for inimigo in inimigos[:]:
        inimigo.mover(rect)
        inimigo.desenhar(screen)

        if rect.colliderect(inimigo.rect):
            if tempo_atual - ultimo_dano > tempo_invencibilidade:
                vida_jogador -= dano_inimigo
                ultimo_dano = tempo_atual

                if vida_jogador <= 0:
                    running = False

    for tiro in tiros[:]:
        tiro.mover()

        if not screen.get_rect().colliderect(tiro.rect):
            tiros.remove(tiro)
            continue

        for inimigo in inimigos[:]:
            if tiro.rect.colliderect(inimigo.rect):
                tiros.remove(tiro)
                inimigos.remove(inimigo)
                break

        tiro.desenhar(screen)

    pygame.display.flip()

pygame.quit()