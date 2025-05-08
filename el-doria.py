import pygame
import os

pygame.init()
clock = pygame.time.Clock()
#TELA
largura = 1000
altura = 800
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("El-Doria")
fonte = pygame.font.SysFont(None, 60)
texto = fonte.render("", True, (255, 255, 255))
preto = (0, 0, 0)

#SPRITESHEET_WALKING
caminho_walk = os.path.join("champ", "walk.png.png")
spritesheet_walk = pygame.image.load(caminho_walk).convert_alpha()

largura_walk = 64
altura_walk = 64
quantidade_walk_frames = 7

walk_frames_direita = []
for i in range(quantidade_walk_frames):
    frame = spritesheet_walk.subsurface((i * largura_walk, 0, largura_walk, altura_walk))
    walk_frames_direita.append(frame)

walk_frames_esquerda = [pygame.transform.flip(f, True, False) for f in walk_frames_direita]

x = 300
y = 300
velocidade = 10
direcao = "idle"

#spritessheet
caminho_idle = os.path.join("champ", "idle.png.png")
spritesheet_idle = pygame.image.load(caminho_idle).convert_alpha()

#CONFIG DO SPRITESHEET
largura_frame = 64
altura_frame = 64
quantidade_frames = 4
idle_frames = []

for i in range(quantidade_frames):
    frame = spritesheet_idle.subsurface((i * largura_frame, 0, largura_frame, altura_frame))
    idle_frames.append(frame)


#CONTROLE DE ANIMAÇÃO
indice_frame = 0
tempo_animacao = 180
ultimo_update = pygame.time.get_ticks()


rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
    clock.tick(60)

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT]:
        x -= velocidade
        direcao = "esquerda"
    elif teclas[pygame.K_RIGHT]:
        x += velocidade
        direcao = "direita"
    else:
        direcao = "idle"
    
    agora = pygame.time.get_ticks()
    if agora - ultimo_update > tempo_animacao:
        if direcao == "idle":
            indice_frame = (indice_frame + 1) % len(idle_frames)
        else:
            indice_frame = (indice_frame + 1) % quantidade_walk_frames
        ultimo_update = agora


    
    tela.fill((preto))
    
    if direcao == "idle":
        tela.blit(idle_frames[indice_frame % len(idle_frames)], (x, y))
    elif direcao == "direita":
        tela.blit(walk_frames_direita[indice_frame % len(walk_frames_direita)], (x, y))
    elif direcao == "esquerda":
        tela.blit(walk_frames_esquerda[indice_frame % len(walk_frames_esquerda)], (x, y))

    pygame.display.update()

pygame.quit()
