import pygame

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        
        # Цвета для монеты
        self.coin_color = (255, 215, 0)  # Золотой
        self.outline_color = (218, 165, 32)  # Темно-золотой
        
        # Рисуем монету
        pygame.draw.circle(self.image, self.outline_color, (10, 10), 10)  # Внешний круг
        pygame.draw.circle(self.image, self.coin_color, (10, 10), 8)  # Внутренний круг
        # Добавляем блик
        pygame.draw.circle(self.image, (255, 255, 200), (7, 7), 3)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Анимация покачивания
        self.original_y = y
        self.float_offset = 0
        self.float_speed = 0.1 