"""
Основной цикл игры и переключение уровней
"""

import pygame
from settings import *
from player import Player
from level import Level
from select_screen import CharacterSelectScreen
from utils import draw_text

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Платформер - Спаси девушек!")
        self.clock = pygame.time.Clock()
        
        # Состояние игры
        self.state = STATE_SELECT_CHARACTER
        self.selected_character = 1
        self.current_level = 1
        self.player = None
        self.level = None
        self.level_timer = 0  # Таймер для автозавершения уровня 1
        
        # Экран выбора персонажа
        from select_screen import CharacterSelectScreen
        self.character_select = CharacterSelectScreen()
        
        # Звуки (заглушки)
        self.sounds = {
            "jump": None,
            "hit": None,
            "win": None,
            "lose": None
        }
    
    def start_new_game(self):
        """
        Начинает новую игру
        """
        self.current_level = 1
        self.level_timer = 0
        print(f"DEBUG: Starting new game with level {self.current_level}")
        self.player = Player(100, 300, self.selected_character)
        self.level = Level(self.current_level)
        print(f"DEBUG: Created level {self.level.level_number}")
        self.state = STATE_PLAYING
    
    def next_level(self):
        """
        Переходит к следующему уровню
        """
        self.current_level += 1
        if self.current_level <= 3:
            # Сбрасываем позицию игрока в начало нового уровня
            self.player.x = 100
            self.player.y = 300
            self.player.vel_x = 0
            self.player.vel_y = 0
            self.player.rect.x = self.player.x
            self.player.rect.y = self.player.y
            self.level = Level(self.current_level)
            # Сбрасываем таймер уровня
            self.level_timer = 0
            print(f"DEBUG: Moved to level {self.current_level}")
        else:
            self.state = STATE_VICTORY
            print("DEBUG: Game completed - Victory!")
    
    def game_over(self):
        """
        Обрабатывает окончание игры
        """
        self.state = STATE_GAME_OVER
    
    def restart_game(self):
        """
        Перезапускает игру
        """
        self.state = STATE_SELECT_CHARACTER
        self.selected_character = 1
        self.character_select.selected_character = 1
    
    def handle_events(self):
        """
        Обрабатывает события игры
        """
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == STATE_PLAYING:
                        self.state = STATE_SELECT_CHARACTER
                        self.restart_game()
                    elif self.state == STATE_GAME_OVER or self.state == STATE_VICTORY:
                        self.restart_game()
        
        return True
    
    def update(self):
        """
        Обновляет состояние игры
        """
        keys = pygame.key.get_pressed()
        
        # Обрабатываем выбор персонажа
        if self.state == STATE_SELECT_CHARACTER:
            selected = self.character_select.handle_input(keys)
            if selected:
                self.selected_character = selected
                self.start_new_game()
        
        elif self.state == STATE_PLAYING:
            # Обновляем игрока
            self.player.handle_input(keys)
            self.player.update(self.level.platforms, self.level.get_enemies(), self.level.get_boss())
            
            # Обновляем уровень
            self.level.update(self.player)
            
            # Обновляем таймер уровня
            self.level_timer += 1
            
            # Проверяем, жив ли игрок
            if not self.player.is_alive():
                self.game_over()
                return
            
            # Проверяем завершение уровня
            if self.level.is_completed(self.player, self.level_timer):
                self.next_level()
    
    def draw(self):
        """
        Отрисовывает игру
        """
        if self.state == STATE_SELECT_CHARACTER:
            self.character_select.draw(self.screen)
        
        elif self.state == STATE_PLAYING:
            # Отрисовываем уровень
            self.level.draw(self.screen)
            
            # Отрисовываем игрока
            self.player.draw(self.screen)
            
            # Отрисовываем информацию об уровне
            draw_text(self.screen, f"Уровень {self.current_level}", 24, WHITE, 10, 10)
            
            # Инструкции для первого уровня
            if self.current_level == 1:
                draw_text(self.screen, "Дойдите до правого края экрана!", 18, YELLOW, SCREEN_WIDTH // 2, 50, center=True)
                draw_text(self.screen, "Используйте стрелки/WASD для движения", 16, WHITE, SCREEN_WIDTH // 2, 80, center=True)
                draw_text(self.screen, "Пробел для прыжка", 16, WHITE, SCREEN_WIDTH // 2, 110, center=True)
            
            # Инструкции для других уровней
            elif self.current_level == 2:
                draw_text(self.screen, "Победите всех врагов ИЛИ дойдите до правого края!", 18, YELLOW, SCREEN_WIDTH // 2, 50, center=True)
                draw_text(self.screen, "Прыгайте на врагов сверху", 16, WHITE, SCREEN_WIDTH // 2, 80, center=True)
            elif self.current_level == 3:
                draw_text(self.screen, "Победите босса-бегемота!", 18, RED, SCREEN_WIDTH // 2, 50, center=True)
                draw_text(self.screen, "Прыгайте на босса сверху 3 раза", 16, WHITE, SCREEN_WIDTH // 2, 80, center=True)
                draw_text(self.screen, "Избегайте огненных шаров", 16, WHITE, SCREEN_WIDTH // 2, 110, center=True)
        
        elif self.state == STATE_GAME_OVER:
            self.draw_game_over()
        
        elif self.state == STATE_VICTORY:
            self.draw_victory()
        
        pygame.display.flip()
    
    def draw_game_over(self):
        """
        Отрисовывает экран окончания игры
        """
        self.screen.fill(BLACK)
        
        draw_text(self.screen, "ИГРА ОКОНЧЕНА", 48, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, center=True)
        draw_text(self.screen, "Нажмите ESC для возврата в меню", 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, center=True)
    
    def draw_victory(self):
        """
        Отрисовывает экран победы
        """
        self.screen.fill(GREEN)
        
        draw_text(self.screen, "ПОБЕДА!", 48, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100, center=True)
        draw_text(self.screen, "Вы спасли всех девушек!", 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, center=True)
        draw_text(self.screen, "Бегемот побежден!", 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20, center=True)
        draw_text(self.screen, "Нажмите ESC для новой игры", 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, center=True)
    
    def run(self):
        """
        Основной цикл игры
        """
        running = True
        
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit() 