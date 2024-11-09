import pygame
from settings import Settings

class Splash:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.done = False
        self.font_big = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 36)
        self.settings = Settings(screen_width, screen_height)
        
        # Создаем кнопку Play
        self.play_button = pygame.Surface((200, 50))
        self.play_button.fill((255, 215, 0))  # Золотой цвет
        self.play_text = self.font_small.render("PLAY", True, (0, 0, 0))
        self.play_button_rect = pygame.Rect(
            screen_width//2 - 100,  # x
            screen_height * 2//3,    # y
            200,                     # width
            50                       # height
        )

        # Создаем кнопку Settings
        self.settings_button = pygame.Surface((200, 50))
        self.settings_button.fill((255, 215, 0))  # Золотой цвет
        self.settings_text = self.font_small.render("SETTINGS", True, (0, 0, 0))
        self.settings_button_rect = pygame.Rect(
            screen_width//2 - 100,  # x
            screen_height * 2//3 + 70,    # y (ниже кнопки Play)
            200,                     # width
            50                       # height
        )
        
        # Создаем большого цыпленка для заставки
        self.chicken_surface = pygame.Surface((100, 150), pygame.SRCALPHA)
        
        # Цвета для цыпленка
        YELLOW_BODY = (255, 235, 0)    # Ярко-желтый для тела
        ORANGE_BEAK = (255, 140, 0)    # Оранжевый для клюва
        CROWN_GOLD = (255, 215, 0)     # Золотой для короны
        CROWN_JEWEL = (255, 0, 0)      # Красный для камней в короне
        
        # Тело цыпленка (большое круглое)
        pygame.draw.ellipse(self.chicken_surface, YELLOW_BODY, (10, 30, 80, 100))
        
        # Корона
        crown_points = [
            (30, 35),    # Нижняя левая точка
            (30, 20),    # Верхняя левая точка основания
            (40, 20),    # Верх первого зубца
            (40, 10),    # Вершина первого зубца
            (50, 20),    # Верх второго зубца
            (50, 10),    # Вершина второго зубца
            (60, 20),    # Верх третьего зубца
            (60, 10),    # Вершина третьего зубца
            (70, 20),    # Верх правой стороны
            (70, 35),    # Нижняя правая точка
        ]
        pygame.draw.polygon(self.chicken_surface, CROWN_GOLD, crown_points)
        
        # Камни в короне
        pygame.draw.circle(self.chicken_surface, CROWN_JEWEL, (40, 25), 3)  # Левый камень
        pygame.draw.circle(self.chicken_surface, CROWN_JEWEL, (50, 25), 3)  # Центральный камень
        pygame.draw.circle(self.chicken_surface, CROWN_JEWEL, (60, 25), 3)  # Правый камень
        
        # Клюв
        pygame.draw.polygon(self.chicken_surface, ORANGE_BEAK, [
            (70, 70),
            (90, 75),
            (70, 80)
        ])
        
        # Глаз
        pygame.draw.circle(self.chicken_surface, (0, 0, 0), (65, 70), 5)
        
        # Ножки
        pygame.draw.rect(self.chicken_surface, ORANGE_BEAK, (30, 120, 8, 20))
        pygame.draw.rect(self.chicken_surface, ORANGE_BEAK, (60, 120, 8, 20))
        
    def draw(self, screen):
        if self.settings.active:
            self.settings.draw(screen)
            return
            
        # Заливка фона
        screen.fill((0, 0, 0))
        
        # Название игры
        title = self.font_big.render("HAPPY FLAPPY", True, (255, 255, 0))
        title_shadow = self.font_big.render("HAPPY FLAPPY", True, (255, 165, 0))
        
        # Имя разработчика
        author = self.font_small.render("by Robert Kuklin", True, (255, 255, 255))
        
        # Отрисовка с тенью
        screen.blit(title_shadow, (self.screen_width//2 - title.get_width()//2 + 2, 
                                 self.screen_height//3 + 2))
        screen.blit(title, (self.screen_width//2 - title.get_width()//2, 
                           self.screen_height//3))
        
        # Отрисовка цыпленка по центру экрана
        screen.blit(self.chicken_surface, 
                   (self.screen_width//2 - self.chicken_surface.get_width()//2,
                    self.screen_height//2 - 50))
        
        # Отрисовка кнопки Play
        pygame.draw.rect(screen, (255, 215, 0), self.play_button_rect)  # Кнопка
        pygame.draw.rect(screen, (0, 0, 0), self.play_button_rect, 2)  # Обводка кнопки
        # Центрируем текст на кнопке
        text_x = self.play_button_rect.centerx - self.play_text.get_width()//2
        text_y = self.play_button_rect.centery - self.play_text.get_height()//2
        screen.blit(self.play_text, (text_x, text_y))

        # Отрисовка кнопки Settings
        pygame.draw.rect(screen, (255, 215, 0), self.settings_button_rect)  # Кнопка
        pygame.draw.rect(screen, (0, 0, 0), self.settings_button_rect, 2)  # Обводка кнопки
        # Центрируем текст на кнопке
        text_x = self.settings_button_rect.centerx - self.settings_text.get_width()//2
        text_y = self.settings_button_rect.centery - self.settings_text.get_height()//2
        screen.blit(self.settings_text, (text_x, text_y))
        
        # Отрисовка имени разработчика в центре нижней части экрана
        screen.blit(author, (self.screen_width//2 - author.get_width()//2, 
                            self.screen_height - 40)) 