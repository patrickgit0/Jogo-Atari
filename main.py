# -*- coding: utf-8 -*-
"""
Motor Principal do Atari Space Game.
Gerencia a inicialização, o loop do jogo, as telas de estado,
colisões, renderização e lógica de progressão de dificuldade.
"""

import sys
import pygame
from config import (
    LARGURA_TELA, ALTURA_TELA, TITULO_JOGO, FPS, COR_FUNDO, COR_TEXTO,
    COR_GAME_OVER, COOLDOWN_TIRO, ASTEROIDE_SPAWN_TEMPO,
    AUMENTO_DIFICULDADE_PONTOS, VELOCIDADE_PROGRESSIVA_INCREMENTO
)
from sprites import Nave, Projetil, Asteroide

# Definição dos Estados do Jogo usando constantes
ESTADO_MENU = 0
ESTADO_JOGANDO = 1
ESTADO_GAME_OVER = 2

class Jogo:
    """
    Classe central que gerencia o fluxo global, estados e recursos do jogo.
    """
    def __init__(self):
        # Inicializa todos os módulos importados do Pygame
        pygame.init()
        
        # Configura a janela de exibição
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption(TITULO_JOGO)
        
        # Cria o relógio para controle de taxa de quadros (FPS)
        self.clock = pygame.time.Clock()
        
        # Configura a fonte para renderização dos textos.
        # Usa Courier New ou Consolas, que são comuns em sistemas operacionais modernos
        # e dão um excelente visual de terminal pixelado estilo Atari.
        try:
            self.fonte_placar = pygame.font.SysFont("Courier New", 28, bold=True)
            self.fonte_titulo = pygame.font.SysFont("Courier New", 48, bold=True)
            self.fonte_subtitulo = pygame.font.SysFont("Courier New", 20, bold=True)
        except OSError:
            # Caso a fonte do sistema não esteja disponível, usa a fonte padrão
            self.fonte_placar = pygame.font.Font(None, 36)
            self.fonte_titulo = pygame.font.Font(None, 64)
            self.fonte_subtitulo = pygame.font.Font(None, 24)

        # Configura o estado inicial do jogo
        self.estado_atual = ESTADO_MENU
        
        # Criação de Grupos de Sprites do Pygame
        # Estes grupos ajudam a gerenciar múltiplos objetos, atualizá-los e desenhá-los de uma só vez
        self.todos_sprites = pygame.sprite.Group()
        self.asteroides = pygame.sprite.Group()
        self.projeteis = pygame.sprite.Group()
        
        # Instanciação da Nave do Jogador
        self.nave = Nave()
        self.todos_sprites.add(self.nave)
        
        # Variáveis de Controle de Pontuação e Dificuldade
        self.pontos = 0
        self.nivel = 1
        
        # Variáveis de Controle de Tempo para Disparos e Surgimento de Inimigos
        self.ultimo_tiro = 0
        self.ultimo_spawn = 0
        self.tempo_spawn_atual = ASTEROIDE_SPAWN_TEMPO
        self.velocidade_adicional_asteroide = 0.0

    def reiniciar_jogo(self):
        """
        Reseta todas as variáveis de estado, limpa os sprites
        e prepara o jogo para uma nova rodada.
        """
        # Limpa todos os sprites antigos
        self.todos_sprites.empty()
        self.asteroides.empty()
        self.projeteis.empty()
        
        # Recria e adiciona a nave do jogador
        self.nave = Nave()
        self.todos_sprites.add(self.nave)
        
        # Reseta pontuação, nível e mecânicas de tempo
        self.pontos = 0
        self.nivel = 1
        self.ultimo_tiro = 0
        self.ultimo_spawn = pygame.time.get_ticks()
        self.tempo_spawn_atual = ASTEROIDE_SPAWN_TEMPO
        self.velocidade_adicional_asteroide = 0.0
        
        # Define o estado para iniciar a jogabilidade
        self.estado_atual = ESTADO_JOGANDO

    def disparar_projetil(self):
        """
        Cria um projétil no bico da nave se o cooldown de tiro já tiver passado.
        """
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.ultimo_tiro >= COOLDOWN_TIRO:
            # Instancia o projétil na posição horizontal do centro da nave
            # e na posição vertical da parte superior da nave
            tiro = Projetil(self.nave.rect.centerx, self.nave.rect.top)
            self.todos_sprites.add(tiro)
            self.projeteis.add(tiro)
            # Atualiza a marcação do tempo do último tiro
            self.ultimo_tiro = tempo_atual

    def gerenciar_dificuldade(self):
        """
        Aumenta o nível de dificuldade com base na pontuação atual do jogador.
        Asteroides caem mais rápido e aparecem com maior frequência.
        """
        novo_nivel = (self.pontos // AUMENTO_DIFICULDADE_PONTOS) + 1
        if novo_nivel > self.nivel:
            self.nivel = novo_nivel
            # Aumenta a velocidade de queda dos novos asteroides
            self.velocidade_adicional_asteroide = (self.nivel - 1) * VELOCIDADE_PROGRESSIVA_INCREMENTO
            # Diminui o tempo de spawn (aparecem mais rápido), limitando a no mínimo 250ms
            self.tempo_spawn_atual = max(250, ASTEROIDE_SPAWN_TEMPO - ((self.nivel - 1) * 75))

    def atualizar(self):
        """
        Lida com as atualizações de lógica e física do jogo.
        """
        tempo_atual = pygame.time.get_ticks()
        
        # 1. Geração de Asteroides
        # Cria um novo asteroide se o intervalo de tempo tiver expirado
        if tempo_atual - self.ultimo_spawn >= self.tempo_spawn_atual:
            asteroide = Asteroide(self.velocidade_adicional_asteroide)
            self.todos_sprites.add(asteroide)
            self.asteroides.add(asteroide)
            self.ultimo_spawn = tempo_atual

        # 2. Movimento dos Sprites
        # Captura as teclas pressionadas para atualizar especificamente a nave
        teclas = pygame.key.get_pressed()
        self.nave.update(teclas)
        
        # Atualiza a física de todos os outros sprites (tiros e asteroides)
        for sprite in self.todos_sprites:
            if sprite != self.nave:
                sprite.update()

        # 3. Processamento de Colisões
        # Colisão entre Projéteis e Asteroides:
        # groupcollide() remove ambos (True, True) em caso de sobreposição
        colisoes = pygame.sprite.groupcollide(self.projeteis, self.asteroides, True, True)
        if colisoes:
            # Aumenta a pontuação para cada asteroide destruído
            for asteroide_atingido in colisoes.values():
                self.pontos += len(asteroide_atingido)
            # Reavalia o nível de dificuldade
            self.gerenciar_dificuldade()

        # Colisão entre Nave do Jogador e Asteroides:
        # Finaliza o jogo se houver qualquer colisão direta
        colisao_nave = pygame.sprite.spritecollide(self.nave, self.asteroides, False)
        if colisao_nave:
            self.estado_atual = ESTADO_GAME_OVER

        # 4. Verificação de Condição de Game Over por Fuga
        # Se algum asteroide cruzar a borda inferior da tela, o jogador perde
        for asteroide in self.asteroides:
            if asteroide.rect.top > ALTURA_TELA:
                self.estado_atual = ESTADO_GAME_OVER
                break

    def processar_eventos(self):
        """
        Captura e interpreta eventos do sistema (teclado e fechamento da janela).
        """
        for evento in pygame.event.get():
            # Evento de fechar a janela do jogo
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # Detecção de pressionamento de teclas únicas (não contínuas)
            elif evento.type == pygame.KEYDOWN:
                # Sair do jogo ao pressionar a tecla ESC
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                # Processamento de teclas baseado no estado atual
                if self.estado_atual == ESTADO_MENU:
                    # Inicia o jogo se pressionar a Barra de Espaço na tela inicial
                    if evento.key == pygame.K_SPACE:
                        self.reiniciar_jogo()
                        
                elif self.estado_atual == ESTADO_JOGANDO:
                    # Permite disparar tiros imediatos pressionando a Barra de Espaço
                    if evento.key == pygame.K_SPACE:
                        self.disparar_projetil()
                        
                elif self.estado_atual == ESTADO_GAME_OVER:
                    # Reinicia a partida ao pressionar a tecla R
                    if evento.key == pygame.K_r:
                        self.reiniciar_jogo()

    def desenhar(self):
        """
        Renderiza todos os elementos visuais na janela de jogo de acordo com o estado.
        """
        # Limpa a tela desenhando o fundo preto estilo espaço Atari
        self.tela.fill(COR_FUNDO)
        
        if self.estado_atual == ESTADO_MENU:
            # ---- TELA DE MENU INICIAL ----
            # Renderiza o Título Principal
            texto_titulo = self.fonte_titulo.render("ATARI SPACE GAME", True, COR_TEXTO)
            rect_titulo = texto_titulo.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 3))
            self.tela.blit(texto_titulo, rect_titulo)
            
            # Efeito piscante simples para o subtítulo baseado no tempo do sistema (a cada 500ms)
            if pygame.time.get_ticks() % 1000 < 600:
                texto_instrucao = self.fonte_subtitulo.render("PRESSIONE ESPACO PARA INICIAR", True, COR_TEXTO)
                rect_instrucao = texto_instrucao.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 + 50))
                self.tela.blit(texto_instrucao, rect_instrucao)
                
            # Renderiza as instruções de controle básicas
            texto_controles = self.fonte_subtitulo.render("Setas: Mover | Espaco: Atirar", True, COR_TEXTO)
            rect_controles = texto_controles.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA - 100))
            self.tela.blit(texto_controles, rect_controles)

        elif self.estado_atual == ESTADO_JOGANDO:
            # ---- TELA DE JOGABILIDADE ATIVA ----
            # Desenha todos os sprites do jogo na tela (Nave, Tiros, Asteroides)
            self.todos_sprites.draw(self.tela)
            
            # Renderiza a pontuação atual no canto superior esquerdo
            # O texto da pontuação formata o placar com zeros à esquerda (ex: SCORE: 0005)
            texto_score = self.fonte_placar.render(f"SCORE: {self.pontos:04d}", True, COR_TEXTO)
            self.tela.blit(texto_score, (20, 20))
            
            # Exibe o nível atual do jogo logo abaixo da pontuação
            texto_nivel = self.fonte_subtitulo.render(f"LEVEL: {self.nivel}", True, COR_TEXTO)
            self.tela.blit(texto_nivel, (20, 55))

        elif self.estado_atual == ESTADO_GAME_OVER:
            # ---- TELA DE GAME OVER (FIM DE JOGO) ----
            # Mensagem de Game Over em vermelho vibrante
            texto_game_over = self.fonte_titulo.render("GAME OVER", True, COR_GAME_OVER)
            rect_game_over = texto_game_over.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 3))
            self.tela.blit(texto_game_over, rect_game_over)
            
            # Placar final obtido
            texto_final_score = self.fonte_placar.render(f"PONTUACAO FINAL: {self.pontos:04d}", True, COR_TEXTO)
            rect_final_score = texto_final_score.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2))
            self.tela.blit(texto_final_score, rect_final_score)
            
            # Instruções para reiniciar ou fechar
            texto_reiniciar = self.fonte_subtitulo.render("PRESSIONE 'R' PARA REINICIAR OU 'ESC' PARA SAIR", True, COR_TEXTO)
            rect_reiniciar = texto_reiniciar.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA * 2 // 3))
            self.tela.blit(texto_reiniciar, rect_reiniciar)

        # Atualiza o buffer da tela inteira (Double Buffering)
        pygame.display.flip()

    def iniciar(self):
        """
        Método de entrada principal do loop do jogo.
        Mantém o jogo rodando a 60 FPS fixos.
        """
        while True:
            # Captura a entrada do usuário
            self.processar_eventos()
            
            # Atualiza o estado lógico apenas se estiver ativamente jogando
            if self.estado_atual == ESTADO_JOGANDO:
                # Disparo contínuo com base em teclado segurado
                teclas = pygame.key.get_pressed()
                if teclas[pygame.K_SPACE]:
                    self.disparar_projetil()
                    
                self.atualizar()
                
            # Renderiza os gráficos atualizados
            self.desenhar()
            
            # Garante que o loop execute no máximo a 60 vezes por segundo (FPS)
            self.clock.tick(FPS)

# Ponto de entrada padrão do interpretador Python
if __name__ == "__main__":
    jogo = Jogo()
    jogo.iniciar()
