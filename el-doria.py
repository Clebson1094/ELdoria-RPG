import pygame
import os
from personagem import Personagem

pygame.init()

LARGURA, ALTURA = 928, 793
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("El-Doria")
fonte = pygame.font.SysFont(None, 37)
preto = (0, 0, 0)
clock = pygame.time.Clock()

def carregar_layers():
    layers = []
    nomes = [
        "Layer_0011_0.png", "Layer_0010_1.png", "Layer_0009_2.png", "Layer_0008_3.png",
        "Layer_0007_Lights.png", "Layer_0006_4.png", "Layer_0005_5.png", "Layer_0004_Lights.png",
        "Layer_0003_6.png", "Layer_0002_7.png", "Layer_0001_8.png", "Layer_0000_9.png"
    ]
    for nome in nomes:
        caminho = os.path.join("cenario", nome)
        imagem = pygame.image.load(caminho).convert_alpha()
        layers.append(imagem)
    return layers

def desenhar_hud(tela, vida_atual, vida_maxima):
    x, y = 20, 20
    largura_barra = 200
    altura_barra = 25
    pygame.draw.rect(tela, (255, 255, 255), (x, y, largura_barra, altura_barra), 2)
    largura_vida = int((vida_atual / vida_maxima) * largura_barra)
    pygame.draw.rect(tela, (255, 0, 0), (x, y, largura_vida, altura_barra))
    texto_vida = fonte.render(f"{vida_atual}/{vida_maxima}", True, (255, 255, 255))
    tela.blit(texto_vida, (x + largura_barra + 10, y + 2))

personagem = Personagem()
layers = carregar_layers()
largura_cenario = layers[0].get_width()
deslocamento_cenario = 0
vida_atual = 100
vida_maxima = 100
rodando = True

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and not personagem.atk:
                personagem.atacar()
            if evento.key == pygame.K_LSHIFT and not personagem.dashando:
                personagem.dash()
            if evento.key == pygame.K_LCTRL and not personagem.roll:
                personagem.iniciar_roll()

    clock.tick(60)
    teclas = pygame.key.get_pressed()
    personagem.atualizar(teclas)

    if teclas[pygame.K_d] and deslocamento_cenario > -(largura_cenario - LARGURA):
        deslocamento_cenario -= 2
    elif teclas[pygame.K_a] and deslocamento_cenario < 0:
        deslocamento_cenario += 2

    tela.fill(preto)
    for layer in layers:
        tela.blit(layer, (deslocamento_cenario, 0))

    personagem.desenhar(tela)
    desenhar_hud(tela, vida_atual, vida_maxima)
    pygame.display.update()

pygame.quit()
