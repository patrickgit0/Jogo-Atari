# -*- coding: utf-8 -*-
"""
Classes de Sprites para o Atari Space Game.
Contém a definição das entidades móveis do jogo: Nave, Projétil e Asteroide.
Todos os sprites são renderizados via código usando formas geométricas retro.
"""

import pygame
import random
from config import (
    LARGURA_TELA, ALTURA_TELA, COR_NAVE, COR_PROJETIL, COR_ASTEROIDE,
    VELOCIDADE_NAVE, VELOCIDADE_PROJETIL
)

class Nave(pygame.sprite.Sprite):
    """
    Classe que representa a nave espacial controlada pelo jogador.
    Pode se mover horizontalmente e atirar projéteis.
    """
    def __init__(self):
        super().__init__()
        # Define as dimensões da nave espacial
        self.width = 44
        self.height = 36
        
        # Cria uma superfície com suporte a transparência para o sprite
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Desenha a nave com formas geométricas sólidas para simular o estilo de 8-bits
        # Corpo triangular central
        pontos_corpo = [
            (self.width // 2, 0),             # Bico da nave (topo centro)
            (self.width - 8, self.height),     # Asa direita inferior
            (8, self.height)                  # Asa esquerda inferior
        ]
        pygame.draw.polygon(self.image, COR_NAVE, pontos_corpo)
        
        # Asas laterais estilo bloco retrô
        pygame.draw.rect(self.image, COR_NAVE, (0, self.height - 12, 8, 12))
        pygame.draw.rect(self.image, COR_NAVE, (self.width - 8, self.height - 12, 8, 12))
        
        # Canhão central de tiro
        pygame.draw.rect(self.image, COR_NAVE, (self.width // 2 - 2, 0, 4, 10))
        
        # Obtém o retângulo delimitador da nave e posiciona na parte inferior central
        self.rect = self.image.get_rect()
        self.rect.centerx = LARGURA_TELA // 2
        self.rect.bottom = ALTURA_TELA - 20

    def update(self, teclas):
        """
        Atualiza a posição da nave baseado na entrada de teclas do jogador.
        Impede que a nave saia dos limites laterais da tela.
        """
        # Movimento para a esquerda
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.rect.x -= VELOCIDADE_NAVE
            
        # Movimento para a direita
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.rect.x += VELOCIDADE_NAVE
            
        # Garante que a nave permaneça dentro dos limites horizontais da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LARGURA_TELA:
            self.rect.right = LARGURA_TELA


class Projetil(pygame.sprite.Sprite):
    """
    Classe que representa os projéteis (tiros) disparados pela Nave.
    Movem-se verticalmente para o topo da tela.
    """
    def __init__(self, x, y):
        super().__init__()
        # Dimensões do tiro estilo linha clássica de Atari
        self.width = 4
        self.height = 14
        
        # Cria a superfície do projétil e preenche com a cor sólida branca
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(COR_PROJETIL)
        
        # Posiciona o projétil acima do canhão da nave
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self):
        """
        Move o projétil para cima.
        Se ele ultrapassar a borda superior da tela, é excluído para liberar recursos.
        """
        self.rect.y -= VELOCIDADE_PROJETIL
        
        # Destrói o projétil se ele sair da tela
        if self.rect.bottom < 0:
            self.kill()


class Asteroide(pygame.sprite.Sprite):
    """
    Classe que representa os asteroides que caem do céu de forma constante.
    Surgem em posições horizontais aleatórias acima da tela.
    """
    def __init__(self, velocidade_adicional=0):
        super().__init__()
        # Define aleatoriamente o tamanho do asteroide para maior variedade visual
        self.tamanho = random.randint(24, 48)
        
        # Cria a superfície quadrada com transparência
        self.image = pygame.Surface((self.tamanho, self.tamanho), pygame.SRCALPHA)
        
        # Desenha um asteroide irregular poligonal para manter a aparência retrô áspera
        # Cria pontos irregulares a partir do quadrado central
        t = self.tamanho
        pontos = [
            (t // 2, 0),                 # Topo
            (t - random.randint(0, 4), t // 3),   # Superior direito
            (t, t - random.randint(0, 6)),        # Inferior direito
            (t // 2, t),                 # Base
            (random.randint(0, 4), t - 4),        # Inferior esquerdo
            (0, t // 2)                  # Meio esquerdo
        ]
        
        # Preenche o asteroide com uma cor avermelhada sólida e adiciona uma borda pixelizada escura
        pygame.draw.polygon(self.image, COR_ASTEROIDE, pontos)
        
        # Adiciona alguns detalhes/crateras no estilo retrô pixel-art usando pequenos retângulos pretos
        cratera_tamanho = max(4, t // 8)
        pygame.draw.rect(self.image, (0, 0, 0), (t // 3, t // 3, cratera_tamanho, cratera_tamanho))
        pygame.draw.rect(self.image, (0, 0, 0), (t * 2 // 3, t * 3 // 5, cratera_tamanho, cratera_tamanho))
        
        # Posiciona o asteroide em uma coordenada X aleatória logo acima da área de visualização
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, LARGURA_TELA - self.tamanho)
        self.rect.y = -self.tamanho
        
        # Define a velocidade de queda individual adicionando a progressão de dificuldade
        velocidade_base = random.uniform(2.0, 4.5)
        self.velocidade = velocidade_base + velocidade_adicional

    def update(self):
        """
        Move o asteroide para baixo de forma constante.
        """
        self.rect.y += int(self.velocidade)
        # Nota: a colisão com o fundo da tela será processada no loop principal do jogo.
