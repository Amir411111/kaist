"""
Логика пленных персонажей
"""

import pygame
from settings import *
from utils import create_male_character_sprite

class Captive:
    def __init__(self, x, y, character_id):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.character_id = character_id
        self.freed = False
        
        # Имена мужских героев
        self.names = {
            1: "Sanzhar",
            2: "Erkosh", 
            3: "Aibek"
        }
        
        # Создаем спрайт пленного (уменьшенная версия мужского персонажа)
        self.sprite = create_male_character_sprite(str(character_id))
        self.sprite = pygame.transform.scale(self.sprite, (32, 32))
        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def draw(self, surface):
        """
        Отрисовывает пленного персонажа
        """
        if not self.freed:
            surface.blit(self.sprite, (self.x, self.y))
    
    def is_freed(self):
        """
        Проверяет, освобожден ли пленный
        """
        return self.freed
    
    def free(self):
        """
        Освобождает пленного
        """
        self.freed = True 