"""
Логика финального босса
"""

import pygame
import random
from settings import *
from utils import create_boss_sprite, create_fireball_sprite

class Fireball:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16
        self.direction = direction  # 1 - вправо, -1 - влево
        self.speed = 5
        
        self.sprite = create_fireball_sprite()
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.alive = True
    
    def update(self):
        """
        Обновляет состояние огненного шара
        """
        self.x += self.speed * self.direction
        self.rect.x = self.x
        
        # Уничтожаем, если вышел за границы экрана
        if self.x < 0 or self.x > SCREEN_WIDTH:
            self.alive = False
    
    def draw(self, surface):
        """
        Отрисовывает огненный шар
        """
        if self.alive:
            surface.blit(self.sprite, (self.x, self.y))
    
    def check_collision_with_player(self, player):
        """
        Проверяет коллизию с игроком
        """
        if self.alive and player.rect.colliderect(self.rect):
            self.alive = False
            return True
        return False

class Boss:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = BOSS_WIDTH
        self.height = BOSS_HEIGHT
        
        # Состояние
        self.lives = BOSS_LIVES
        self.alive = True
        self.invulnerable = False
        self.invulnerable_timer = 0
        
        # Движение
        self.direction = 1
        self.patrol_left = 100
        self.patrol_right = SCREEN_WIDTH - 100
        
        # Атака
        self.fireballs = []
        self.attack_timer = 0
        self.attack_cooldown = 120  # 2 секунды при 60 FPS
        
        # Спрайт
        self.sprite = create_boss_sprite()
        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def update(self, platforms, player):
        """
        Обновляет состояние босса
        """
        if not self.alive:
            return
        
        # Движение босса
        self.x += BOSS_SPEED * self.direction
        
        # Проверка границ патрулирования
        if self.x <= self.patrol_left:
            self.x = self.patrol_left
            self.direction = 1
        elif self.x >= self.patrol_right:
            self.x = self.patrol_right
            self.direction = -1
        
        # Обновление прямоугольника коллизии
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Проверка коллизий с платформами
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Коллизия слева
                if self.direction > 0 and self.rect.right > platform.rect.left and self.rect.left < platform.rect.left:
                    self.rect.right = platform.rect.left
                    self.x = self.rect.x
                    self.direction = -1
                # Коллизия справа
                elif self.direction < 0 and self.rect.left < platform.rect.right and self.rect.right > platform.rect.right:
                    self.rect.left = platform.rect.right
                    self.x = self.rect.x
                    self.direction = 1
        
        # Атака огненными шарами
        self.attack_timer += 1
        if self.attack_timer >= self.attack_cooldown:
            self.attack()
            self.attack_timer = 0
        
        # Обновление огненных шаров
        for fireball in self.fireballs[:]:
            fireball.update()
            if not fireball.alive:
                self.fireballs.remove(fireball)
            elif fireball.check_collision_with_player(player):
                self.fireballs.remove(fireball)
        
        # Обновление неуязвимости
        if self.invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
    
    def attack(self):
        """
        Босс атакует огненными шарами
        """
        # Создаем огненный шар в направлении движения босса
        fireball_x = self.x + (self.width if self.direction > 0 else 0)
        fireball_y = self.y + self.height // 2
        
        fireball = Fireball(fireball_x, fireball_y, self.direction)
        self.fireballs.append(fireball)
    
    def take_damage(self):
        """
        Босс получает урон
        """
        if not self.invulnerable:
            self.lives -= 1
            self.invulnerable = True
            self.invulnerable_timer = 60  # 1 секунда при 60 FPS
            
            if self.lives <= 0:
                self.alive = False
    
    def check_collision_with_player(self, player):
        """
        Проверяет коллизию с игроком
        """
        if not self.alive:
            return False
        
        # Проверяем, прыгнул ли игрок на босса сверху
        if (player.rect.bottom <= self.rect.top + 10 and 
            player.vel_y > 0 and 
            player.rect.right > self.rect.left and 
            player.rect.left < self.rect.right):
            self.take_damage()
            player.vel_y = JUMP_SPEED // 2  # Отскок от босса
            return True
        
        # Обычная коллизия (игрок получает урон)
        if player.rect.colliderect(self.rect):
            return True
        
        return False
    
    def draw(self, surface):
        """
        Отрисовывает босса
        """
        if not self.alive:
            return
        
        # Мигание при неуязвимости
        if self.invulnerable and self.invulnerable_timer % 10 < 5:
            return
        
        surface.blit(self.sprite, (self.x, self.y))
        
        # Отрисовка жизней босса
        for i in range(self.lives):
            pygame.draw.circle(surface, RED, (SCREEN_WIDTH - 30 - i * 25, 30), 10)
            pygame.draw.circle(surface, BLACK, (SCREEN_WIDTH - 30 - i * 25, 30), 10, 2)
        
        # Отрисовка огненных шаров
        for fireball in self.fireballs:
            fireball.draw(surface)
    
    def is_alive(self):
        """
        Проверяет, жив ли босс
        """
        return self.alive 