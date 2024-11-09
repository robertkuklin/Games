import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, window_width=800, window_height=600, player_width=32, player_height=48):
        super().__init__()
        self.window_width = window_width
        self.window_height = window_height
        self.player_width = player_width
        self.player_height = player_height
        
        self.sprites_right = []
        self.sprites_left = []
        
        # Добавляем инициализацию жизней
        self.lives = 3
        self.initial_lives = 3
        self.coins = 0
        self.is_alive = True
        self.speed_x = 0
        self.speed_y = 0
        self.gravity = 0.5
        self.jump_power = -10
        self.on_ground = False
        self.jump_count = 0
        self.max_jumps = 2
        
        # Создаем базовый спрайт цыпленка
        base_sprite = pygame.Surface((self.player_width, self.player_height), pygame.SRCALPHA)
        
        # Цвета для цыпленка
        YELLOW_BODY = (255, 235, 0)    # Ярко-желтый для тела
        ORANGE_BEAK = (255, 140, 0)    # Оранжевый для клюва
        CROWN_GOLD = (255, 215, 0)     # Золотой для короны
        CROWN_JEWEL = (255, 0, 0)      # Красный для камней в короне
        BLACK = (0, 0, 0)              # Черный цвет для глаз
        
        # Тло цыпленка (круглое)
        pygame.draw.ellipse(base_sprite, YELLOW_BODY, (2, 10, self.player_width-4, self.player_height-15))
        
        # Корона
        crown_points = [
            (8, 15),     # Нижняя левая точка
            (8, 10),     # Верхняя левая точка основания
            (14, 10),    # Верх первого зубца
            (14, 5),     # Вершина первого зубца
            (18, 10),    # Верх второго зубца
            (18, 5),     # Вершина второго зубца
            (22, 10),    # Верх третьего зубца
            (22, 5),     # Вершина третьего зубца
            (26, 10),    # Верх правой стороны
            (26, 15),    # Нижняя правая точка
        ]
        pygame.draw.polygon(base_sprite, CROWN_GOLD, crown_points)
        
        # Камни в короне
        pygame.draw.circle(base_sprite, CROWN_JEWEL, (14, 12), 2)  # Левый камень
        pygame.draw.circle(base_sprite, CROWN_JEWEL, (18, 12), 2)  # Центральный камень
        pygame.draw.circle(base_sprite, CROWN_JEWEL, (22, 12), 2)  # Правый камень
        
        # Клюв
        pygame.draw.polygon(base_sprite, ORANGE_BEAK, [
            (self.player_width-10, self.player_height//2-2),
            (self.player_width-2, self.player_height//2),
            (self.player_width-10, self.player_height//2+2)
        ])
        
        # Глаз
        pygame.draw.circle(base_sprite, BLACK, (self.player_width-12, self.player_height//2), 2)
        
        # Ножки
        pygame.draw.rect(base_sprite, ORANGE_BEAK, (8, self.player_height-8, 3, 8))
        pygame.draw.rect(base_sprite, ORANGE_BEAK, (18, self.player_height-8, 3, 8))
        
        # Создаем вариации для анимации
        for i in range(3):
            sprite = base_sprite.copy()
            if i > 0:
                # Анимация ног при ходьбе
                if i == 1:
                    pygame.draw.rect(sprite, ORANGE_BEAK, (8, self.player_height-8, 3, 6))
                    pygame.draw.rect(sprite, ORANGE_BEAK, (18, self.player_height-6, 3, 6))
                else:
                    pygame.draw.rect(sprite, ORANGE_BEAK, (8, self.player_height-6, 3, 6))
                    pygame.draw.rect(sprite, ORANGE_BEAK, (18, self.player_height-8, 3, 6))
            self.sprites_right.append(sprite)
        
        # Создаем спрайты для движения влево
        for sprite in self.sprites_right:
            self.sprites_left.append(pygame.transform.flip(sprite, True, False))
        
        self.current_sprite = 0
        self.animation_speed = 0.2
        self.last_update = 0
        self.facing_right = True
        
        self.image = self.sprites_right[0]
        self.rect = self.image.get_rect()
        
        # Создаем хитбокс меньшего размеа для более точных коллизий
        self.hitbox = pygame.Rect(0, 0, self.player_width-12, self.player_height-12)
        self.spawn_point = (self.window_width // 2, self.window_height // 2)
        self.rect.center = self.spawn_point
        
        # Остальные параметры...
        self.has_sword = False  # Изначально меча нет
        self.sword_active = False
        self.sword_animation_index = 0
        self.sword_animation_speed = 0.1
        self.armor = 1  # Броня на одно сердце
        self.armor_max = 1
        self.armor_recharge_time = 10000  # Время восстановления брони в миллисекундах
        self.last_armor_recharge = pygame.time.get_ticks()
        self.invulnerable = False  # Флаг невосприимчивости
        self.invulnerable_time = 1000  # Время невосприимчивости в миллисекундах
        self.last_hit_time = 0  # Время последнего удара
        self.has_egg = False  # Флаг наличия яйца
        self.extra_armor = False  # Флаг дополнительной брони
        self.blink_interval = 100  # Интервал мерцания в миллисекундах
        self.visible = True  # Флаг видимости для мерцания

    def draw_sword(self, screen):
        if self.sword_active:
            sword_length = 40
            sword_width = 5
            sword_color = (192, 192, 192)  # Серебряный цвет для клинка
            handle_length = 10
            handle_width = 4  # Увеличили ширину рукояти
            handle_color = (139, 69, 19)  # Коричневый цвет для рукояти
            guard_color = (169, 169, 169)  # Серый цвет для гарды
            offset = 10  # Сдвиг меча вправо

            # Угол поворота меча
            angle = self.sword_animation_index * 45  # 45 градусов за кадр

            # Вычисляем координаты меча с учетом угла и направления
            if self.facing_right:
                sword_start = (self.rect.centerx + offset, self.rect.centery)
                # Основная часть клинка
                sword_mid = (
                    sword_start[0] + (sword_length - 10) * pygame.math.Vector2(1, 0).rotate(angle).x,
                    sword_start[1] + (sword_length - 10) * pygame.math.Vector2(1, 0).rotate(angle).y
                )
                # Острый конец меча
                sword_end = (
                    sword_start[0] + sword_length * pygame.math.Vector2(1, 0).rotate(angle).x,
                    sword_start[1] + sword_length * pygame.math.Vector2(1, 0).rotate(angle).y
                )
                # Координаты рукояти
                handle_end = (
                    sword_start[0] - handle_length * pygame.math.Vector2(1, 0).rotate(angle).x,
                    sword_start[1] - handle_length * pygame.math.Vector2(1, 0).rotate(angle).y
                )
                # Координаты гарды (перпендикулярно мечу)
                guard_vector = pygame.math.Vector2(0, 1).rotate(angle)
                guard_top = (
                    sword_start[0] + 8 * guard_vector.x,
                    sword_start[1] + 8 * guard_vector.y
                )
                guard_bottom = (
                    sword_start[0] - 8 * guard_vector.x,
                    sword_start[1] - 8 * guard_vector.y
                )
            else:
                sword_start = (self.rect.centerx - offset, self.rect.centery)
                # Основная часть клинка
                sword_mid = (
                    sword_start[0] + (sword_length - 10) * pygame.math.Vector2(-1, 0).rotate(-angle).x,
                    sword_start[1] + (sword_length - 10) * pygame.math.Vector2(-1, 0).rotate(-angle).y
                )
                # Острый конец меча
                sword_end = (
                    sword_start[0] + sword_length * pygame.math.Vector2(-1, 0).rotate(-angle).x,
                    sword_start[1] + sword_length * pygame.math.Vector2(-1, 0).rotate(-angle).y
                )
                # Координаты рукояти
                handle_end = (
                    sword_start[0] - handle_length * pygame.math.Vector2(-1, 0).rotate(-angle).x,
                    sword_start[1] - handle_length * pygame.math.Vector2(-1, 0).rotate(-angle).y
                )
                # Координаты гарды (перпендикулярно мечу)
                guard_vector = pygame.math.Vector2(0, 1).rotate(-angle)
                guard_top = (
                    sword_start[0] + 8 * guard_vector.x,
                    sword_start[1] + 8 * guard_vector.y
                )
                guard_bottom = (
                    sword_start[0] - 8 * guard_vector.x,
                    sword_start[1] - 8 * guard_vector.y
                )

            # Сначала рисуем рукоять
            pygame.draw.line(screen, handle_color, handle_end, sword_start, handle_width)
            # Рисуем гарду
            pygame.draw.line(screen, guard_color, guard_top, guard_bottom, 4)
            # Затем рисуем основную часть клинка
            pygame.draw.line(screen, sword_color, sword_start, sword_mid, sword_width)
            # И наконец заострённый конец
            pygame.draw.line(screen, sword_color, sword_mid, sword_end, max(1, sword_width - 2))

    def animate(self):
        now = pygame.time.get_ticks()
        
        # Мерцание при невосприимчивости
        if self.invulnerable:
            if (now - self.last_hit_time) // self.blink_interval % 2 == 0:
                self.visible = True
            else:
                self.visible = False
            
            if now - self.last_hit_time >= self.invulnerable_time:
                self.invulnerable = False
                self.visible = True
        
        if now - self.last_update > 100:  # Обновляем каждые 100мс
            self.last_update = now
            if self.sword_active:
                self.sword_animation_index += 1
                if self.sword_animation_index >= 12:
                    self.sword_active = False
                    self.sword_animation_index = 0
            elif abs(self.speed_x) > 0:
                self.current_sprite = (self.current_sprite + 1) % 3
                if self.speed_x > 0:
                    self.image = self.sprites_right[self.current_sprite]
                    self.facing_right = True
                else:
                    self.image = self.sprites_left[self.current_sprite]
                    self.facing_right = False
            else:
                self.current_sprite = 0
                if self.facing_right:
                    self.image = self.sprites_right[0]
                else:
                    self.image = self.sprites_left[0]
        
        # Делаем спрайт прозрачным при мерцании
        if not self.visible:
            self.image.set_alpha(0)
        else:
            self.image.set_alpha(255)

    def die(self):
        now = pygame.time.get_ticks()
        if self.invulnerable and now - self.last_hit_time < self.invulnerable_time:
            return  # Игрок невосприимчив, не умирает

        if self.armor > 0:
            self.armor -= 1
            self.invulnerable = True
            self.last_hit_time = now
            self.last_armor_recharge = now  # Сбрасываем таймер восстановления брони
        else:
            self.lives -= 1
            if self.lives > 0:
                self.respawn()
            else:
                self.is_alive = False
                self.lives = 0

    def reset_lives(self):
        self.lives = self.initial_lives
        self.is_alive = True
        self.coins = 0  # Сбрасываем монеты
        self.armor = 1
        self.armor_max = 1
        self.extra_armor = False
        self.has_egg = False
        self.has_sword = False  # Сбрасываем меч
        self.max_jumps = 2  # Сбрасываем количество прыжков
        self.jump_power = -10  # Сбрасываем силу прыжка
        self.speed_x = 0  # Сбрасываем скорость
        self.respawn()

    def respawn(self):
        self.rect.center = self.spawn_point
        self.speed_x = 0
        self.speed_y = 0
        self.jump_count = 0
        self.is_alive = True

    def update(self):
        # Гравитация
        self.speed_y += self.gravity
        
        # Перемеени
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Обновляем позицию хитбокса вместе с rect
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.centery = self.rect.centery + 2  # Немного смещаем хитбокс вниз
        
        # Анимация
        self.animate()

        # роверка пания за пределы экрана
        if self.rect.top > self.window_height:
            self.die()
        
        # Ограничение экрана по бокам
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.window_width:
            self.rect.right = self.window_width

        # Восстановление брони
        now = pygame.time.get_ticks()
        if now - self.last_armor_recharge > self.armor_recharge_time:
            if self.armor < self.armor_max:
                self.armor += 1
                self.last_armor_recharge = now

        # Сброс невосприимчивости
        if self.invulnerable and now - self.last_hit_time >= self.invulnerable_time:
            self.invulnerable = False
