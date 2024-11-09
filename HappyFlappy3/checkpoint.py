import pygame

class Checkpoint(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 60), pygame.SRCALPHA)
        
        # Цвета
        FLAG_COLOR = (255, 215, 0)  # Золотой цвет для флага
        POLE_COLOR = (169, 169, 169)  # Серый цвет для шеста
        
        # Рисуем шест
        pygame.draw.rect(self.image, POLE_COLOR, (18, 0, 4, 60))
        
        # Рисуем флаг
        flag_points = [
            (22, 5),   # Верхнее крепление
            (40, 15),  # Кончик флага
            (22, 25)   # Нижнее крепление
        ]
        pygame.draw.polygon(self.image, FLAG_COLOR, flag_points)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.activated = False 