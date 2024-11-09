import pygame
import random

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        
        # Цвета для каменной платформы
        STONE_COLOR = (105, 105, 105)  # Основной серый цвет
        STONE_DARK = (79, 79, 79)      # Тёмно-серый для рамки
        
        # Заполняем основным цветом камня
        self.image.fill(STONE_COLOR)
        
        # Добавляем рамку
        pygame.draw.rect(self.image, STONE_DARK, (0, 0, width, height), 2)
        
        # Добавляем текстуру камня (случайные точки)
        for _ in range(width * height // 40):  # Количество точек зависит от размера платформы
            px = random.randint(4, width-4)
            py = random.randint(4, height-4)
            dot_size = random.randint(2, 4)
            dot_color = random.choice([(120, 120, 120), (90, 90, 90)])  # Случайный оттенок серого
            pygame.draw.circle(self.image, dot_color, (px, py), dot_size)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y