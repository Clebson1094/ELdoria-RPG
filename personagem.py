import pygame
import os

LARGURA = 928

class Personagem:
    def __init__(self):
        self.x = 300
        self.y = 662
        self.velocidade = 5
        self.direcao = "idle"
        self.direcao_pulo = "direita"
        self.y_chao = 662

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
        self.velocidade_y = 0
        self.forca_pulo = 10
        self.gravidade = 1
        self.jump_frames = self.carregar_frames("Jump_KG_2.gif", 6)
        self.jump_frames_esquerda = [pygame.transform.flip(f, True, False) for f in self.jump_frames]
        self.indice_pulo = 0
        self.tempo_pulo = 100
        self.ultimo_pulo_update = pygame.time.get_ticks()

        self.walk_frames_direita = self.carregar_frames("Walking_KG_2.png", 7)
        self.walk_frames_esquerda = [pygame.transform.flip(f, True, False) for f in self.walk_frames_direita]

        self.idle_frames = self.carregar_frames("Idle_KG_2.png", 4)
        self.indice_frame = 0
        self.tempo_animacao = 150
        self.ultimo_update = pygame.time.get_ticks()

        # DASH
        self.dash_frames = self.carregar_frames("Dashing_KG_1.png", 4)
        self.dash_frames_esquerda = [pygame.transform.flip(f, True, False) for f in self.dash_frames]
        self.dashando = False
        self.tempo_dash = 300
        self.velocidade_dash = 12
        self.indice_dash = 0
        self.ultimo_dash = 0

        # ROLL
        self.roll_frames = self.carregar_frames("Rolling_KG_1.png", 10)
        self.roll_frames_esquerda = [pygame.transform.flip(f, True, False) for f in self.roll_frames]
        self.roll = False
        self.tempo_roll = 500
        self.velocidade_roll = 8
        self.indice_roll = 0
        self.ultimo_roll = 0

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

    def carregar_frames(self, arquivo, quantidade, largura=100, altura=64):
        caminho = os.path.join("champ", arquivo)
        spritesheet = pygame.image.load(caminho).convert_alpha()
        return [spritesheet.subsurface((i * largura, 0, largura, altura)) for i in range(quantidade)]

    def atualizar(self, teclas):
        agora = pygame.time.get_ticks()

        # Roll
        if self.roll:
            if agora - self.ultimo_roll < self.tempo_roll:
                if self.direcao == "direita":
                    self.x += self.velocidade_roll
                elif self.direcao == "esquerda":
                    self.x -= self.velocidade_roll
                if agora - self.ultimo_update > self.tempo_animacao:
                    self.indice_roll = (self.indice_roll + 1) % len(self.roll_frames)
                    self.ultimo_update = agora
                return
            else:
                self.roll = False

        # Dash
        if self.dashando:
            if agora - self.ultimo_dash < self.tempo_dash:
                if self.direcao == "direita":
                    self.x += self.velocidade_dash
                elif self.direcao == "esquerda":
                    self.x -= self.velocidade_dash
                if agora - self.ultimo_update > self.tempo_animacao:
                    self.indice_dash = (self.indice_dash + 1) % len(self.dash_frames)
                    self.ultimo_update = agora
                return
            else:
                self.dashando = False

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

        if not self.atk:
            if teclas[pygame.K_a]:
                self.x -= self.velocidade
                self.direcao = "esquerda"
            elif teclas[pygame.K_d]:
                self.x += self.velocidade
                self.direcao = "direita"
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
        if self.roll:
            frame = self.roll_frames_esquerda[self.indice_roll] if self.direcao == "esquerda" else self.roll_frames[self.indice_roll]
            tela.blit(frame, (self.x, self.y))
            return

        if self.dashando:
            frame = self.dash_frames_esquerda[self.indice_dash] if self.direcao == "esquerda" else self.dash_frames[self.indice_dash]
            tela.blit(frame, (self.x, self.y))
            return

        if self.atk:
            frames = self.combo_frames_esquerda if self.direcao == "esquerda" else self.combo_frames
            tela.blit(frames[self.combo_etapa][self.indice_atk], (self.x, self.y))
        elif self.pulo:
            frame = self.jump_frames_esquerda[self.indice_pulo] if self.direcao_pulo == "esquerda" else self.jump_frames[self.indice_pulo]
            tela.blit(frame, (self.x, self.y))
        elif self.direcao == "idle":
            tela.blit(self.idle_frames[self.indice_frame % len(self.idle_frames)], (self.x, self.y))
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

    def dash(self):
        agora = pygame.time.get_ticks()
        if not self.dashando:
            self.dashando = True
            self.ultimo_dash = agora
            self.indice_dash = 0

    def iniciar_roll(self):
        agora = pygame.time.get_ticks()
        if not self.roll and not self.pulo:
            self.roll = True
            self.ultimo_roll = agora
            self.indice_roll = 0
