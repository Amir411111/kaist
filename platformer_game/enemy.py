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
        if self.vel_y > MAX_FALL_SPEED:
            self.vel_y = MAX_FALL_SPEED
        
        # Сохраняем старую позицию для проверки края платформы
        old_x = self.x
        
        # Движение по горизонтали
        self.x += self.vel_x * self.direction
        
        # Проверка границ патрулирования
        if self.x <= self.patrol_left:
            self.x = self.patrol_left
            self.direction = 1
        elif self.x >= self.patrol_right:
            self.x = self.patrol_right
            self.direction = -1
        
        # Проверка края платформы - враг НЕ должен падать!
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Проверяем, есть ли платформа под ногами врага в новой позиции
        future_bottom_rect = pygame.Rect(
            self.x + (self.width if self.direction > 0 else -5),  # Смотрим на край в направлении движения
            self.y + self.height,  # Под ногами
            5, 10  # Небольшой прямоугольник для проверки
        )
        
        platform_found = False
        for platform in platforms:
            if future_bottom_rect.colliderect(platform.rect):
                platform_found = True
                break
        
        # Если платформы нет под ногами - разворачиваемся!
        if not platform_found:
            self.x = old_x  # Возвращаемся к старой позиции
            self.direction *= -1  # Разворачиваемся
        
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
        Проверяет коллизию с игроком и возвращает тип коллизии
        """
        if not self.alive:
            return None
        
        # Проверяем основную коллизию
        if not player.rect.colliderect(self.rect):
            return None
        
        # Определяем тип коллизии более точно
        player_center_x = player.rect.centerx
        player_bottom = player.rect.bottom
        enemy_top = self.rect.top
        enemy_center_x = self.rect.centerx
        
        # Проверяем, прыгнул ли игрок на врага сверху
        vertical_overlap = player_bottom - enemy_top
        horizontal_distance = abs(player_center_x - enemy_center_x)
        
        # Условия для успешной атаки прыжком:
        # 1. Игрок падает вниз (vel_y > 0)
        # 2. Небольшое вертикальное перекрытие (игрок почти сверху)
        # 3. Игрок не слишком далеко по горизонтали
        if (player.vel_y > 0 and 
            vertical_overlap <= 15 and 
            horizontal_distance <= self.width // 2 + 5):
            self.take_damage()
            player.vel_y = JUMP_SPEED // 2  # Отскок от врага
            return "enemy_killed"  # Успешная атака на врага
        
        # Обычная коллизия (игрок получает урон)
        return "player_damage"
    
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