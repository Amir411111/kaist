"""
Настройки игры - основные параметры и константы
"""

# Размеры окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)

# Физика
GRAVITY = 0.8
JUMP_SPEED = -15
PLAYER_SPEED = 5
ENEMY_SPEED = 2
BOSS_SPEED = 1

# Размеры объектов
PLAYER_WIDTH = 32
PLAYER_HEIGHT = 32
ENEMY_WIDTH = 32
ENEMY_HEIGHT = 32
BOSS_WIDTH = 64
BOSS_HEIGHT = 64
TILE_SIZE = 32

# Игровые параметры
PLAYER_LIVES = 3
BOSS_LIVES = 3

# Состояния игры
STATE_MENU = "menu"
STATE_SELECT_CHARACTER = "select_character"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
STATE_VICTORY = "victory"

# Уровни
LEVEL_1 = 1
LEVEL_2 = 2
LEVEL_3 = 3

# FPS
FPS = 60 