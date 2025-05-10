import pygame
import os

pygame.init()

# TELA
LARGURA, ALTURA = 928, 793
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("El-Doria")
fonte = pygame.font.SysFont(None, 37)
preto = (0, 0, 0)
clock = pygame.time.Clock()

# CLASSE PRINCIPAL
class Personagem:
    def __init__(self):
        self.x = 300
        self.y = 662
        self.velocidade = 3
        self.direcao = "idle"
        self.direcao_pulo = "direita"
        self.y_chao = 662
        self.direcao_face = "direita"

        self.atk = False
        self.combo_etapa = 0
        self.combo_frames = self.carregar_combo()
        self.combo_frames_esquerda = [[pygame.transform.flip(f, True, False) for f in frames] for frames in self.combo_frames]
        self.indice_atk = 0
        self.tempo_atk = 60
        self.ultimo_atk_update = pygame.time.get_ticks()
        self.tempo_combo_max = 1500
        self.ultimo_ataque_combo = 0

        self.pulo = False
        self.velocidade_y = 100
        self.forca_pulo = 7
        self.gravidade = 0.5
        self.jump_frames = self.carregar_frames("Jump_KG_2.gif", 6)
        self.jump_frames_esquerda = [pygame.transform.flip(f, True, False) for f in self.jump_frames]
        self.indice_pulo = 0
        self.tempo_pulo = 1000
        self.ultimo_pulo_update = pygame.time.get_ticks()

        self.dash = False
        self.dash_frames = self.carregar_frames("Dashing_KG_1.png", 4)
        self.dash_frames_esquerda = [pygame.transform.flip(f, True, False) for f in self.dash_frames]
        self.indice_dash = 0
        self.tempo_dash = 10
        self.ultimo_dash_update = pygame.time.get_ticks()
        self.tempo_dash_total = 4 * self.tempo_dash
        self.dash_cooldown = 3000
        self.ultimo_dash = -self.dash_cooldown
        self.distancia_dash = 200
        self.velocidade_dash = 25
        self.walk_frames_direita = self.carregar_frames("Walking_KG_2.png", 7)
        self.walk_frames_esquerda = [pygame.transform.flip(f, True, False) for f in self.walk_frames_direita]

        self.idle_frames = self.carregar_frames("Idle_KG_2.png", 4)
        self.indice_frame = 0
        self.tempo_animacao = 100
        self.ultimo_update = pygame.time.get_ticks()
        self.idle_frames_esquerda = [pygame.transform.flip(f, True, False) for f in self.idle_frames]
    def carregar_combo(self):
        combo = []
        spritesheets = ["Attack_KG_1.png", "Attack_KG_2.png", "Attack_KG_4.png", "Attack_KG_3.png"]
        frames_por_combo = [6, 6, 5, 9]
        for i, arquivo in enumerate(spritesheets):
            caminho = os.path.join("champ", arquivo)
            spritesheet = pygame.image.load(caminho).convert_alpha()
            frames = [spritesheet.subsurface((j * 100, 0, 100, 64)) for j in range(frames_por_combo[i])]
            combo.append(frames)
        return combo

    def carregar_frames(self, arquivo, quantidade):
        caminho = os.path.join("champ", arquivo)
        spritesheet = pygame.image.load(caminho).convert_alpha()
        return [spritesheet.subsurface((i * 100, 0, 100, 64)) for i in range(quantidade)]

    def atualizar(self, teclas):
        agora = pygame.time.get_ticks()

        if self.atk:
            if agora - self.ultimo_atk_update > self.tempo_atk:
                self.indice_atk += 1
                self.ultimo_atk_update = agora
                if self.indice_atk >= len(self.combo_frames[self.combo_etapa]):
                    self.atk = False
                    self.indice_atk = 0

        if not self.pulo:
            if teclas[pygame.K_w]:
                self.pulo = True
                self.velocidade_y = -self.forca_pulo
                self.indice_pulo = 0
                self.direcao_pulo = self.direcao
        else:
            self.y += self.velocidade_y
            self.velocidade_y += self.gravidade

            if agora - self.ultimo_pulo_update > self.tempo_pulo:
                self.indice_pulo = (self.indice_pulo + 1) % len(self.jump_frames)
                self.ultimo_pulo_update = agora

            if self.y >= self.y_chao:
                self.y = self.y_chao
                self.pulo = False

        agora = pygame.time.get_ticks()
        if not self.dash and teclas[pygame.K_LSHIFT] and agora - self.ultimo_dash >= self.dash_cooldown:

            self.dash = True
            self.indice_dash = 0
            self.ultimo_dash_update = agora
            self.ultimo_dash = agora
        
        if self.dash:
            if agora - self.ultimo_dash_update > self.tempo_dash:
                self.indice_dash += 1
                self.ultimo_dash_update = agora

                if self.direcao == "direita":
                    self.x += self.velocidade_dash
                else:
                    self.x -= self.velocidade_dash

                if self.indice_dash >= len(self.dash_frames):
                    self.dash = False
                    self.indice_dash = 0

        if not self.atk and not self.dash:
            if teclas[pygame.K_a]:
                self.x -= self.velocidade
                self.direcao = "esquerda"
                self.direcao_face = "esquerda"
            elif teclas[pygame.K_d]:
                self.x += self.velocidade
                self.direcao = "direita"
                self.direcao_face = "direita"
            else:
                self.direcao = "idle"

        if self.x < 0:
            self.x = 0
        if self.x > LARGURA - 100:
            self.x = LARGURA - 100

        if agora - self.ultimo_update > self.tempo_animacao:
            self.indice_frame = (self.indice_frame + 1) % 7
            self.ultimo_update = agora

    def desenhar(self, tela):
        if self.dash:
            frame = self.dash_frames_esquerda[self.indice_dash] if self.direcao == "esquerda" else self.dash_frames[self.indice_dash]
            tela.blit(frame, (self.x, self.y))
        if self.atk:
            frames = self.combo_frames_esquerda if self.direcao == "esquerda" else self.combo_frames
            tela.blit(frames[self.combo_etapa][self.indice_atk], (self.x, self.y))
        elif self.pulo:
            frame = self.jump_frames_esquerda[self.indice_pulo] if self.direcao_pulo == "esquerda" else self.jump_frames[self.indice_pulo]
            tela.blit(frame, (self.x, self.y))
        elif self.direcao == "idle":
            if self.direcao_face == "esquerda":
                frame = self.idle_frames_esquerda[self.indice_frame % len(self.idle_frames_esquerda)]
            else:
                frame = self.idle_frames[self.indice_frame % len(self.idle_frames)]
            tela.blit(frame, (self.x, self.y))
        elif self.direcao == "direita":
            tela.blit(self.walk_frames_direita[self.indice_frame % len(self.walk_frames_direita)], (self.x, self.y))
        elif self.direcao == "esquerda":
            tela.blit(self.walk_frames_esquerda[self.indice_frame % len(self.walk_frames_esquerda)], (self.x, self.y))

    def atacar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_ataque_combo <= self.tempo_combo_max:
            self.combo_etapa = (self.combo_etapa + 1) % 4
        else:
            self.combo_etapa = 0
        self.atk = True
        self.indice_atk = 0
        self.ultimo_atk_update = agora
        self.ultimo_ataque_combo = agora


