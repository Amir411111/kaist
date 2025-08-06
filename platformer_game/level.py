"""
Логика уровней и платформ
"""

import pygame
from settings import *
from utils import create_tile_sprite
from enemy import Enemy
from boss import Boss

class Platform:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        
        # Создаем спрайт платформы
        self.sprite = create_tile_sprite()
    
    def draw(self, surface):
        """
        Отрисовывает платформу
        """
        # Отрисовываем тайлы для платформы
        for tile_x in range(0, self.width, TILE_SIZE):
            for tile_y in range(0, self.height, TILE_SIZE):
                surface.blit(self.sprite, (self.x + tile_x, self.y + tile_y))

class Level:
    def __init__(self, level_number):
        self.level_number = level_number
        self.platforms = []
        self.enemies = []
        self.boss = None
        self.background_color = None
        
        # Таймер для первого уровня (автозавершение)
        self.level_timer = 0
        
        # Создаем уровень в зависимости от номера
        self.create_level()
    
    def create_level(self):
        """
        Создает уровень в зависимости от номера
        """
        print(f"DEBUG: Creating level {self.level_number}")
        if self.level_number == LEVEL_1:
            print("DEBUG: Creating level 1")
            self.create_level_1()
        elif self.level_number == LEVEL_2:
            print("DEBUG: Creating level 2")
            self.create_level_2()
        elif self.level_number == LEVEL_3:
            print("DEBUG: Creating level 3")
            self.create_level_3()
    
    def create_level_1(self):
        """
        Создает первый уровень (обучение)
        """
        self.background_color = CYAN
        
        # Основная платформа
        self.platforms.append(Platform(0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
        
        # Несколько платформ для обучения прыжкам
        self.platforms.append(Platform(200, SCREEN_HEIGHT - 200, 100, 20))
        self.platforms.append(Platform(400, SCREEN_HEIGHT - 250, 100, 20))
        self.platforms.append(Platform(600, SCREEN_HEIGHT - 300, 100, 20))
    
    def create_level_2(self):
        """
        Создает второй уровень (враги и ямы)
        """
        self.background_color = GREEN
        
        # Основная платформа с ямами
        self.platforms.append(Platform(0, SCREEN_HEIGHT - 100, 200, 100))
        self.platforms.append(Platform(300, SCREEN_HEIGHT - 100, 200, 100))
        self.platforms.append(Platform(600, SCREEN_HEIGHT - 100, 200, 100))
        
        # Платформы для прыжков
        self.platforms.append(Platform(250, SCREEN_HEIGHT - 200, 100, 20))
        self.platforms.append(Platform(450, SCREEN_HEIGHT - 250, 100, 20))
        
        # Добавляем врагов (правильные границы платформ!)
        from enemy import Enemy
        # Платформа 1: x=250-350, y=SCREEN_HEIGHT-200, враг на высоте -230
        self.enemies.append(Enemy(260, SCREEN_HEIGHT - 230, 250, 340))
        # Платформа 2: x=450-550, y=SCREEN_HEIGHT-250, враг на высоте -280  
        self.enemies.append(Enemy(460, SCREEN_HEIGHT - 280, 450, 540))
    
    def create_level_3(self):
        """
        Создает третий уровень (битва с боссом)
        """
        self.background_color = RED
        
        # Основная платформа
        self.platforms.append(Platform(0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
        
        # Платформы для битвы с боссом
        self.platforms.append(Platform(100, SCREEN_HEIGHT - 200, 150, 20))
        self.platforms.append(Platform(550, SCREEN_HEIGHT - 200, 150, 20))
        self.platforms.append(Platform(300, SCREEN_HEIGHT - 300, 200, 20))
        
        # Добавляем босса
        from boss import Boss
        self.boss = Boss(SCREEN_WIDTH // 2 - BOSS_WIDTH // 2, SCREEN_HEIGHT - 200)
    
    def update(self, player):
        """
        Обновляет состояние уровня
        """
        # Обновляем врагов
        for enemy in self.enemies:
            enemy.update(self.platforms)
            # Проверяем коллизии с игроком
            collision_result = enemy.check_collision_with_player(player)
            if collision_result == "player_damage" and not player.invulnerable:
                player.take_damage()
            # При "enemy_killed" урон врага уже нанесен в check_collision_with_player
        
        # Обновляем босса
        if self.boss:
            self.boss.update(self.platforms, player)
            # Проверяем столкновение с боссом
            collision_result = self.boss.check_collision_with_player(player)
            if collision_result == "damage_player" and not player.invulnerable:
                # Игрок получает урон от касания босса
                player.take_damage()
            # При "damage_boss" урон босса уже нанесен в check_collision_with_player
            
            # Проверяем столкновения с огненными шарами босса
            for fireball in self.boss.fireballs[:]:  # Копируем список для безопасного удаления
                if fireball.check_collision_with_player(player) and not player.invulnerable:
                    player.take_damage()
    
    def draw(self, surface):
        """
        Отрисовывает уровень
        """
        # Отрисовываем фон
        surface.fill(self.background_color)
        
        # Отрисовываем платформы
        for platform in self.platforms:
            platform.draw(surface)
        
        # Отрисовываем врагов
        for enemy in self.enemies:
            enemy.draw(surface)
        
        # Отрисовываем босса
        if self.boss:
            self.boss.draw(surface)
    
    def get_enemies(self):
        """
        Возвращает список врагов
        """
        return self.enemies
    
    def get_boss(self):
        """
        Возвращает босса
        """
        return self.boss
    
    def is_completed(self, player=None, timer=0):
        """
        Проверяет, завершен ли уровень
        """
        if self.level_number == LEVEL_1:
            # Уровень 1 завершается только когда игрок дойдет до правого края экрана
            if player and player.x >= SCREEN_WIDTH - 50:
                return True
            return False
        
        elif self.level_number == LEVEL_2:
            # Уровень 2 завершается, когда все враги побеждены ИЛИ игрок дошел до правого края
            all_enemies_dead = all(not enemy.is_alive() for enemy in self.enemies)
            reached_end = player and player.x >= SCREEN_WIDTH - 50
            return all_enemies_dead or reached_end
        
        elif self.level_number == LEVEL_3:
            # Уровень 3 завершается, когда босс побежден
            return self.boss and not self.boss.is_alive()
        
        return False
    
    def get_enemies(self):
        """
        Возвращает список врагов
        """
        return self.enemies
    
    def get_boss(self):
        """
        Возвращает босса
        """
        return self.boss 