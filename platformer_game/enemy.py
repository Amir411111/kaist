"""
Логика обычных врагов
"""

import pygame
from settings import *
from utils import create_enemy_sprite

class Enemy:
    def __init__(self, x, y, patrol_left, patrol_right):
        self.x = x
        self.y = y
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        
        # Патрулирование
        self.patrol_left = patrol_left
        self.patrol_right = patrol_right
        self.direction = 1  # 1 - вправо, -1 - влево
        
        # Физика
        self.vel_x = ENEMY_SPEED
        self.vel_y = 0
        
        # Состояние
        self.alive = True
        
        # Спрайт
        self.sprite = create_enemy_sprite()
        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def update(self, platforms):
        """
        Обновляет состояние врага
        """
        if not self.alive:
            return
        
        # Гравитация
        self.vel_y += GRAVITY
        
        # Ограничение скорости падения
        if self.vel_y > 20:
            self.vel_y = 20
        
        # Движение по горизонтали
        self.x += self.vel_x * self.direction
        
        # Проверка границ патрулирования
        if self.x <= self.patrol_left:
            self.x = self.patrol_left
            self.direction = 1
        elif self.x >= self.patrol_right:
            self.x = self.patrol_right
            self.direction = -1
        
        # Обновление позиции по вертикали
        self.y += self.vel_y
        
        # Обновление прямоугольника коллизии
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Проверка коллизий с платформами
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Коллизия снизу (враг на платформе)
                if self.vel_y > 0 and self.rect.bottom > platform.rect.top and self.rect.top < platform.rect.top:
                    self.rect.bottom = platform.rect.top
                    self.y = self.rect.y
                    self.vel_y = 0
                # Коллизия сверху
                elif self.vel_y < 0 and self.rect.top < platform.rect.bottom and self.rect.bottom > platform.rect.bottom:
                    self.rect.top = platform.rect.bottom
                    self.y = self.rect.y
                    self.vel_y = 0
                # Коллизия слева
                elif self.vel_x > 0 and self.rect.right > platform.rect.left and self.rect.left < platform.rect.left:
                    self.rect.right = platform.rect.left
                    self.x = self.rect.x
                    self.direction = -1
                # Коллизия справа
                elif self.vel_x < 0 and self.rect.left < platform.rect.right and self.rect.right > platform.rect.right:
                    self.rect.left = platform.rect.right
                    self.x = self.rect.x
                    self.direction = 1
        
        # Проверка выхода за границы экрана
        if self.y > SCREEN_HEIGHT:
            self.alive = False
    
    def take_damage(self):
        """
        Враг получает урон (умирает)
        """
        self.alive = False
    
    def check_collision_with_player(self, player):
        """
        Проверяет коллизию с игроком
        """
        if not self.alive:
            return False
        
        # Проверяем, прыгнул ли игрок на врага сверху
        if (player.rect.bottom <= self.rect.top + 10 and 
            player.vel_y > 0 and 
            player.rect.right > self.rect.left and 
            player.rect.left < self.rect.right):
            self.take_damage()
            player.vel_y = JUMP_SPEED // 2  # Отскок от врага
            return True
        
        # Обычная коллизия (игрок получает урон)
        if player.rect.colliderect(self.rect):
            return True
        
        return False
    
    def draw(self, surface):
        """
        Отрисовывает врага
        """
        if self.alive:
            surface.blit(self.sprite, (self.x, self.y))
    
    def is_alive(self):
        """
        Проверяет, жив ли враг
        """
        return self.alive 