import pygame

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 60), pygame.SRCALPHA)  # Прозрачный фон
        
        # Цвета
        DOOR_COLOR = (101, 67, 33)  # Тёмный дубовый цвет
        DOOR_DARK = (82, 54, 27)    # Более тёмный для деталей
        
        # Основа двери
        pygame.draw.rect(self.image, DOOR_COLOR, (0, 0, 40, 60))
        
        # Рамка двери
        pygame.draw.rect(self.image, DOOR_DARK, (0, 0, 40, 60), 2)
        
        # Дверная ручка
        pygame.draw.circle(self.image, DOOR_DARK, (30, 30), 3)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y