import pygame

class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        
        # Цвета
        self.heart_color = (255, 0, 89)  # Основной цвет сердца
        self.heart_outline = (200, 0, 60)  # Цвет контура
        
        # Паттерн пиксельного сердца
        pixels = [
            "   **   **    ",
            "  ***   ***  ",
            " ***** ***** ",
            " *********** ",
            " *********** ",
            "  ********* ",
            "   *******  ",
            "    *****   ",
            "     ***    ",
            "      *     "
        ]
        
        pixel_size = 2
        # Центрируем сердце на поверхности
        start_x = (30 - len(pixels[0]) * pixel_size) // 2
        start_y = (30 - len(pixels) * pixel_size) // 2
        
        # Рисуем основное сердце
        for y_pos, row in enumerate(pixels):
            for x_pos, pixel in enumerate(row):
                if pixel == '*':
                    pygame.draw.rect(self.image, self.heart_color, 
                                   (start_x + x_pos * pixel_size, 
                                    start_y + y_pos * pixel_size, 
                                    pixel_size, pixel_size))
                    
        # Добавляем контур для объема
        for y_pos, row in enumerate(pixels):
            for x_pos, pixel in enumerate(row):
                if pixel == '*':
                    # Проверяем края для контура
                    if (x_pos == 0 or x_pos == len(row)-1 or 
                        y_pos == 0 or y_pos == len(pixels)-1 or
                        (x_pos > 0 and row[x_pos-1] == ' ') or
                        (x_pos < len(row)-1 and row[x_pos+1] == ' ')):
                        pygame.draw.rect(self.image, self.heart_outline, 
                                       (start_x + x_pos * pixel_size, 
                                        start_y + y_pos * pixel_size, 
                                        pixel_size, pixel_size))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 