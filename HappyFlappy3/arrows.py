import pygame

class Arrow(pygame.sprite.Sprite):
    def __init__(self, direction='left'):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        
        # Паттерн для стрелки
        if direction == 'left':
            pixels = [
                "    *     ",
                "   **     ",
                "  ***     ",
                " ****     ",
                "*****     ",
                "*****     ",
                " ****     ",
                "  ***     ",
                "   **     ",
                "    *     "
            ]
        else:  # right
            pixels = [
                "     *    ",
                "     **   ",
                "     *** ",
                "     ****",
                "     *****",
                "     *****",
                "     ****",
                "     *** ",
                "     **   ",
                "     *    "
            ]
        
        # Рисуем стрелку
        pixel_size = 2
        for y, row in enumerate(pixels):
            for x, pixel in enumerate(row):
                if pixel == '*':
                    pygame.draw.rect(self.image, (255, 255, 255),
                                   (x * pixel_size, y * pixel_size,
                                    pixel_size, pixel_size)) 