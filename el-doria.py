import pygame
import os

pygame.init()

#TELA
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("El-Doria")
fonte = pygame.font.SysFont(None, 60)
texto = fonte.render("El-Doria", True, (255, 255, 255))
preto = (0, 0, 0)

#CLOCK
clock = pygame.time.Clock()

#MOVIMENTAÇÃO DO PERSONAGEM
x = 300
y = 300
velocidade = 4

pulo = False
forca_pulo = 25
gravidade = 2
vel_y = 1

#CONTROLES
def controles(teclas):
    global x, y, pulo, vel_y

    if teclas[pygame.K_LEFT]:
        x -= velocidade
    if teclas [pygame.K_RIGHT]:
        x += velocidade

    if not pulo:
        if teclas[pygame.K_SPACE]:
            pulo = True
            vel_y = -forca_pulo
    else:
        y += vel_y
        vel_y += gravidade

        #ENCOSTANDO NO CHÃO
        if y >= 300:
            y = 300
            pulo = False

rodando = True
while rodando:
    clock.tick(60)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
    
    teclas = pygame.key.get_pressed()
    controles(teclas)

   

    tela.fill((preto))
    
    personagem = pygame.Rect(x, y, 50, 50)
    pygame.draw.rect(tela, (255, 0, 0), personagem)
    
    

    tela.blit(texto, (326, 260))
    pygame.display.update()

pygame.quit()
