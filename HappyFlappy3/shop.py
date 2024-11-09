import pygame

class ShopItem:
    def __init__(self, name, cost, description):
        self.name = name
        self.cost = cost
        self.description = description
        self.purchased = False

class Shop:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.items = [
            ShopItem("Дополнительное сердце", 5, "Добавляет одну жизнь"),
            ShopItem("Тройной прыжок", 10, "Позволяет прыгать три раза"),
            ShopItem("Высокий прыжок", 15, "Увеличивает высоту прыжка"),
            ShopItem("Скорость", 20, "Увеличивает скорость бега"),
            ShopItem("Меч", 0, "Убивает врагов при нажатии ПКМ")
        ]
        self.selected_item = 0
        self.font = pygame.font.Font(None, 30)
        
    def draw(self, screen, coins):
        # Затемнение фона
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))
        
        # Заголовок магазина
        title = self.font.render("МАГАЗИН", True, (255, 255, 255))
        coins_text = self.font.render(f"Монеты: {coins}", True, (255, 215, 0))
        screen.blit(title, (self.screen_width//2 - title.get_width()//2, 50))
        screen.blit(coins_text, (self.screen_width//2 - coins_text.get_width()//2, 100))
        
        # Отрисовка предметов
        for i, item in enumerate(self.items):
            color = (255, 255, 0) if i == self.selected_item else (255, 255, 255)
            if item.purchased:
                color = (100, 100, 100)
            
            y_pos = 150 + i * 60
            item_text = self.font.render(f"{item.name} - {item.cost} монет", True, color)
            desc_text = self.font.render(item.description, True, color)
            
            if i == self.selected_item:
                pygame.draw.rect(screen, color, (
                    self.screen_width//2 - item_text.get_width()//2 - 10,
                    y_pos - 5,
                    item_text.get_width() + 20,
                    item_text.get_height() + 10
                ), 2)
            
            screen.blit(item_text, (self.screen_width//2 - item_text.get_width()//2, y_pos))
            screen.blit(desc_text, (self.screen_width//2 - desc_text.get_width()//2, y_pos + 20))
        
        # Инструкции
        instructions = self.font.render("↑↓ - Выбор, ENTER - Купить, ESC - Выход", True, (255, 255, 255))
        screen.blit(instructions, (self.screen_width//2 - instructions.get_width()//2, self.screen_height - 50)) 