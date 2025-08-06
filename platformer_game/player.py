"""
Логика игрока
"""

import pygame
from settings import *
from utils import create_character_sprite

class Player:
    def __init__(self, x, y, character_id=1):
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.character_id = character_id
        
        # Физика
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        
        # Состояние
        self.lives = PLAYER_LIVES
        self.invulnerable = False
        self.invulnerable_timer = 0
        
        # Спрайты персонажей
        self.sprites = {
            1: create_character_sprite(BLUE, "1"),
            2: create_character_sprite(GREEN, "2"),
            3: create_character_sprite(CYAN, "3")
        }
        
        self.current_sprite = self.sprites[character_id]
        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def update(self, platforms, enemies=None, boss=None):
        """
        Обновляет состояние игрока
        """
        # Гравитация
        self.vel_y += GRAVITY
        
        # Ограничение скорости падения
        if self.vel_y > 20:
            self.vel_y = 20
        
        # Обновление позиции
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Обновление прямоугольника коллизии
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Проверка коллизий с платформами
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Коллизия снизу (игрок на платформе)
                if self.vel_y > 0 and self.rect.bottom > platform.rect.top and self.rect.top < platform.rect.top:
                    self.rect.bottom = platform.rect.top
                    self.y = self.rect.y
                    self.vel_y = 0
                    self.on_ground = True
                # Коллизия сверху
                elif self.vel_y < 0 and self.rect.top < platform.rect.bottom and self.rect.bottom > platform.rect.bottom:
                    self.rect.top = platform.rect.bottom
                    self.y = self.rect.y
                    self.vel_y = 0
                # Коллизия слева
                elif self.vel_x > 0 and self.rect.right > platform.rect.left and self.rect.left < platform.rect.left:
                    self.rect.right = platform.rect.left
                    self.x = self.rect.x
                    self.vel_x = 0
                # Коллизия справа
                elif self.vel_x < 0 and self.rect.left < platform.rect.right and self.rect.right > platform.rect.right:
                    self.rect.left = platform.rect.right
                    self.x = self.rect.x
                    self.vel_x = 0
        
        # Проверка коллизий с врагами
        if enemies:
            for enemy in enemies:
                if self.rect.colliderect(enemy.rect) and not self.invulnerable:
                    self.take_damage()
        
        # Проверка коллизий с боссом обрабатывается в level.py
        
        # Обновление неуязвимости
        if self.invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
        
        # Проверка выхода за границы экрана
        if self.y > SCREEN_HEIGHT:
            self.take_damage()
            self.reset_position()
    
    def handle_input(self, keys):
        """
        Обрабатывает ввод игрока
        """
        self.vel_x = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = PLAYER_SPEED
        if (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]) and self.on_ground:
            self.jump()
    
    def jump(self):
        """
        Прыжок игрока
        """
        if self.on_ground:
            self.vel_y = JUMP_SPEED
            self.on_ground = False
    
    def take_damage(self):
        """
        Игрок получает урон
        """
        if not self.invulnerable:
            self.lives -= 1
            self.invulnerable = True
            self.invulnerable_timer = 60  # 1 секунда при 60 FPS
    
    def reset_position(self):
        """
        Сбрасывает позицию игрока
        """
        self.x = 100
        self.y = 300
        self.vel_x = 0
        self.vel_y = 0
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self, surface):
        """
        Отрисовывает игрока
        """
        # Мигание при неуязвимости
        if self.invulnerable and self.invulnerable_timer % 10 < 5:
            return
        
        surface.blit(self.current_sprite, (self.x, self.y))
        
        # Отрисовка жизней
        for i in range(self.lives):
            pygame.draw.circle(surface, RED, (30 + i * 25, 30), 10)
            pygame.draw.circle(surface, BLACK, (30 + i * 25, 30), 10, 2)
    
    def is_alive(self):
        """
        Проверяет, жив ли игрок
        """
        return self.lives > 0
    
    def change_character(self, character_id):
        """
        Меняет персонажа
        """
        if character_id in self.sprites:
            self.character_id = character_id
            self.current_sprite = self.sprites[character_id] 