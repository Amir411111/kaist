"""
Экран выбора персонажа
"""

import pygame
from settings import *
from utils import draw_text, create_character_sprite

class CharacterSelectScreen:
    def __init__(self):
        self.selected_character = 1
        self.characters = [
            {"id": 1, "name": "Kamilla", "color": BLUE, "sprite": create_character_sprite(BLUE, "1")},
            {"id": 2, "name": "Dana", "color": GREEN, "sprite": create_character_sprite(GREEN, "2")},
            {"id": 3, "name": "Moldir", "color": CYAN, "sprite": create_character_sprite(CYAN, "3")}
        ]
        
        # Позиции персонажей
        self.character_positions = [
            (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2),
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            (3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        ]
        
        # Защита от спама нажатий
        self.key_cooldown = 0
        self.cooldown_time = 10  # кадров между нажатиями
    
    def handle_input(self, keys):
        """
        Обрабатывает ввод на экране выбора
        """
        # Обновляем таймер кулдауна
        if self.key_cooldown > 0:
            self.key_cooldown -= 1
            
        # Обрабатываем нажатия только если кулдаун закончился
        if self.key_cooldown == 0:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.selected_character = max(1, self.selected_character - 1)
                self.key_cooldown = self.cooldown_time
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.selected_character = min(3, self.selected_character + 1)
                self.key_cooldown = self.cooldown_time
            elif keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
                return self.selected_character
        return None
    
    def draw(self, surface):
        """
        Отрисовывает экран выбора персонажа
        """
        # Фон
        surface.fill(DARK_GRAY)
        
        # Заголовок
        draw_text(surface, "CHOOSE YOUR HEROINE", 56, WHITE, SCREEN_WIDTH // 2, 100, center=True)
        
        # Отрисовка персонажей
        for i, character in enumerate(self.characters):
            x, y = self.character_positions[i]
            
            # Подсветка выбранного персонажа
            if character["id"] == self.selected_character:
                # Рамка вокруг выбранного персонажа (подгоняем под новый размер)
                frame_size = PLAYER_WIDTH + 20  # Рамка больше персонажа на 20 пикселей
                frame_offset = frame_size // 2
                pygame.draw.rect(surface, YELLOW, (x - frame_offset, y - frame_offset, frame_size, frame_size), 4)
            
            # Спрайт персонажа (центрируем спрайт)
            sprite_offset = PLAYER_WIDTH // 2  # 64 // 2 = 32
            surface.blit(character["sprite"], (x - sprite_offset, y - sprite_offset))
            
            # Имя персонажа
            draw_text(surface, character["name"], 28, WHITE, x, y + 50, center=True)
        
        # Инструкции
        draw_text(surface, "Use arrow keys to select", 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150, center=True)
        draw_text(surface, "Press ENTER to confirm", 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120, center=True)
        
        # Информация о персонажах
        draw_text(surface, "All heroines have the same abilities", 20, LIGHT_GRAY, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80, center=True)
        draw_text(surface, "Differences are only in appearance", 20, LIGHT_GRAY, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60, center=True)
    
    def get_selected_character(self):
        """
        Возвращает ID выбранного персонажа
        """
        return self.selected_character 