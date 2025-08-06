"""
Вспомогательные функции для игры
"""

import pygame
import os
from settings import *

def load_image(path, size=None):
    """
    Загружает изображение из файла или создает заглушку
    """
    try:
        if os.path.exists(path):
            image = pygame.image.load(path)
            if size:
                image = pygame.transform.scale(image, size)
            return image
        else:
            # Создаем заглушку
            surface = pygame.Surface((32, 32))
            surface.fill(BLUE)
            pygame.draw.rect(surface, BLACK, (0, 0, 32, 32), 2)
            if size:
                surface = pygame.transform.scale(surface, size)
            return surface
    except:
        # Создаем заглушку в случае ошибки
        surface = pygame.Surface((32, 32))
        surface.fill(RED)
        pygame.draw.rect(surface, BLACK, (0, 0, 32, 32), 2)
        if size:
            surface = pygame.transform.scale(surface, size)
        return surface

def load_sound(path):
    """
    Загружает звук из файла или создает заглушку
    """
    try:
        if os.path.exists(path):
            return pygame.mixer.Sound(path)
        else:
            # Создаем пустой звук
            return pygame.mixer.Sound(buffer=bytes([]))
    except:
        return pygame.mixer.Sound(buffer=bytes([]))

def draw_text(surface, text, font_size, color, x, y, center=False):
    """
    Отрисовывает текст на поверхности
    """
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    
    surface.blit(text_surface, text_rect)

def create_character_sprite(color, character_id="1"):
    """
    Создает спрайт персонажа, загружая изображение из файла или создавая заглушку
    """
    # Маппинг ID персонажей к файлам
    character_files = {
        "1": "assets/characters/female_1.png",
        "2": "assets/characters/female_2.png", 
        "3": "assets/characters/female_3.png"
    }
    
    # Пытаемся загрузить изображение персонажа
    if character_id in character_files:
        character_path = character_files[character_id]
        print(f"DEBUG: Loading character {character_id} from {character_path}")
        if os.path.exists(character_path):
            try:
                image = pygame.image.load(character_path)
                print(f"DEBUG: Original size: {image.get_size()}")
                # Масштабируем изображение под размер игрока
                image = pygame.transform.scale(image, (PLAYER_WIDTH, PLAYER_HEIGHT))
                print(f"DEBUG: Scaled to: {PLAYER_WIDTH}x{PLAYER_HEIGHT}")
                return image
            except Exception as e:
                print(f"DEBUG: Error loading image: {e}")
    
    # Если не удалось загрузить - создаем яркую заглушку для отладки
    print(f"DEBUG: Creating bright fallback sprite for character {character_id}")
    surface = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
    surface.fill(YELLOW)  # Яркий желтый для видимости
    pygame.draw.rect(surface, RED, (0, 0, PLAYER_WIDTH, PLAYER_HEIGHT), 4)
    
    # Добавляем крупный текст
    font = pygame.font.Font(None, 36)
    text_surface = font.render(str(character_id), True, BLACK)
    text_rect = text_surface.get_rect(center=(PLAYER_WIDTH//2, PLAYER_HEIGHT//2))
    surface.blit(text_surface, text_rect)
    
    return surface

def create_tile_sprite():
    """
    Создает спрайт тайла земли
    """
    surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
    surface.fill(GREEN)
    pygame.draw.rect(surface, BLACK, (0, 0, TILE_SIZE, TILE_SIZE), 1)
    return surface

def create_enemy_sprite():
    """
    Создает спрайт врага, загружая изображение из файла
    """
    enemy_path = "assets/enemies/enemy.png"
    
    # Пытаемся загрузить изображение врага
    if os.path.exists(enemy_path):
        try:
            image = pygame.image.load(enemy_path)
            # Масштабируем изображение под размер врага
            image = pygame.transform.scale(image, (ENEMY_WIDTH, ENEMY_HEIGHT))
            return image
        except Exception as e:
            print(f"DEBUG: Error loading enemy image: {e}")
    
    # Если не удалось загрузить - создаем заглушку
    surface = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
    surface.fill(RED)
    pygame.draw.rect(surface, BLACK, (0, 0, ENEMY_WIDTH, ENEMY_HEIGHT), 2)
    
    # Добавляем текст "ВРАГ"
    font = pygame.font.Font(None, 20)
    text_surface = font.render("ВРАГ", True, WHITE)
    text_rect = text_surface.get_rect(center=(ENEMY_WIDTH//2, ENEMY_HEIGHT//2))
    surface.blit(text_surface, text_rect)
    
    return surface

def create_boss_sprite():
    """
    Создает спрайт босса, загружая изображение из файла
    """
    boss_path = "assets/enemies/enemy.png"
    
    # Пытаемся загрузить изображение босса (используем ту же текстуру что и у врагов)
    if os.path.exists(boss_path):
        try:
            image = pygame.image.load(boss_path)
            # Масштабируем изображение под размер босса (64x64)
            image = pygame.transform.scale(image, (BOSS_WIDTH, BOSS_HEIGHT))
            return image
        except Exception as e:
            print(f"DEBUG: Error loading boss image: {e}")
    
    # Если не удалось загрузить - создаем заглушку
    surface = pygame.Surface((BOSS_WIDTH, BOSS_HEIGHT))
    surface.fill(MAGENTA)
    pygame.draw.rect(surface, BLACK, (0, 0, BOSS_WIDTH, BOSS_HEIGHT), 3)
    
    # Добавляем текст "БОСС"
    font = pygame.font.Font(None, 24)
    text_surface = font.render("БОСС", True, WHITE)
    text_rect = text_surface.get_rect(center=(BOSS_WIDTH//2, BOSS_HEIGHT//2))
    surface.blit(text_surface, text_rect)
    
    return surface

def create_fireball_sprite():
    """
    Создает спрайт огненного шара
    """
    surface = pygame.Surface((16, 16))
    surface.fill(YELLOW)
    pygame.draw.circle(surface, RED, (8, 8), 6)
    return surface 