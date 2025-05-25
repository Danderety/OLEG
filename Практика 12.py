# import pygame
# import random
# import time

# # Инициализация pygame
# pygame.init()

# # Цвета
# WHITE = (0, 200, 255)
# BLACK = (0, 0, 0)
# RED = (255, 0, 0)
# GREEN = (0, 255, 0)
# BLUE = (0, 0, 255)

# # Настройки игры
# WIDTH, HEIGHT = 600, 400
# GRID_SIZE = 20
# GRID_WIDTH = WIDTH // GRID_SIZE
# GRID_HEIGHT = HEIGHT // GRID_SIZE
# FPS = 20

# # Настройка экрана
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Змейка")
# clock = pygame.time.Clock()

# class Snake:
#     def __init__(self):
#         self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
#         self.direction = (1, 0)
#         self.length = 1
#         self.score = 0
#         self.color = GREEN
    
#     def get_head_position(self):
#         return self.positions[0]
    
#     def update(self):
#         head_x, head_y = self.get_head_position()
#         dir_x, dir_y = self.direction
#         new_x = (head_x + dir_x) % GRID_WIDTH
#         new_y = (head_y + dir_y) % GRID_HEIGHT
        
#         # Проверка на столкновение с собой
#         if (new_x, new_y) in self.positions[1:]:
#             return False
        
#         self.positions.insert(0, (new_x, new_y))
#         if len(self.positions) > self.length:
#             self.positions.pop()
        
#         return True
    
#     def change_direction(self, new_direction):
#         # Запрещаем движение в противоположном направлении
#         if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
#             self.direction = new_direction
    
#     def grow(self):
#         self.length += 1
#         self.score += 1
    
#     def draw(self, surface):
#         for position in self.positions:
#             rect = pygame.Rect(position[0] * GRID_SIZE, position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
#             pygame.draw.rect(surface, self.color, rect)
#             pygame.draw.rect(surface, BLACK, rect, 1)

# class Food:
#     def __init__(self):
#         self.position = (0, 0)
#         self.color = RED
#         self.randomize_position()
    
#     def randomize_position(self):
#         self.position = (random.randint(0, GRID_WIDTH - 1), (random.randint(0, GRID_HEIGHT - 1)))
    
#     def draw(self, surface):
#         rect = pygame.Rect(self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
#         pygame.draw.rect(surface, self.color, rect)
#         pygame.draw.rect(surface, BLACK, rect, 1)

# def draw_grid(surface):
#     for y in range(0, HEIGHT, GRID_SIZE):
#         for x in range(0, WIDTH, GRID_SIZE):
#             rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
#             pygame.draw.rect(surface, WHITE, rect)
#             pygame.draw.rect(surface, BLACK, rect, 1)

# def show_game_over(surface, score):
#     surface.fill(WHITE)
#     font = pygame.font.SysFont('arial', 36)
#     text = font.render(f"Игра окончена! Счет: {score}", True, BLACK)
#     text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
    
#     restart_font = pygame.font.SysFont('arial', 24)
#     restart_text = restart_font.render("Нажмите R для рестарта или Q для выхода", True, BLACK)
#     restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
    
#     surface.blit(text, text_rect)
#     surface.blit(restart_text, restart_rect)
#     pygame.display.update()

# def main():
#     snake = Snake()
#     food = Food()
#     running = True
#     game_over = False
    
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             elif event.type == pygame.KEYDOWN:
#                 if game_over:
#                     if event.key == pygame.K_r:
#                         # Рестарт игры
#                         snake = Snake()
#                         food = Food()
#                         game_over = False
#                     elif event.key == pygame.K_q:
#                         running = False
#                 else:
#                     if event.key == pygame.K_UP:
#                         snake.change_direction((0, -1))
#                     elif event.key == pygame.K_DOWN:
#                         snake.change_direction((0, 1))
#                     elif event.key == pygame.K_LEFT:
#                         snake.change_direction((-1, 0))
#                     elif event.key == pygame.K_RIGHT:
#                         snake.change_direction((1, 0))
        
#         if not game_over:
#             # Обновление игры
#             if not snake.update():
#                 game_over = True
            
#             # Проверка на съедение еды
#             if snake.get_head_position() == food.position:
#                 snake.grow()
#                 food.randomize_position()
#                 # Убедимся, что еда не появилась в змейке
#                 while food.position in snake.positions:
#                     food.randomize_position()
            
#             # Отрисовка
#             screen.fill(WHITE)
#             draw_grid(screen)
#             snake.draw(screen)
#             food.draw(screen)
            
#             # Отображение счета
#             font = pygame.font.SysFont('arial', 20)
#             score_text = font.render(f"Счет: {snake.score}", True, BLACK)
#             screen.blit(score_text, (5, 5))
            
#             pygame.display.update()
#         else:
#             show_game_over(screen, snake.score)
        
#         clock.tick(FPS)
    
#     pygame.quit()

# if __name__ == "__main__":
#     main()




# class Soda:
#     def __init__(self, ingredient=None):
#         if isinstance(ingredient, str):
#             self.ingredient = ingredient
#         else:
#             self.ingredient = None

#     def show_my_drink(self):
#         if self.ingredient:
#             print(f'Газировка и {self.ingredient}')
#         else:
#             print('Обычная газировка')

 
# # Тесты
# drink1 = Soda()
# drink2 = Soda('малина')
# drink3 = Soda(5)
# drink1.show_my_drink()
# drink2.show_my_drink()
# drink3.show_my_drink()

# class Nikola:
#     __slots__ = ['name','age']
#     def __init__(self,name,age):
#         if name == "Николай":
#             self.name=name
#         else:
#             self.name=f'Я не {name}, а Николай'

#         self.age=age


# ppers = Nikola('Иван', 23)
# pers = Nikola("Николай", 12)
# print(ppers.name)
# print(pers.name)




class Book:
    def __init__(self, title, author, year, format):
        self.title = title
        self.author = author
        self.year = year
        self.format = format

    def info(self):
        return f"Название: {self.title}, Автор: {self.author}, Год: {self.year}, Формат: {self.format}"
    def __str__(self):
        return self.info()






class Libary:
    def __init__(self):
        self.books=[]

    def add_book(self,book):
        self.books.append(book)

    def show_books(self):
        for book in self.books:
            print(book.info())
lib = (Libary())

lib.add_book( Book("1984", "Джордж Оруэлл", 1949, 'TXT'))
lib.add_book( Book("1984", "Джордж Оруэлл", 1949, 'PDF'))


lib.show_books()