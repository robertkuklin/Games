import pygame

# Добавим новый класс для гнезда с яйцом
class Nest(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 25), pygame.SRCALPHA)  # Размер оверхности
        
        # Рисуем яйцо с более насыщенными цветами
        pygame.draw.ellipse(self.image, (255, 223, 186), (0, 0, 20, 25))  # Основной цвет яйца (более теплый)
        pygame.draw.ellipse(self.image, (255, 255, 220), (3, 3, 14, 15))  # Блик на яйце
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collected = False