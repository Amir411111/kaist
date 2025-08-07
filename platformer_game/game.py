"""
Основной цикл игры и переключение уровней
"""

import pygame
from settings import *
from player import Player
from level import Level
from select_screen import CharacterSelectScreen
<<<<<<< HEAD
from utils import draw_text, create_character_sprite, create_male_character_sprite
=======
from utils import draw_text
>>>>>>> 34bd1fe0c9b62876c01efda95ef2c17266b3188d

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
<<<<<<< HEAD
        pygame.display.set_caption("Platformer - Save the Heroes!")
=======
        pygame.display.set_caption("Платформер - Спаси девушек!")
>>>>>>> 34bd1fe0c9b62876c01efda95ef2c17266b3188d
        self.clock = pygame.time.Clock()
        
        # Состояние игры
        self.state = STATE_SELECT_CHARACTER
        self.selected_character = 1
        self.current_level = 1
        self.player = None
        self.level = None
        self.level_timer = 0  # Таймер для автозавершения уровня 1
<<<<<<< HEAD
        self.final_scene_timer = 0  # Таймер для финальной сцены
=======
>>>>>>> 34bd1fe0c9b62876c01efda95ef2c17266b3188d
        
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
            
<<<<<<< HEAD
                                # Проверяем завершение уровня
            if self.level.is_completed(self.player, self.level_timer):
                if self.current_level == 3:
                    # Если завершен третий уровень - запускаем финальную сцену
                    self.state = STATE_FINAL_SCENE
                    self.final_scene_timer = 0
                else:
                    self.next_level()
        
        elif self.state == STATE_FINAL_SCENE:
            # Обновляем финальную сцену
            self.final_scene_timer += 1
            if self.final_scene_timer >= 180:  # 3 секунды при 60 FPS
                self.state = STATE_VICTORY
=======
            # Проверяем завершение уровня
            if self.level.is_completed(self.player, self.level_timer):
                self.next_level()
