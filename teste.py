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

fonte_vida = pygame.font.SysFont(None, 36)
fonte_pontos = pygame.font.SysFont(None, 40)
fonte_titulo = pygame.font.SysFont(None, 80)

vida_jogador = 100
dano_inimigo = 20
ultimo_dano = 0
tempo_invencibilidade = 1000
pontuacao = 0

nivel_dificuldade = 1
tempo_dificuldade = 0
intervalo_dificuldade = 15000

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

def fim_de_jogo():
    texto = fonte_titulo.render("FIM DE JOGO", True, (255, 0, 0))
    pontos_finais = fonte_pontos.render(
        f"Pontuação Final: {pontuacao}", True, (255, 255, 255)
    )

    texto_rect = texto.get_rect(center=(512, 450))
    pontos_rect = pontos_finais.get_rect(center=(512, 550))

    while True:
        clock.tick(60)
        screen.blit(fundo, (0, 0))
        screen.blit(texto, texto_rect)
        screen.blit(pontos_finais, pontos_rect)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            if evento.type == pygame.KEYDOWN:
                pygame.quit()
                exit()

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
    def __init__(self, x, y, imagem, plataforma):
        self.image = imagem
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocidade = 2 + nivel_dificuldade
        self.plataforma = plataforma

    def mover(self, jogador_rect):
        if jogador_rect.centerx < self.rect.centerx:
            self.rect.x -= self.velocidade
        elif jogador_rect.centerx > self.rect.centerx:
            self.rect.x += self.velocidade

        if self.rect.left < self.plataforma.left:
            self.rect.left = self.plataforma.left
        if self.rect.right > self.plataforma.right:
            self.rect.right = self.plataforma.right

    def desenhar(self, tela):
        tela.blit(self.image, self.rect)

def spawn_inimigo():
    plataforma = random.choice(prateleiras)
    imagem = random.choice([inimigo_amarelo_img, inimigo_vermelho_img])
    lado = random.choice(["esq", "dir"])

    inimigo = Inimigo(0, 0, imagem, plataforma)

    if lado == "esq":
        inimigo.rect.left = plataforma.left
    else:
        inimigo.rect.right = plataforma.right

    inimigo.rect.bottom = plataforma.top
    inimigos.append(inimigo)

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

prateleiras = [
    pygame.Rect(15, 860, 275, 20),
    pygame.Rect(320, 763, 350, 18),
    pygame.Rect(720, 860, 275, 20),
]

menu()
running = True

while running:
    clock.tick(60)
    tempo_atual = pygame.time.get_ticks()

    if tempo_atual - tempo_dificuldade > intervalo_dificuldade:
        nivel_dificuldade += 1
        tempo_dificuldade = tempo_atual

        if intervalo_spawn > 600:
            intervalo_spawn -= 300

        dano_inimigo += 5

    if tempo_atual - tempo_spawn > intervalo_spawn:
        spawn_inimigo()
        tempo_spawn = tempo_atual

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_f:
                tiros.append(Projetil(rect.centerx, rect.centery, direcao_jogador))

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

    vel_y += gravidade
    rect.y += vel_y

    no_chao = False
    for plataforma in prateleiras:
        if rect.colliderect(plataforma) and vel_y > 0:
            rect.bottom = plataforma.top
            vel_y = 0
            no_chao = True

    if rect.top > 1024:
        fim_de_jogo()

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
                    fim_de_jogo()

    for tiro in tiros[:]:
        tiro.mover()
        if not screen.get_rect().colliderect(tiro.rect):
            tiros.remove(tiro)
            continue

        for inimigo in inimigos[:]:
            if tiro.rect.colliderect(inimigo.rect):
                tiros.remove(tiro)
                inimigos.remove(inimigo)
                pontuacao += 10
                break

        tiro.desenhar(screen)

    screen.blit(fonte_vida.render(f"Vida: {vida_jogador}", True, (255, 0, 0)), (20, 20))
    screen.blit(fonte_pontos.render(f"Pontos: {pontuacao}", True, (255, 255, 255)), (20, 60))
    screen.blit(
        fonte_pontos.render(f"Dificuldade: {nivel_dificuldade}", True, (255, 255, 0)),
        (20, 100)
    )

    pygame.display.flip()

pygame.quit()