"""
settings.py
Arquivo de configuração global para o projeto Jogo da Velha 4 Jogadores.
Define constantes, regras e recompensas usadas pelo Ambiente e pelo Agente.
"""

# --- Dimensões e Regras ---
BOARD_SIZE = 4        # Tamanho do grid (4x4)
WIN_LENGTH = 3        # Quantas peças alinhar para ganhar (Regra ajustada para 4 jogadores)
NUM_PLAYERS = 4       # Total de jogadores (1 Agente + 3 Oponentes)

# --- Identificadores no Tabuleiro (Encoding) ---
# Usamos números inteiros para representar o estado no Numpy
EMPTY = 0
AGENT_ID = 1          # O Nosso Agente (IA)
OPPONENTS = [2, 3, 4] # IDs dos adversários

# --- Mapeamento Visual (Para debugging no terminal) ---
SYMBOLS = {
    EMPTY: '.',
    AGENT_ID: 'X',       # Agente é X
    2: 'O',              # Oponente 1
    3: '<',              # Oponente 2
    4: '^'               # Oponente 3
}

# --- Sistema de Recompensas (Reinforcement Learning) ---
# O Agente usa esses valores para saber se jogou bem ou mal
REWARDS = {
    'WIN': 10,          # Vitória: O objetivo máximo
    'LOSS': -10,        # Derrota: O que devemos evitar
    'DRAW': 0,          # Empate: Neutro (ou levemente negativo -1 se quiser incentivar agressividade)
    'INVALID': -50,     # Movimento Inválido: Punição severa (jogar em casa ocupada)
    'STEP': 0           # Custo por movimento (0 = sem pressa)
}

# --- Configurações de Treinamento (Fase 2) ---
EPISODES = 50_000       # Total de partidas para treino
LEARNING_RATE = 0.1     # Alpha: O quão rápido o agente substitui conhecimento antigo
DISCOUNT_FACTOR = 0.9   # Gamma: Importância de recompensas futuras
EPSILON_START = 1.0     # Começa 100% aleatório
EPSILON_MIN = 0.01      # Termina 1% aleatório
EPSILON_DECAY = 0.9995  # Taxa de decaimento da exploração