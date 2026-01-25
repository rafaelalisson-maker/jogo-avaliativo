import pygame

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1024, 1024))
pygame.display.set_caption("A CANETADA")

fundo = pygame.image.load("fundo.png")
jogador = pygame.image.load("C:/Users/USER/Documents/jogo-avaliativo/Ganoel Mones.png")
menu_jogo = pygame.image.load("menu.png")

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


rect = jogador.get_rect()
rect.center = (512, 650)
velocidade = 5
running = True

menu()

while running:
    clock.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_a]:
        rect.x -= velocidade
    if teclas[pygame.K_d]:
        rect.x += velocidade
    if teclas[pygame.K_w]:
        rect.y -= velocidade
    if teclas[pygame.K_s]:
        rect.y += velocidade

    screen.blit(fundo, (0, 0))
    screen.blit(jogador, rect)

    pygame.display.flip()

pygame.quit()
