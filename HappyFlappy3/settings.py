import pygame
from arrows import Arrow
import json
import os

class Settings:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.active = False
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.volume = 0.5
        # Создаем спрайты стрелок
        self.left_arrow = Arrow('left')
        self.right_arrow = Arrow('right')

        # Добавляем константы из main.py
        # Размеры окна
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600
        self.FPS = 60

        # Цвета
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.PINK = (255, 192, 203)
        self.HEART_COLOR = (255, 0, 89)

        # Константы для анимации
        self.PLAYER_WIDTH = 32
        self.PLAYER_HEIGHT = 48

        # Константы управления
        self.CONTROLS = {
            'LEFT': [pygame.K_LEFT, pygame.K_a],
            'RIGHT': [pygame.K_RIGHT, pygame.K_d],
            'JUMP': [pygame.K_SPACE],
            'SETTINGS': pygame.K_s,
            'ESCAPE': pygame.K_ESCAPE,
            'USE_EGG': pygame.K_e,
            'CHEAT_LIFE': (pygame.K_h, pygame.KMOD_CTRL),
            'CHEAT_LEVEL': (pygame.K_n, pygame.KMOD_CTRL),
            'CHEAT_COINS': (pygame.K_m, pygame.KMOD_CTRL)
        }

        # Константы игровой механики
        self.PLAYER_SPEED = 5
        self.GRAVITY = 0.5
        self.INITIAL_JUMP_POWER = -10
        self.MAX_JUMPS = 2

        # Добавляем флаг полноэкранного режима
        self.fullscreen = True  # По умолчанию True для старта в полноэкранном режиме
        
        # Сохраняем базовые размеры окна для переключения режимов
        self.BASE_WIDTH = 800
        self.BASE_HEIGHT = 600

        self.load_settings()

    def draw(self, screen):
        # Затемнение фона
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(200)
        screen.blit(overlay, (0, 0))
        
        # Заголовок
        title = self.font.render("НАСТРОЙКИ", True, (255, 255, 255))
        screen.blit(title, (self.screen_width//2 - title.get_width()//2, 50))
        
        # Громкость
        volume_text = self.font.render("Громкость музыки:", True, (255, 255, 255))
        screen.blit(volume_text, (self.screen_width//2 - 150, 100))
        
        # Полоса громкости
        pygame.draw.rect(screen, (100, 100, 100), (self.screen_width//2 - 100, 150, 200, 20))
        pygame.draw.rect(screen, (255, 255, 0), 
                        (self.screen_width//2 - 100, 150, 200 * self.volume, 20))
        
        # Процент громкости
        volume_percent = self.font.render(f"{int(self.volume * 100)}%", True, (255, 255, 255))
        screen.blit(volume_percent, (self.screen_width//2 + 120, 145))

        # Добавляем описание управления
        controls_title = self.font.render("УПРАВЛЕНИЕ:", True, (255, 255, 0))
        screen.blit(controls_title, (self.screen_width//2 - controls_title.get_width()//2, 220))

        # Обновляем список управления
        controls = [
            ("A", self.left_arrow, "Движение влево"),
            ("D", self.right_arrow, "Движение вправо"),
            "ПРОБЕЛ / ЛКМ - Прыжок",
            "ПКМ - Атака мечом (если есть)",
            "E - Использовать яйцо (если есть)",
            "S - Открыть настройки",
            "ESC - Выход в меню/из магазина",
            "CTRL + H - Секретная комбинация для +1 жизни",
            "CTRL + N - Секретная комбинация для пропуска уровня",
            "CTRL + M - Секретная комбинация для +10 монет",
            "R - Перезапуск после проигрыша",
            "↑/↓ - Выбор предмета в магазине",
            "ENTER - Покупка предмета в магазине"
        ]

        y_pos = 260
        for i, control in enumerate(controls):
            if isinstance(control, tuple):  # Если это строка со стрелкой
                key, arrow, description = control
                text1 = self.small_font.render(f"{key} / ", True, (255, 255, 255))
                text2 = self.small_font.render(f" - {description}", True, (255, 255, 255))
                
                total_width = text1.get_width() + 20 + text2.get_width()
                x_pos = self.screen_width//2 - total_width//2
                
                screen.blit(text1, (x_pos, y_pos))
                screen.blit(arrow.image, (x_pos + text1.get_width(), y_pos))
                screen.blit(text2, (x_pos + text1.get_width() + 25, y_pos))
            else:
                control_text = self.small_font.render(control, True, (255, 255, 255))
                screen.blit(control_text, (self.screen_width//2 - control_text.get_width()//2, y_pos))
            y_pos += 30
        
        # Инструкция с использованием спрайтов стрелок
        instruction_text1 = self.font.render("Регулировка громкости: ", True, (255, 255, 255))
        instruction_text2 = self.font.render(" / ", True, (255, 255, 255))
        instruction_text3 = self.font.render(", ESC - Выход", True, (255, 255, 255))
        
        total_width = (instruction_text1.get_width() + 40 + instruction_text2.get_width() + 
                      instruction_text3.get_width())
        x_pos = self.screen_width//2 - total_width//2
        y_pos = self.screen_height - 50
        
        screen.blit(instruction_text1, (x_pos, y_pos))
        screen.blit(self.left_arrow.image, (x_pos + instruction_text1.get_width(), y_pos + 8))
        screen.blit(instruction_text2, (x_pos + instruction_text1.get_width() + 20, y_pos))
        screen.blit(self.right_arrow.image, (x_pos + instruction_text1.get_width() + 
                                           instruction_text2.get_width() + 20, y_pos + 8))
        screen.blit(instruction_text3, (x_pos + instruction_text1.get_width() + 
                                      instruction_text2.get_width() + 40, y_pos)) 

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                data = json.load(f)
                self.volume = data.get('volume', 0.5)
                # другие настройки...
        except FileNotFoundError:
            self.save_settings()
    
    def save_settings(self):
        data = {
            'volume': self.volume,
            # другие настройки...
        }
        with open('settings.json', 'w') as f:
            json.dump(data, f) 