# CENÁRIO
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


# HUD DE VIDA
def desenhar_hud(tela, vida_atual, vida_maxima):
    x, y = 20, 20
    largura_barra = 200
    altura_barra = 25
    pygame.draw.rect(tela, (255, 255, 255), (x, y, largura_barra, altura_barra), 2)  # Borda
    largura_vida = int((vida_atual / vida_maxima) * largura_barra)
    pygame.draw.rect(tela, (255, 0, 0), (x, y, largura_vida, altura_barra))  # Vida
    texto_vida = fonte.render(f"{vida_atual}/{vida_maxima}", True, (255, 255, 255))
    tela.blit(texto_vida, (x + largura_barra + 10, y + 2))


# GAME SETUP
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

    clock.tick(120)
    teclas = pygame.key.get_pressed()
    personagem.atualizar(teclas)

    # Scroll de fundo com limites
    if teclas[pygame.K_d] and deslocamento_cenario > -(largura_cenario - LARGURA):
        deslocamento_cenario -= 2
    elif teclas[pygame.K_a] and deslocamento_cenario < 0:
        deslocamento_cenario += 2

    tela.fill(preto)

    # Desenhar camadas do cenário com deslocamento
    for layer in layers:
        tela.blit(layer, (deslocamento_cenario, 0))

    personagem.desenhar(tela)

    # Desenhar HUD
    desenhar_hud(tela, vida_atual, vida_maxima)

    pygame.display.update()

pygame.quit()