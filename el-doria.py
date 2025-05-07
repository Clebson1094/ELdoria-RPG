import pygame
import os

pygame.init()

#TELA
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("El-Doria")
fonte = pygame.font.Sysfont(None, 60)
texto = fonte.render("titulo", True, (255, 255, 255))
titulo = "El-Doria"
meio_da_tela = (150, 250)
preto = (0, 0, 0)

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False



    

    tela.fill((preto))
    tela.blit(texto (meio_da_tela))
    pygame.display.update()
pygame.quit()