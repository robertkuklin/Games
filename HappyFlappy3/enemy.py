import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, window_width=800, window_height=600):
        super().__init__()
        self.frames = []
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100
        self.is_dead = False
        self.speed_y = 0
        self.gravity = 0.5
        self.window_width = window_width
        self.window_height = window_height

        # Создаем кадры анимации
        for i in range(2):
            frame = pygame.Surface((30, 30), pygame.SRCALPHA)
            
            # Цвета для мухи
            BODY_COLOR = (0, 0, 0)
            WING_COLOR = (200, 200, 200)
            EYE_COLOR = (255, 0, 0)
            
            # Рисуем тело мухи
            pygame.draw.circle(frame, BODY_COLOR, (15, 15), 8)
            
            # Рисуем крылья
            if i == 0:
                pygame.draw.ellipse(frame, WING_COLOR, (5, 5, 10, 20))
                pygame.draw.ellipse(frame, WING_COLOR, (15, 5, 10, 20))
            else:
                pygame.draw.ellipse(frame, WING_COLOR, (5, 10, 10, 15))
                pygame.draw.ellipse(frame, WING_COLOR, (15, 10, 10, 15))
            
            # Рисуем глаза
            pygame.draw.circle(frame, EYE_COLOR, (12, 12), 2)
            pygame.draw.circle(frame, EYE_COLOR, (18, 12), 2)
            
            self.frames.append(frame)

        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 2

    def update(self):
        if self.is_dead:
            self.speed_y += self.gravity
            self.rect.y += self.speed_y
            
            # Используем сохраненную высоту окна
            if self.rect.top > self.window_height:
                self.kill()
        else:
            self.rect.x += self.speed_x
            # Используем сохраненную ширину окна
            if self.rect.left < 0 or self.rect.right > self.window_width:
                self.speed_x = -self.speed_x

            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]

    def die(self):
        self.is_dead = True
        self.speed_x = 0
