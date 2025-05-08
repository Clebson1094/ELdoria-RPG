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

#SPRITESHEET_PULO
caminho_pulo = os.path.join("champ", "Jump_KG_1.png")
spritesheet_jump = pygame.image.load(caminho_pulo).convert_alpha()
largura_pulo = 100
altura_pulo = 64
quantidade_jump_frames = 6

jump_frames = []
for i in range(quantidade_jump_frames):
    frame = spritesheet_jump.subsurface((i * largura_pulo, 0, largura_pulo, altura_pulo))
    jump_frames.append(frame)

pulo = False
velocidade_y = 0
forca_pulo = 15
gravidade = 1
y_chao = 300
indice_pulo = 0
tempo_pulo = 100
ultimo_pulo_update = pygame.time.get_ticks()

#SPRITESHEET_WALKING
caminho_walk = os.path.join("champ", "walk.png.png")
spritesheet_walk = pygame.image.load(caminho_walk).convert_alpha()

largura_walk = 100
altura_walk = 64
quantidade_walk_frames = 7

walk_frames_direita = []
for i in range(quantidade_walk_frames):
    frame = spritesheet_walk.subsurface((i * largura_walk, 0, largura_walk, altura_walk))
    walk_frames_direita.append(frame)

walk_frames_esquerda = [pygame.transform.flip(f, True, False) for f in walk_frames_direita]

x = 300
y = 300
velocidade = 4
direcao = "idle"

#SPRITES_IDLE
caminho_idle = os.path.join("champ", "idle.png.png")
spritesheet_idle = pygame.image.load(caminho_idle).convert_alpha()

largura_frame = 100
altura_frame = 64
quantidade_frames = 4
idle_frames = []

for i in range(quantidade_frames):
    frame = spritesheet_idle.subsurface((i * largura_frame, 0, largura_frame, altura_frame))
    idle_frames.append(frame)

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
    if not pulo:
        if teclas[pygame.K_UP]:
            pulo = True
            velocidade_y = -forca_pulo
            indice_pulo = 0
    else:
        y += velocidade_y
        velocidade_y += gravidade

        agora = pygame.time.get_ticks()
        if agora - ultimo_pulo_update > tempo_pulo:
            indice_pulo = (indice_pulo + 1) % len(jump_frames)
            ultimo_pulo_update = agora
        
        if y >= y_chao:
            y = y_chao
            pulo = False
    
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
    
    if pulo:
        tela.blit(jump_frames[indice_pulo], (x, y))
    elif direcao == "idle":
        tela.blit(idle_frames[indice_frame % len(idle_frames)], (x, y))
    elif direcao == "direita":
        tela.blit(walk_frames_direita[indice_frame % len(walk_frames_direita)], (x, y))
    elif direcao == "esquerda":
        tela.blit(walk_frames_esquerda[indice_frame % len(walk_frames_esquerda)], (x, y))

    pygame.display.update()

pygame.quit()
