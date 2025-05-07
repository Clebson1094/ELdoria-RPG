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

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False



    

    tela.fill((preto))
    tela.blit(texto, (326, 260))
    pygame.display.update()
pygame.quit()
