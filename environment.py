import numpy as np
import random
from settings import *

class TicTacToeEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        """Reinicia o tabuleiro para o estado vazio."""
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.done = False
        self.winner = None
        return self.board.flatten() # Retorna o estado inicial

    def is_valid_move(self, action):
        """Verifica se a célula está dentro do grid e vazia."""
        row, col = divmod(action, BOARD_SIZE)
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return self.board[row, col] == EMPTY
        return False

    def check_winner(self, player_id):
        """
        Verifica vitória com Janela Deslizante.
        Como o tabuleiro é 4x4 e precisamos de 3 em linha,
        verificamos sub-sequências de tamanho 3.
        """
        b = self.board
        n = BOARD_SIZE
        target = WIN_LENGTH # 3

        # 1. Verificar Linhas e Colunas
        for i in range(n):
            # Linha i: verifica colunas (0,1,2) e (1,2,3)
            row = b[i, :]
            for j in range(n - target + 1):
                if np.all(row[j:j+target] == player_id):
                    return True
            
            # Coluna i: verifica linhas (0,1,2) e (1,2,3)
            col = b[:, i]
            for j in range(n - target + 1):
                if np.all(col[j:j+target] == player_id):
                    return True

        # 2. Verificar Diagonais
        # Precisamos varrer janelas 3x3 dentro do grid 4x4
        # Um grid 4x4 contém quatro subgrids 3x3 possíveis.
        
        # Lista de coordenadas iniciais (top-left) de janelas 3x3 possíveis
        # (0,0), (0,1), (1,0), (1,1)
        for r in range(n - target + 1):
            for c in range(n - target + 1):
                # Pega a submatriz 3x3
                subgrid = b[r:r+target, c:c+target]
                
                # Verifica diagonal principal da submatriz
                if np.all(subgrid.diagonal() == player_id):
                    return True
                
                # Verifica diagonal secundária da submatriz (flip na horizontal)
                if np.all(np.fliplr(subgrid).diagonal() == player_id):
                    return True

        return False

    def is_draw(self):
        """Verifica se não há mais espaços vazios."""
        return not np.any(self.board == EMPTY)

    def play_opponents(self):
        """
        Simula a jogada dos oponentes 2, 3 e 4 sequencialmente.
        Estratégia atual: Aleatória (Random Walk).
        """
        if self.done: return

        for opp_id in OPPONENTS:
            # Encontrar todas as células vazias
            empty_cells = np.argwhere(self.board == EMPTY)
            
            if len(empty_cells) == 0:
                self.done = True
                return

            # Escolhe uma célula aleatória
            choice = random.choice(empty_cells)
            self.board[choice[0], choice[1]] = opp_id

            # Verifica se esse oponente ganhou
            if self.check_winner(opp_id):
                self.winner = opp_id
                self.done = True
                return
            
            # Verifica empate após jogada
            if self.is_draw():
                self.done = True
                return

    def step(self, action):
        """
        Executa um passo completo do jogo (Turno Agente + Turno Oponentes).
        """
        # Se o jogo já acabou, reseta (segurança)
        if self.done:
            return self.board.flatten(), 0, True, {}

        # 1. AÇÃO DO AGENTE
        if not self.is_valid_move(action):
            return self.board.flatten(), REWARDS['INVALID'], self.done, {'error': 'Invalid Move'}

        row, col = divmod(action, BOARD_SIZE)
        self.board[row, col] = AGENT_ID

        # 2. VERIFICA VITÓRIA DO AGENTE
        if self.check_winner(AGENT_ID):
            self.done = True
            self.winner = AGENT_ID
            return self.board.flatten(), REWARDS['WIN'], True, {'result': 'Win'}

        # 3. VERIFICA EMPATE
        if self.is_draw():
            self.done = True
            return self.board.flatten(), REWARDS['DRAW'], True, {'result': 'Draw'}

        # 4. TURNOS DOS OPONENTES
        self.play_opponents()

        # 5. AVALIAÇÃO FINAL APÓS OPONENTES
        if self.done:
            if self.winner in OPPONENTS:
                return self.board.flatten(), REWARDS['LOSS'], True, {'result': 'Loss'}
            else:
                # Caso raro: Empate aconteceu durante turno do oponente
                return self.board.flatten(), REWARDS['DRAW'], True, {'result': 'Draw'}

        # Se ninguém ganhou, jogo segue
        return self.board.flatten(), REWARDS['STEP'], False, {}