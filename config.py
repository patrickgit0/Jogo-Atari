# -*- coding: utf-8 -*-
"""
Configurações globais para o Jogo Atari Space Game.
Este arquivo contém as constantes que definem as propriedades da tela,
cores, velocidades, taxas de atualização e outros parâmetros de jogabilidade.
"""

# Configurações da Janela do Jogo
LARGURA_TELA = 800
ALTURA_TELA = 600
TITULO_JOGO = "Atari Space Game"
FPS = 60

# Paleta de Cores Estilo Atari (RGB)
COR_FUNDO = (0, 0, 0)          # Preto absoluto para o espaço profundo
COR_NAVE = (0, 255, 128)       # Verde limão vibrante retro para a nave do jogador
COR_PROJETIL = (255, 255, 255)  # Branco clássico de 8-bits para os tiros
COR_ASTEROIDE = (255, 64, 64)   # Vermelho vibrante estilo perigo para os asteroides
COR_TEXTO = (255, 255, 255)     # Branco para a interface de usuário (placar e textos)
COR_GAME_OVER = (255, 0, 0)     # Vermelho brilhante para mensagens de fim de jogo

# Parâmetros de Equilíbrio do Jogador
VELOCIDADE_NAVE = 7            # Pixels por quadro que a nave se move
COOLDOWN_TIRO = 250            # Tempo mínimo (milissegundos) entre disparos (barra de espaço)
VELOCIDADE_PROJETIL = 9        # Pixels por quadro que o tiro sobe

# Parâmetros de Geração e Queda de Asteroides
ASTEROIDE_SPAWN_TEMPO = 900    # Intervalo de tempo inicial (ms) para surgir um novo asteroide
ASTEROIDE_VEL_MIN = 2          # Velocidade mínima de descida do asteroide
ASTEROIDE_VEL_MAX = 5          # Velocidade máxima de descida do asteroide
TAMANHO_MIN_ASTEROIDE = 20     # Tamanho mínimo do asteroide (pixels)
TAMANHO_MAX_ASTEROIDE = 50     # Tamanho máximo do asteroide (pixels)

# Progressão de Dificuldade
AUMENTO_DIFICULDADE_PONTOS = 10  # A cada X pontos, a dificuldade aumenta
VELOCIDADE_PROGRESSIVA_INCREMENTO = 0.5  # Incremento de velocidade dos asteroides por nível
