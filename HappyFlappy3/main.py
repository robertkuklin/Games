import pygame
import sys
import os
from game import Game
from settings import Settings
from coin import Coin

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

# Создаем настройки
settings = Settings(800, 600)

# Создание окна (только полноэкранный режим)
screen = pygame.display.set_mode(
    (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT),
    pygame.SCALED
)

pygame.display.set_caption("HappyFlappy")
clock = pygame.time.Clock()

# Загрузка и воспроизведение музыки
try:
    pygame.mixer.music.load(os.path.join('assets', 'sound', 'background.wav'))
    pygame.mixer.music.set_volume(settings.volume)
    pygame.mixer.music.play(-1)
except:
    print("Не удалось загрузить фоновую музыку")

# Создание игры
game = Game(screen, settings)

# Игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            # Используем новую систему обработки событий
            should_continue = game.handle_events(event)
            if should_continue:
                continue

    # Управление
    keys = pygame.key.get_pressed()
    if game.player.is_alive and not game.game_over:
        game.player.speed_x = 0
        for key in game.settings.CONTROLS['LEFT']:
            if keys[key]:
                game.player.speed_x = -game.settings.PLAYER_SPEED
        for key in game.settings.CONTROLS['RIGHT']:
            if keys[key]:
                game.player.speed_x = game.settings.PLAYER_SPEED

    # Обновление
    game.update()
    game.check_collisions()

    # Отрисовка
    if not game.splash.done:
        game.splash.draw(screen)
    else:
        if game.in_settings:
            game.settings.draw(screen)
        else:
            screen.fill(game.settings.WHITE)
            game.all_sprites.draw(screen)
            game.hearts.draw(screen)
            game.draw_armor(screen)
            
            # Отображение текста
            level_text = game.settings.font.render(
                f"Уровень: {game.current_level + 1}", 
                True, 
                game.settings.BLACK
            )
            screen.blit(level_text, (game.settings.WINDOW_WIDTH // 2 - level_text.get_width() // 2, 10))
            
            # Отображение счетчика монет
            coin = Coin(0, 0)  # Создаем монету для иконки
            coin_pos = (game.settings.WINDOW_WIDTH - 150, 15)  # Позиция для иконки
            screen.blit(coin.image, coin_pos)  # Отображаем иконку монеты

            # Отображаем количество монет
            coin_text = game.settings.font.render(
                f"x {game.player.coins}", 
                True, 
                (218, 165, 32)  # Золотой цвет
            )
            screen.blit(coin_text, (coin_pos[0] + 30, coin_pos[1]))  # Смещаем текст правее иконки

            if game.game_over:
                game_over_text = game.settings.font.render(
                    "GAME OVER! Нажмите R для перезапуска", 
                    True, 
                    game.settings.BLACK
                )
                text_rect = game_over_text.get_rect(
                    center=(game.settings.WINDOW_WIDTH/2, game.settings.WINDOW_HEIGHT/2)
                )
                screen.blit(game_over_text, text_rect)
            
            if game.in_shop:
                game.shop.draw(screen, game.player.coins)
            
            game.player.draw_sword(screen)

            if game.player.has_egg:
                egg_text = game.settings.font.render(
                    "E - Использовать яйцо", 
                    True, 
                    game.settings.BLACK
                )
                screen.blit(egg_text, (10, game.settings.WINDOW_HEIGHT - 30))

    pygame.display.flip()
    clock.tick(game.settings.FPS)

pygame.quit()
sys.exit() 