>>>>>>> 34bd1fe0c9b62876c01efda95ef2c17266b3188d
    
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
<<<<<<< HEAD
            draw_text(self.screen, f"Level {self.current_level}", 32, WHITE, 10, 10)
            
            # Инструкции для первого уровня
            if self.current_level == 1:
                draw_text(self.screen, "Reach the right edge of the screen!", 24, YELLOW, SCREEN_WIDTH // 2, 50, center=True)
                draw_text(self.screen, "Use arrow keys/WASD for movement", 20, WHITE, SCREEN_WIDTH // 2, 80, center=True)
                draw_text(self.screen, "Space to jump", 20, WHITE, SCREEN_WIDTH // 2, 110, center=True)
            
            # Инструкции для других уровней
            elif self.current_level == 2:
                draw_text(self.screen, "Defeat all enemies OR reach the right edge!", 24, YELLOW, SCREEN_WIDTH // 2, 50, center=True)
                draw_text(self.screen, "Jump on enemies from above", 20, WHITE, SCREEN_WIDTH // 2, 80, center=True)
            elif self.current_level == 3:
                draw_text(self.screen, "Defeat the hippo boss!", 24, RED, SCREEN_WIDTH // 2, 50, center=True)
                draw_text(self.screen, "Jump on the boss 3 times", 20, WHITE, SCREEN_WIDTH // 2, 80, center=True)
                draw_text(self.screen, "Avoid fireballs", 20, WHITE, SCREEN_WIDTH // 2, 110, center=True)
                draw_text(self.screen, "Free Sanzhar, Erkosh & Aibek!", 20, YELLOW, SCREEN_WIDTH // 2, 140, center=True)
=======
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
>>>>>>> 34bd1fe0c9b62876c01efda95ef2c17266b3188d
        
        elif self.state == STATE_GAME_OVER:
            self.draw_game_over()
        
<<<<<<< HEAD
        elif self.state == STATE_FINAL_SCENE:
            self.draw_final_scene()
=======
>>>>>>> 34bd1fe0c9b62876c01efda95ef2c17266b3188d
        elif self.state == STATE_VICTORY:
            self.draw_victory()
        
        pygame.display.flip()
    
<<<<<<< HEAD
    def draw_final_scene(self):
        """
        Отрисовывает финальную сцену освобождения героев
        """
        self.screen.fill(BLUE)
        
        # Определяем имя выбранной героини
        heroine_names = {
            1: "Kamilla",
            2: "Dana", 
            3: "Moldir"
        }
        heroine_name = heroine_names.get(self.selected_character, "Heroine")
        
        # Позиции персонажей в зависимости от времени
        progress = min(self.final_scene_timer / 180.0, 1.0)  # От 0 до 1
        
        # Героиня в центре
        heroine_x = SCREEN_WIDTH // 2 - 32
        heroine_y = SCREEN_HEIGHT // 2 - 50
        player_sprite = self.player.current_sprite
        self.screen.blit(player_sprite, (heroine_x, heroine_y))
        draw_text(self.screen, heroine_name, 24, WHITE, SCREEN_WIDTH // 2, heroine_y + 80, center=True)
        
        # Мужские герои начинают с краев и сходятся к центру
        male_sprites = []
        for i in range(1, 4):
            sprite = create_male_character_sprite(str(i))
            sprite = pygame.transform.scale(sprite, (48, 48))
            male_sprites.append(sprite)
        
        # Имена мужских героев
        male_names = ["Sanzhar", "Erkosh", "Aibek"]
        
        # Начальные позиции (по краям экрана)
        start_positions = [
            (50, SCREEN_HEIGHT - 100),  # Левый
            (SCREEN_WIDTH - 98, SCREEN_HEIGHT - 100),  # Правый
            (SCREEN_WIDTH // 2 - 24, SCREEN_HEIGHT - 50)  # Центр снизу
        ]
        
        # Конечные позиции (вокруг героини)
        end_positions = [
            (heroine_x - 80, heroine_y + 20),  # Слева от героини
            (heroine_x + 80, heroine_y + 20),  # Справа от героини
            (heroine_x, heroine_y + 100)  # Под героиней
        ]
        
        # Отрисовываем мужских героев с анимацией движения
        for i, (sprite, start_pos, end_pos, name) in enumerate(zip(male_sprites, start_positions, end_positions, male_names)):
            # Интерполируем позицию
            current_x = start_pos[0] + (end_pos[0] - start_pos[0]) * progress
            current_y = start_pos[1] + (end_pos[1] - start_pos[1]) * progress
            
            self.screen.blit(sprite, (current_x, current_y))
            draw_text(self.screen, name, 16, WHITE, current_x + 24, current_y + 60, center=True)
        
        # Текст сцены
        if progress < 0.3:
            draw_text(self.screen, "Heroes are being freed...", 28, WHITE, SCREEN_WIDTH // 2, 50, center=True)
        elif progress < 0.7:
            draw_text(self.screen, "Heroes are coming together...", 28, WHITE, SCREEN_WIDTH // 2, 50, center=True)
        else:
            draw_text(self.screen, "All heroes united!", 28, WHITE, SCREEN_WIDTH // 2, 50, center=True)
    
=======
>>>>>>> 34bd1fe0c9b62876c01efda95ef2c17266b3188d
    def draw_game_over(self):
        """
        Отрисовывает экран окончания игры
        """
        self.screen.fill(BLACK)
        
<<<<<<< HEAD
        draw_text(self.screen, "GAME OVER", 64, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, center=True)
        draw_text(self.screen, "Press ESC to return to menu", 28, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, center=True)
    
    def draw_victory(self):
        """
        Отрисовывает экран победы с освобожденными персонажами
        """
        self.screen.fill(GREEN)
        
        # Заголовок
        draw_text(self.screen, "VICTORY!", 64, WHITE, SCREEN_WIDTH // 2, 80, center=True)
        draw_text(self.screen, "Hippo boss defeated!", 28, WHITE, SCREEN_WIDTH // 2, 130, center=True)
        
        # Отрисовываем всех персонажей в новом расположении
        # Игрок (женский персонаж) - в центре сверху
        player_sprite = self.player.current_sprite
        self.screen.blit(player_sprite, (SCREEN_WIDTH // 2 - 32, 200))
        
        # Определяем имя выбранной героини
        heroine_names = {
            1: "Kamilla",
            2: "Dana", 
            3: "Moldir"
        }
        heroine_name = heroine_names.get(self.selected_character, "Heroine")
        draw_text(self.screen, heroine_name, 24, WHITE, SCREEN_WIDTH // 2, 280, center=True)
        
        # Освобожденные персонажи (мужские) - внизу полукругом
        male_sprites = []
        for i in range(1, 4):
            sprite = create_male_character_sprite(str(i))
            sprite = pygame.transform.scale(sprite, (48, 48))  # Немного меньше игрока
            male_sprites.append(sprite)
        
        # Позиции для освобожденных персонажей (полукругом внизу)
        positions = [
            (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT - 200),  # Левый
            (SCREEN_WIDTH // 2 - 24, SCREEN_HEIGHT - 180),   # Центр
            (SCREEN_WIDTH // 2 + 72, SCREEN_HEIGHT - 200)    # Правый
        ]
        
        labels = ["Sanzhar", "Erkosh", "Aibek"]
        
        for i, (sprite, pos, label) in enumerate(zip(male_sprites, positions, labels)):
            self.screen.blit(sprite, pos)
            draw_text(self.screen, label, 20, WHITE, pos[0] + 24, pos[1] + 60, center=True)
        
        # Финальное сообщение
        draw_text(self.screen, "All heroes saved!", 28, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, center=True)
        draw_text(self.screen, "Press ESC for new game", 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, center=True)
=======
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
>>>>>>> 34bd1fe0c9b62876c01efda95ef2c17266b3188d
    
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