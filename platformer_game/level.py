"""
Логика уровней и платформ
"""

import pygame
from settings import *
from utils import create_tile_sprite
from enemy import Enemy
from boss import Boss
<<<<<<< HEAD
from captives import Captive
=======
>>>>>>> 34bd1fe0c9b62876c01efda95ef2c17266b3188d

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
<<<<<<< HEAD
        self.captives = []  # Пленные персонажи
=======
>>>>>>> 34bd1fe0c9b62876c01efda95ef2c17266b3188d
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
<<<<<<< HEAD
        Создает первый уровень (обучение с врагами)
=======
        Создает первый уровень (обучение)
>>>>>>> 34bd1fe0c9b62876c01efda95ef2c17266b3188d
        """
        self.background_color = CYAN
        
        # Основная платформа
        self.platforms.append(Platform(0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
        
        # Несколько платформ для обучения прыжкам
        self.platforms.append(Platform(200, SCREEN_HEIGHT - 200, 100, 20))
        self.platforms.append(Platform(400, SCREEN_HEIGHT - 250, 100, 20))
        self.platforms.append(Platform(600, SCREEN_HEIGHT - 300, 100, 20))
<<<<<<< HEAD
        
        # Добавляем врагов на первый уровень
        from enemy import Enemy
        # Враг на первой платформе
        self.enemies.append(Enemy(210, SCREEN_HEIGHT - 230, 200, 300))
        # Враг на второй платформе
        self.enemies.append(Enemy(410, SCREEN_HEIGHT - 280, 400, 500))
=======
>>>>>>> 34bd1fe0c9b62876c01efda95ef2c17266b3188d
    
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
<<<<<<< HEAD
        
        # Добавляем еще двух врагов на основные платформы
        
        self.enemies.append(Enemy(350, SCREEN_HEIGHT - 130, 300, 500))
    
    def create_level_3(self):
        """
        Создает третий уровень (битва с боссом и освобождение пленных)
=======
    
    def create_level_3(self):
        """
        Создает третий уровень (битва с боссом)
>>>>>>> 34bd1fe0c9b62876c01efda95ef2c17266b3188d
        """
        self.background_color = RED
        
        # Основная платформа
        self.platforms.append(Platform(0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
        
        # Платформы для битвы с боссом
        self.platforms.append(Platform(100, SCREEN_HEIGHT - 200, 150, 20))
        self.platforms.append(Platform(550, SCREEN_HEIGHT - 200, 150, 20))
        self.platforms.append(Platform(300, SCREEN_HEIGHT - 300, 200, 20))
        
<<<<<<< HEAD
        # Клетка с пленными персонажами (справа)
        self.platforms.append(Platform(650, SCREEN_HEIGHT - 150, 100, 50))
        
        # Добавляем пленных персонажей (мужские персонажи)
        self.captives.append(Captive(660, SCREEN_HEIGHT - 140, 1))  # male_1
        self.captives.append(Captive(690, SCREEN_HEIGHT - 140, 2))  # male_2
        self.captives.append(Captive(720, SCREEN_HEIGHT - 140, 3))  # male_3
        
=======
>>>>>>> 34bd1fe0c9b62876c01efda95ef2c17266b3188d
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
<<<<<<< HEAD
            # Проверяем столкновение с боссом (только для атаки прыжком)
            collision_result = self.boss.check_collision_with_player(player)
            # При "damage_boss" урон босса уже нанесен в check_collision_with_player
            # Убираем урон от касания босса - теперь только от огненных шаров
=======
            # Проверяем столкновение с боссом
            collision_result = self.boss.check_collision_with_player(player)
            if collision_result == "damage_player" and not player.invulnerable:
                # Игрок получает урон от касания босса
                player.take_damage()
            # При "damage_boss" урон босса уже нанесен в check_collision_with_player
>>>>>>> 34bd1fe0c9b62876c01efda95ef2c17266b3188d
            
            # Проверяем столкновения с огненными шарами босса
            for fireball in self.boss.fireballs[:]:  # Копируем список для безопасного удаления
                if fireball.check_collision_with_player(player) and not player.invulnerable:
                    player.take_damage()
<<<<<<< HEAD
        
        # Освобождаем пленных, если босс побежден
        if self.boss and not self.boss.is_alive():
            for captive in self.captives:
                captive.free()
=======
>>>>>>> 34bd1fe0c9b62876c01efda95ef2c17266b3188d
    
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
<<<<<<< HEAD
        
        # Отрисовываем пленных персонажей
        for captive in self.captives:
            captive.draw(surface)
            # Добавляем имена пленных персонажей
            if not captive.freed:
                from utils import draw_text
                name = captive.names.get(captive.character_id, f"Hero {captive.character_id}")
                draw_text(surface, name, 12, WHITE, captive.x + 16, captive.y - 10, center=True)
=======
>>>>>>> 34bd1fe0c9b62876c01efda95ef2c17266b3188d
    
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