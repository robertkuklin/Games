import random
import pygame
from levels import LEVELS
from splash import Splash
from settings import Settings
from player import Player
from coin import Coin
from heart import Heart
from shop import Shop
from door import Door
from nest import Nest
from checkpoint import Checkpoint
from enemy import Enemy
from platforms import Platform
from enum import Enum
import os

class GameState(Enum):
    SPLASH = 0
    PLAYING = 1
    PAUSED = 2
    SHOP = 3
    SETTINGS = 4
    GAME_OVER = 5


class Game:
    def __init__(self, screen, toggle_fullscreen_func):
        self.screen = screen
        self.toggle_fullscreen = toggle_fullscreen_func
        self.settings = Settings(800, 600)
        self.splash = Splash(self.settings.WINDOW_WIDTH, self.settings.WINDOW_HEIGHT)
        self.current_level = 0
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.hearts = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player = Player(
            self.settings.WINDOW_WIDTH, 
            self.settings.WINDOW_HEIGHT, 
            self.settings.PLAYER_WIDTH, 
            self.settings.PLAYER_HEIGHT
        )
        self.door = None
        self.all_sprites.add(self.player)
        self.game_over = False
        self.load_level(self.current_level)
        self.update_hearts()
        self.shop = Shop(self.settings.WINDOW_WIDTH, self.settings.WINDOW_HEIGHT)
        self.in_shop = False
        self.in_settings = False
        self.nest = None  # Добавляем атрибут для гнезда
        self.nest_group = pygame.sprite.Group()  # Группа для гнезда
        self.checkpoint = None
        self.checkpoint_group = pygame.sprite.Group()
        self.checkpoint_level = None
        self.state = GameState.SPLASH

    def update_hearts(self):
        # Удаляем старые сердца
        for heart in self.hearts:
            heart.kill()
        
        # Создаем новые сердца в соответствии с количеством жизней
        for i in range(self.player.lives):
            heart = Heart(15 + i * 35, 15)  # Увеличим расстояние между сердцами
            self.hearts.add(heart)

    def draw_armor(self, screen):
        # Используем цвета из настроек
        BLACK = self.settings.BLACK
        # Отрисовка щитов и прогресс-баров для брони
        for i in range(self.player.armor_max):  # Рисуем щиты по количеству максимальной брони
            shield = pygame.Surface((25, 25), pygame.SRCALPHA)  # Увеличили размер поверхности
            shield_points = [
                (12, 2),    # Верхняя точка
                (22, 7),    # Правая верхняя точка
                (19, 17),   # Правая нижняя точка
                (12, 22),   # Нижняя точка (заостренная)
                (5, 17),    # Лвая нижняя точка
                (2, 7)      # Левая верхняя точка
            ]
            # Есл щит активен (есть броня), рисуем его серым, иначе тёмно-серым
            color = (169, 169, 169) if i < self.player.armor else (100, 100, 100)
            pygame.draw.polygon(shield, color, shield_points)  # Цвет щита
            pygame.draw.polygon(shield, BLACK, shield_points, 2)  # Контур щита
            screen.blit(shield, (15 + i * 30, 50))  # Увеличили расстояние между щитам

            # Добавляем прогресс-бар восстановления брони
            if i >= self.player.armor:  # Только для неактивных щитов
                now = pygame.time.get_ticks()
                time_since_last_hit = now - self.player.last_armor_recharge
                progress = min(1.0, time_since_last_hit / self.player.armor_recharge_time)
                
                # Фон прогресс-бара
                pygame.draw.rect(screen, (50, 50, 50), 
                               (15 + i * 30, 77, 25, 3))  # Подвинули и расширили прогресс-бар
                
                # Заполнение прогресс-бара
                if progress > 0:
                    pygame.draw.rect(screen, (100, 149, 237),  # Светло-синий цвет
                                   (15 + i * 30, 77, 25 * progress, 3))

    def reset_game(self):
        if self.checkpoint and self.checkpoint.activated:
            self.current_level = self.checkpoint_level
        else:
            self.current_level = 0
        self.game_over = False
        self.player.reset_lives()
        # Сбрасываем состояние всех предметов в магазине
        for item in self.shop.items:
            item.purchased = False
        self.load_level(self.current_level)

    def load_level(self, level_num):
        # Очищаем старые платформы, дврь и врагов
        for platform in self.platforms:
            platform.kill()
        if self.door:
            self.door.kill()
        for coin in self.coins:
            coin.kill()
        for enemy in self.enemies:
            enemy.kill()
        
        # Загружаем новые платформы
        level_data = LEVELS[level_num]
        platforms_list = []
        for platform_data in level_data:
            platform = Platform(
                platform_data["x"],
                platform_data["y"],
                platform_data["width"],
                platform_data["height"]
            )
            self.platforms.add(platform)
            self.all_sprites.add(platform)
            platforms_list.append(platform)
        
        # Находим самую правую платформу для двери
        rightmost_platform = None
        max_right = -float('inf')
        for platform in platforms_list:
            if platform.rect.right > max_right:
                max_right = platform.rect.right
                rightmost_platform = platform
        
        # Устанавливаем дверь на правой платформе
        door_x = rightmost_platform.rect.right - 60
        door_y = rightmost_platform.rect.top - 60
        self.door = Door(door_x, door_y)
        self.all_sprites.add(self.door)
        
        # Находим самую левую платформу для спавна игрока
        leftmost_platform = min(platforms_list, key=lambda p: p.rect.left)
        self.player.spawn_point = (leftmost_platform.rect.left + 50, leftmost_platform.rect.top - 50)
        self.player.respawn()
        
        # Добавляем врагов начиная с 10 уровня
        if level_num >= 9:  # ндекс 9 соответствует 10 уровню
            for i in range(3):  # Добавим 3 врага
                enemy = Enemy(random.randint(0, self.settings.WINDOW_WIDTH - 30), 
                             random.randint(0, self.settings.WINDOW_HEIGHT - 30),
                             self.settings.WINDOW_WIDTH, self.settings.WINDOW_HEIGHT)
                self.enemies.add(enemy)
                self.all_sprites.add(enemy)
        
        # Находим платформу для яйца на 12 уровне
        egg_platform = None
        if level_num == 11:  # Индекс 11 соответствует 12 уровню
            middle_platforms = sorted(self.platforms.sprites(), key=lambda p: p.rect.x)
            if len(middle_platforms) > 2:
                egg_platform = middle_platforms[len(middle_platforms)//2]
                # Центрируем яйцо на платформе
                egg_x = egg_platform.rect.centerx - 10
                egg_y = egg_platform.rect.top - 30
                self.nest = Nest(egg_x, egg_y)
                self.nest_group.add(self.nest)
                self.all_sprites.add(self.nest)
        
        # Добавляем монеты на некоторые платформы
        for platform in self.platforms:
            # Дбавляем монету с вероятностью 50% (кроме первой, последнй и платформы с яйцом)
            if (platform != leftmost_platform and 
                platform != rightmost_platform and 
                platform != egg_platform and
                random.random() < 0.5):
                coin = Coin(platform.rect.centerx - 10, platform.rect.top - 30)
                self.coins.add(coin)
                self.all_sprites.add(coin)
        
        # Добавляем чекпойнт на 11 уровне
        if level_num == 10:  # Индекс 10 соответствует 11 уровню
            # Находим самую нижнюю платформу
            lowest_platform = max(self.platforms.sprites(), key=lambda p: p.rect.bottom)
            # Размещаем чекпонт на этой платформе
            self.checkpoint = Checkpoint(lowest_platform.rect.centerx - 20, lowest_platform.rect.top - 60)
            self.checkpoint_group.add(self.checkpoint)
            self.all_sprites.add(self.checkpoint)

    def next_level(self):
        self.current_level = (self.current_level + 1) % len(LEVELS)
        self.load_level(self.current_level)

    def update(self):
        if not self.splash.done:
            self.state = GameState.SPLASH
        elif self.game_over:
            self.state = GameState.GAME_OVER
        elif self.in_shop:
            self.state = GameState.SHOP
        elif self.in_settings:
            self.state = GameState.SETTINGS
        else:
            self.state = GameState.PLAYING

        if self.state == GameState.PLAYING:
            self.update_playing()
        elif self.state == GameState.SHOP:
            # Обновление состояния магазина, если нужно
            pass
        elif self.state == GameState.SETTINGS:
            # Обновление состояния настроек, если нужно
            pass
        elif self.state == GameState.GAME_OVER:
            # Обновление состояния game over, если нужно
            pass

    def update_playing(self):
        self.all_sprites.update()
        self.update_hearts()
        
        # Проверка достижения двери
        if self.door and pygame.sprite.collide_rect(self.player, self.door):
            if self.current_level == 9:  # После 10-го уровня (индекс 9)
                self.state = GameState.SHOP
                self.in_shop = True
            else:
                self.next_level()
        
        # Проверка окончания жизней
        if self.player.lives <= 0:
            self.state = GameState.GAME_OVER
            self.game_over = True
        
        # Проверка сбора монет
        coins_collected = pygame.sprite.spritecollide(self.player, self.coins, True)
        for coin in coins_collected:
            self.player.coins += 1

        # Проверка столкновения с врагами
        if pygame.sprite.spritecollideany(self.player, self.enemies):
            self.player.die()

        # Проверка сбора яйца
        if self.nest and not self.nest.collected:
            if pygame.sprite.collide_rect(self.player, self.nest):
                self.nest.collected = True
                self.player.has_egg = True
                self.nest.kill()

        # Проверка достижения чекпойнта
        if self.checkpoint and not self.checkpoint.activated:
            if pygame.sprite.collide_rect(self.player, self.checkpoint):
                self.checkpoint.activated = True
                self.checkpoint_level = self.current_level

    def apply_purchase(self, item):
        if item.name == "Дополнительное сердце":
            self.player.lives += 1
            self.player.initial_lives += 1
            self.update_hearts()
        elif item.name == "Тройной прыжок":
            self.player.max_jumps = 3
        elif item.name == "Высокий прыжок":
            self.player.jump_power = -12
        elif item.name == "Скорость":
            self.player.speed_x = 7 if self.player.speed_x > 0 else -7
        elif item.name == "Меч":
            self.player.has_sword = True  # Убедитесь, что это устанолео

    def handle_events(self, event):
        if self.state == GameState.SPLASH:
            self.handle_splash_events(event)
            return True
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_events(event)
        elif event.type == pygame.KEYDOWN:
            self.handle_keyboard_events(event)
        
        return False

    def handle_splash_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:  # Добавляем обработку F11 на главном экране
                try:
                    self.screen = self.toggle_fullscreen(self.settings)
                    # Обновляем размеры в splash
                    self.splash = Splash(self.settings.WINDOW_WIDTH, self.settings.WINDOW_HEIGHT)
                except Exception as e:
                    print(f"Ошибка при переключении режима: {e}")
                return
            
            if self.splash.settings.active:
                if event.key == pygame.K_ESCAPE:
                    self.splash.settings.active = False
                elif event.key == pygame.K_LEFT:
                    self.splash.settings.volume = max(0, self.splash.settings.volume - 0.1)
                    pygame.mixer.music.set_volume(self.splash.settings.volume)
                elif event.key == pygame.K_RIGHT:
                    self.splash.settings.volume = min(1, self.splash.settings.volume + 0.1)
                    pygame.mixer.music.set_volume(self.splash.settings.volume)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.splash.play_button_rect.collidepoint(event.pos):
                    self.splash.done = True
                elif self.splash.settings_button_rect.collidepoint(event.pos):
                    self.splash.settings.active = True

    def handle_mouse_events(self, event):
        if event.button == 1 and not self.game_over and not self.in_shop:
            if self.player.jump_count < self.player.max_jumps:
                self.player.speed_y = self.player.jump_power
                self.player.jump_count += 1
                self.player.on_ground = False
        elif event.button == 3:
            if self.player.has_sword:
                self.player.sword_active = True
                self.handle_sword_attack()

    def handle_keyboard_events(self, event):
        if self.state == GameState.GAME_OVER:
            if event.key == pygame.K_r:
                self.reset_game()
                self.state = GameState.PLAYING
        elif self.state == GameState.SHOP:
            self.handle_shop_events(event)
        elif self.state == GameState.SETTINGS:
            self.handle_settings_events(event)
        elif self.state == GameState.PLAYING:
            self.handle_gameplay_events(event)

    def check_collisions(self):
        # Проверка коллизий с п��атформам��
        for platform in self.platforms:
            if self.player.hitbox.colliderect(platform.rect):
                self.handle_platform_collision(platform)
            
    def handle_platform_collision(self, platform):
        if self.player.speed_y > 0:  # Падение на платформу
            self.player.rect.bottom = platform.rect.top + 8
            self.player.speed_y = 0
            self.player.on_ground = True
            self.player.jump_count = 0
        elif self.player.speed_y < 0:  # Удар головой
            self.player.rect.top = platform.rect.bottom - 8
            self.player.speed_y = 0

    def handle_gameplay_events(self, event):
        if event.key == pygame.K_s:
            self.in_settings = True
        elif event.key == pygame.K_ESCAPE:
            self.splash.done = False
        elif event.key == pygame.K_SPACE and self.player.jump_count < self.player.max_jumps:
            self.player.speed_y = self.player.jump_power
            self.player.jump_count += 1
            self.player.on_ground = False
        elif event.key == pygame.K_h and pygame.key.get_mods() & pygame.KMOD_CTRL:
            self.player.lives += 1
            self.player.initial_lives += 1
            self.update_hearts()
        elif event.key == pygame.K_n and pygame.key.get_mods() & pygame.KMOD_CTRL:
            if self.current_level < len(LEVELS) - 1:
                self.current_level += 1
                self.load_level(self.current_level)
        elif event.key == pygame.K_m and pygame.key.get_mods() & pygame.KMOD_CTRL:  # Добавляем новую комбинацию
            self.player.coins += 10  # Добавляем 10 монет
        elif event.key == pygame.K_e:
            if self.player.has_egg and not self.player.extra_armor:
                self.player.extra_armor = True
                self.player.has_egg = False
                self.player.armor_max += 1
                self.player.armor += 1
        elif event.key == pygame.K_F11:
            try:
                self.screen = self.toggle_fullscreen(self.settings)
                # Перезагружаем уровень для обновления спрайтов
                self.load_level(self.current_level)
                self.update_hearts()
                # Реинициализируем музыку
                pygame.mixer.quit()
                pygame.mixer.init()
                pygame.mixer.music.load(os.path.join('assets', 'sound', 'background.wav'))
                pygame.mixer.music.set_volume(self.settings.volume)
                pygame.mixer.music.play(-1)
            except Exception as e:
                print(f"Ошибка при переключении режима: {e}")

    def handle_settings_events(self, event):
        if event.key == pygame.K_ESCAPE:
            self.in_settings = False
        elif event.key == pygame.K_LEFT:
            self.settings.volume = max(0, self.settings.volume - 0.1)
            pygame.mixer.music.set_volume(self.settings.volume)
            self.settings.save_settings()
        elif event.key == pygame.K_RIGHT:
            self.settings.volume = min(1, self.settings.volume + 0.1)
            pygame.mixer.music.set_volume(self.settings.volume)
            self.settings.save_settings()

    def handle_shop_events(self, event):
        if event.key == pygame.K_ESCAPE:
            self.in_shop = False
            self.current_level = 10
            self.load_level(self.current_level)
        elif event.key == pygame.K_UP:
            self.shop.selected_item = (self.shop.selected_item - 1) % len(self.shop.items)
        elif event.key == pygame.K_DOWN:
            self.shop.selected_item = (self.shop.selected_item + 1) % len(self.shop.items)
        elif event.key == pygame.K_RETURN:
            selected_item = self.shop.items[self.shop.selected_item]
            if not selected_item.purchased and self.player.coins >= selected_item.cost:
                self.player.coins -= selected_item.cost
                selected_item.purchased = True
                self.apply_purchase(selected_item)

    def handle_sword_attack(self):
        sword_rect = pygame.Rect(
            self.player.rect.centerx + (20 if self.player.facing_right else -60),
            self.player.rect.centery - 10,
            60,  # Увеличиваем длину
            20   # Увеличиваем высоту
        )
        enemies_hit = [enemy for enemy in self.enemies if sword_rect.colliderect(enemy.rect)]
        for enemy in enemies_hit:
            enemy.die()

    def toggle_fullscreen(self, settings):
        settings.fullscreen = not settings.fullscreen
        
        # Получаем информацию о текущем дисплее
        display_info = pygame.display.Info()
        
        # Переключаем режим отображения
        if settings.fullscreen:
            # В полноэкранном режиме используем разрешение монитора
            return pygame.display.set_mode(
                (display_info.current_w, display_info.current_h),
                pygame.FULLSCREEN | pygame.SCALED
            )
        else:
            # В оконном режиме используем базовые размеры
            return pygame.display.set_mode(
                (settings.BASE_WIDTH, settings.BASE_HEIGHT)
            )

