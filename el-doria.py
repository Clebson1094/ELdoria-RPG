import pygame
import os

pygame.init()
clock = pygame.time.Clock()
#TELA
largura = 1000
altura = 768
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("El-Doria")
fonte = pygame.font.SysFont(None, 60)
texto = fonte.render("", True, (255, 255, 255))
preto = (0, 0, 0)

#SPRITESHEET_ATACK
combo_frames = []

combo_spritesheets = [
    "Attack_KG_1.png",
    "Attack_KG_2.png",
    "Attack_KG_4.png",
    "Attack_KG_3.png"
]

frames_por_combo = [6, 6, 5, 9]

largura_atk = 100
altura_atk = 64

for i, arquivo in enumerate(combo_spritesheets):
    caminho = os.path.join("champ", arquivo)
    spritesheet = pygame.image.load(caminho).convert_alpha()
    frames = []
    for j in range(frames_por_combo[i]):
        frame = spritesheet.subsurface((j * largura_atk, 0,largura_atk, altura_atk))
        frames.append(frame)
    combo_frames.append(frames)

combo_frames_esquerda = [[pygame.transform.flip(f, True, False) for f in frames] for frames in combo_frames]

largura_atk = 100
altura_atk = 64
quantidade_atk_frames = 5
indice_atk = 0
tempo_atk = 60
ultimo_atk_update = pygame.time.get_ticks()
atk = False
combo_etapa = 0
tempo_combo_max = 800
ultimo_ataque_combo = 0

#SPRITESHEET_PULO
caminho_pulo = os.path.join("champ", "Jump_KG_2.gif")
spritesheet_jump = pygame.image.load(caminho_pulo).convert_alpha()
largura_pulo = 100
altura_pulo = 64
quantidade_jump_frames = 6

jump_frames = []
for i in range(quantidade_jump_frames):
    frame = spritesheet_jump.subsurface((i * largura_pulo, 0, largura_pulo, altura_pulo))
    jump_frames.append(frame)

jump_frames_esquerda = [pygame.transform.flip(f, True, False) for f in jump_frames]

pulo = False
velocidade_y = 0
forca_pulo = 10
gravidade = 1
y_chao = 300
indice_pulo = 0
tempo_pulo = 100
direcao_pulo = "direita"
ultimo_pulo_update = pygame.time.get_ticks()

#SPRITESHEET_WALKING
caminho_walk = os.path.join("champ", "Walking_KG_2.png")
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
velocidade = 5
direcao = "idle"

#SPRITES_IDLE
caminho_idle = os.path.join("champ", "Idle_KG_2.png")
spritesheet_idle = pygame.image.load(caminho_idle).convert_alpha()

largura_frame = 100
altura_frame = 64
quantidade_frames = 4
idle_frames = []

for i in range(quantidade_frames):
    frame = spritesheet_idle.subsurface((i * largura_frame, 0, largura_frame, altura_frame))
    idle_frames.append(frame)

indice_frame = 0
tempo_animacao = 150
ultimo_update = pygame.time.get_ticks()


rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN: 
            if evento.key == pygame.K_SPACE and not atk:
                agora = pygame.time.get_ticks()
                if agora - ultimo_ataque_combo <= tempo_combo_max:
                    combo_etapa = (combo_etapa + 1) % 4
                else:
                    combo_etapa = 0
                atk = True
                indice_atk = 0
                ultimo_atk_update = agora
                ultimo_ataque_combo = agora
    clock.tick(60)

    teclas = pygame.key.get_pressed()

    if atk:
        agora_atk = pygame.time.get_ticks()
        if agora_atk - ultimo_atk_update > tempo_atk:
                indice_atk  += 1
                ultimo_atk_update = agora_atk
                
                if indice_atk >= len(combo_frames[combo_etapa]):
                    atk = False
                    indice_atk = 0

    if not pulo:
        if teclas[pygame.K_UP]:
            pulo = True
            velocidade_y = -forca_pulo
            indice_pulo = 0
            direcao_pulo = direcao
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
    if not atk:
        if teclas[pygame.K_LEFT]:
            x -= velocidade
            direcao = "esquerda"
        elif teclas[pygame.K_RIGHT]:
            x += velocidade
            direcao = "direita"
        else:
            direcao = "idle"
    
    agora_animacao = pygame.time.get_ticks()
    if agora_animacao - ultimo_update > tempo_animacao:
        if direcao == "idle":
            indice_frame = (indice_frame + 1) % len(idle_frames)
        elif not pulo and not atk:
            indice_frame = (indice_frame + 1) % quantidade_walk_frames
        ultimo_update = agora_animacao

    tela.fill((preto))
    
    if atk:
        if direcao == "esquerda":
            tela.blit(combo_frames_esquerda[combo_etapa][indice_atk], (x, y))
        else:
            tela.blit(combo_frames[combo_etapa][indice_atk], (x, y))
    elif pulo:
        if direcao_pulo == "esquerda":
            tela.blit(jump_frames_esquerda[indice_pulo], (x, y))
        else:
            tela.blit(jump_frames[indice_pulo], (x, y))
    elif direcao == "idle":
        tela.blit(idle_frames[indice_frame % len(idle_frames)], (x, y))
    elif direcao == "direita":
        tela.blit(walk_frames_direita[indice_frame % len(walk_frames_direita)], (x, y))
    elif direcao == "esquerda":
        tela.blit(walk_frames_esquerda[indice_frame % len(walk_frames_esquerda)], (x, y))


    pygame.display.update()

pygame.quit()