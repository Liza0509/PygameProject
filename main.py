import pygame
import random

items = [
    {"name": "Лёгкий клинок", "type": "weapon", "effect": 2, "cost": 100},
    {"name": "Тяжёлый меч", "type": "weapon", "effect": 5, "cost": 200},
    {"name": "Эпический меч", "type": "weapon", "effect": 10, "cost": 500},
    {"name": "Кожаная броня", "type": "armor", "effect": 10, "cost": 150},
    {"name": "Стальная броня", "type": "armor", "effect": 25, "cost": 400},
    {"name": "Мифриловая броня", "type": "armor", "effect": 50, "cost": 800},
]
# Инициализация Pygame
weapon = ''
armor = ''
pygame.init()
# Размеры окна и ячеек
CELL_SIZE = 50
GRID_SIZE = 10
WINDOW_SIZE = CELL_SIZE * GRID_SIZE
UI_HEIGHT = 150  # Высота для интерфейса

trader_position = None  # Позиция торговца
trader_visible = False  # Отображается ли торговец

# Установка размеров окна
screen = pygame.display.set_mode((WINDOW_SIZE,
                                  WINDOW_SIZE + UI_HEIGHT))
pygame.display.set_caption("Клеточное поле 10x10")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Шрифт для отображения текста
font = pygame.font.SysFont("Arial", 20)

# Загрузка и изменение размера изображений
miner_image = pygame.image.load("data/miner.png")
miner_image = pygame.transform.scale(miner_image,
                                     (CELL_SIZE, CELL_SIZE))
rock_image = pygame.image.load("data/rock.png")
rock_image = pygame.transform.scale(rock_image,
                                    (CELL_SIZE, CELL_SIZE))
spider_image = pygame.image.load("data/spider.png")
spider_image = pygame.transform.scale(spider_image,
                                      (CELL_SIZE, CELL_SIZE))
stairs_image = pygame.image.load("data/stairs.png")
stairs_image = pygame.transform.scale(stairs_image,
                                      (CELL_SIZE, CELL_SIZE))


# Функция для генерации нового уровня
def generate_level(level):
    global miner_position, rock_positions, \
        spider_positions, \
        spider_healths, stairs_position,\
        hidden_stairs,\
        trader_position, \
        trader_visible

    if level % 1 == 0:  # Уровень с торговцем
        trader_position = [random.randint(0,
                                          GRID_SIZE - 1),
                           random.randint(0, GRID_SIZE - 1)]
        miner_position = [random.randint(0, GRID_SIZE - 1),
                          random.randint(0, GRID_SIZE - 1)]
        while trader_position == miner_position:
            trader_position = [random.randint(0, GRID_SIZE - 1),
                               random.randint(0, GRID_SIZE - 1)]

        rock_positions = set()
        spider_positions = []
        spider_healths = []
        stairs_position = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]
        while stairs_position == miner_position or stairs_position == trader_position:
            stairs_position = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]

        hidden_stairs = False
        trader_visible = True
    else:
        # Обычная генерация уровня
        miner_position = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]
        rock_positions = set()
        while len(rock_positions) < (GRID_SIZE * 2):
            position = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
            if position != tuple(miner_position):
                rock_positions.add(position)

        stairs_position = random.choice(list(rock_positions))
        hidden_stairs = True
        spider_positions = []
        spider_healths = []
        for _ in range(level):
            spider_position = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]
            while (tuple(spider_position) == tuple(miner_position) or
                   tuple(spider_position) in rock_positions):
                spider_position = [random.randint(0,
                                                  GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]
            spider_positions.append(spider_position)
            spider_healths.append(10)


# Здоровье, урон и инвентарь
miner_health = 50
miner_damage = 5
miner_inventory = 0
spider_damage = 1
# Количество драгоценных камней
diamond_count = 0  # Алмазы
ruby_count = 0  # Рубины
emerald_count = 0  # Изумруды
money = 0
# Изначально первый уровень
generate_level(1)
level = 1


# Функция рисования сетки
def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)


# Проверка соседней клетки
def is_adjacent(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) == 1


def draw_buy_window():
    # Размеры окна
    window_width = 300
    window_height = 200
    window_x = (WINDOW_SIZE - window_width) // 2
    window_y = (WINDOW_SIZE - window_height) // 2

    # Рисуем окно
    pygame.draw.rect(screen, (200, 200, 200), (window_x, window_y, window_width, window_height))
    pygame.draw.rect(screen, BLACK, (window_x, window_y, window_width, window_height), 2)

    greeting_text = font.render("вот, что я могу предложить!", True, BLACK)
    screen.blit(greeting_text, (window_x + 20, window_y + 20))

    button_width = 260
    button_height = 40
    button_margin = 10
    button_x = window_x + 20
    button_y = window_y + 60  # Начальная позиция для первой кнопки

    buttons = []  # Список для хранения кнопок

    # Создаем и рисуем кнопки для каждого предмета
    for item_name in items:
        rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(screen, (70, 130, 180), rect)  # Цвет кнопки

        # Обычное отображение текста без font.render
        text_surface = font.render(str(item_name), True, (255, 255, 255))  # Генерация текста в текстовой поверхности
        screen.blit(text_surface, (rect.x + 10, rect.y + 10))  # Рисуем текст на кнопке с отступом

        # Добавляем кнопку в список
        buttons.append((rect, item_name))

        button_y += button_height + button_margin  # Смещение для следующей кнопки

    return buttons


def draw_trade_window():
    # Размеры окна
    window_width = 300
    window_height = 200
    window_x = (WINDOW_SIZE - window_width) // 2
    window_y = (WINDOW_SIZE - window_height) // 2

    # Рисуем окно
    pygame.draw.rect(screen, (200, 200, 200), (window_x, window_y, window_width, window_height))
    pygame.draw.rect(screen, BLACK, (window_x, window_y, window_width, window_height), 2)

    # Приветствие торговца
    greeting_text = font.render("Привет, я Торговец!", True, BLACK)
    screen.blit(greeting_text, (window_x + 20, window_y + 20))

    # Кнопка Продать
    sell_text = font.render("Продать камни", True, WHITE)
    sell_button = pygame.Rect(window_x + 50, window_y + 80, 200, 40)
    pygame.draw.rect(screen, GREEN, sell_button)
    screen.blit(sell_text, (sell_button.x + 20, sell_button.y + 10))

    buy_text = font.render("купить", True, WHITE)
    buy_button = pygame.Rect(window_x + 50, window_y + 160, 200, 40)
    pygame.draw.rect(screen, GREEN, buy_button)
    screen.blit(buy_text, (buy_button.x + 20, buy_button.y + 10))

    return sell_button, buy_button


f = False
# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            new_position = miner_position[:]
            if event.key == pygame.K_w:
                new_position[1] -= 1
            elif event.key == pygame.K_s:
                new_position[1] += 1
            elif event.key == pygame.K_a:
                new_position[0] -= 1
            elif event.key == pygame.K_d:
                new_position[0] += 1

            # Проверка границ и наличия камней
            if (0 <= new_position[0] < GRID_SIZE and
                    0 <= new_position[1] < GRID_SIZE and
                    tuple(new_position) not in rock_positions):
                miner_position = new_position

                # Движение пауков
                for i, spider_position in enumerate(spider_positions):
                    spider_new_position = spider_position[:]
                    direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
                    spider_new_position[0] += direction[0]
                    spider_new_position[1] += direction[1]

                    if (0 <= spider_new_position[0] < GRID_SIZE and
                            0 <= spider_new_position[1] < GRID_SIZE and
                            tuple(spider_new_position) not in rock_positions and
                            tuple(spider_new_position) != tuple(miner_position) and
                            tuple(spider_new_position) not in spider_positions):
                        spider_positions[i] = spider_new_position

                # Проверка столкновения
                for i, spider_position in enumerate(spider_positions):
                    if is_adjacent(miner_position, spider_position):
                        miner_health -= spider_damage
                        spider_healths[i] -= miner_damage
                        if spider_healths[i] <= 0:
                            spider_positions.pop(i)
                            spider_healths.pop(i)
                            break
        if event.type == pygame.MOUSEBUTTONDOWN and trader_visible:
            # Если шахтёр кликает на торговца
            if tuple(miner_position) == tuple(trader_position):
                # Отображаем диалоговое окно торговли (реализуй отдельно)
                # Обработка продажи
                money += (diamond_count * 10) + (ruby_count * 15) + (emerald_count * 20)  # Пример цен
                diamond_count = ruby_count = emerald_count = 0  # Сброс камней
        # Проверка взаимодействия с торговцем
        if trader_visible and is_adjacent(miner_position,
                                          trader_position):
            # Вызов всплывающего окна торговли
            draw_trade_window()

    # Обработка кликов мыши
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        mouse_x, mouse_y = event.pos
        clicked_cell = (mouse_x // CELL_SIZE,
                        mouse_y // CELL_SIZE)

        # Обработка кликов мыши
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            clicked_cell = (mouse_x // CELL_SIZE, mouse_y // CELL_SIZE)

            # Добыча камня
            # Добыча камня
            if (tuple(clicked_cell) in rock_positions and is_adjacent(miner_position,
                                                                      clicked_cell)):
                rock_positions.remove(tuple(clicked_cell))
                miner_inventory += 1

                # Шанс найти драгоценный камень

                chance = random.randint(1, 100)
                if chance <= 10:
                    diamond_count += 1
                elif chance <= 17:
                    ruby_count += 1
                elif chance <= 22:
                    emerald_count += 1

                # Открытие лестницы
                if clicked_cell == stairs_position:
                    hidden_stairs = False

                # Открытие лестницы
                if clicked_cell == stairs_position:
                    hidden_stairs = False

            # Переход на следующий уровень только при клике на лестницу
            if clicked_cell == stairs_position and not hidden_stairs:
                if is_adjacent(miner_position,
                               stairs_position):
                    level += 1
                    generate_level(level)

    # Заливка фона
    screen.fill(WHITE)
    # Рисуем сетку
    draw_grid()
    # Рисуем камни
    for position in rock_positions:
        screen.blit(rock_image, (position[0] * CELL_SIZE,
                                 position[1] * CELL_SIZE))
    # Рисуем лестницу, если она открыта
    if not hidden_stairs:
        if stairs_position is not None:
            screen.blit(stairs_image, (stairs_position[0] * CELL_SIZE, stairs_position[1] * CELL_SIZE))

    # Рисуем изображение шахтёра
    screen.blit(miner_image, (miner_position[0] * CELL_SIZE,
                              miner_position[1] * CELL_SIZE))
    # Рисуем пауков
    for spider_position in spider_positions:
        screen.blit(spider_image, (spider_position[0] * CELL_SIZE, spider_position[1] * CELL_SIZE))

    # Рисуем торговца, если он виден
    if trader_visible:
        trader_image = pygame.image.load("data/trader.png")
        trader_image = pygame.transform.scale(trader_image,
                                              (CELL_SIZE, CELL_SIZE))
        screen.blit(trader_image, (trader_position[0] * CELL_SIZE, trader_position[1] * CELL_SIZE))

    trading = False  # Флаг для торговли

    # Взаимодействие с торговцем
    if trader_visible and is_adjacent(miner_position,
                                      trader_position):
        trading = True

    if trading:
        if not f:
            sell_button, buy_button = draw_trade_window()  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        # if buy_button.collidepoint(mouse_x, mouse_y):
        #     buttons = draw_buy_window()
        # Обработка клика мыши
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            if buy_button.collidepoint(mouse_x,
                                       mouse_y):
                f = True
                continue
                # for i in range (len(buttons)):
                #     if buttons[i].collidepoint(mouse_x,mouse_y):
                #         pass
            if sell_button.collidepoint(mouse_x,
                                        mouse_y):  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                # Продажа камней
                money += miner_inventory * 2  # Продажа обычных камней
                money += diamond_count * 50  # Продажа алмазов
                money += ruby_count * 30  # Продажа рубинов
                money += emerald_count * 20  # Продажа изумрудов

                # Обнуляем инвентарь
                miner_inventory = 0
                diamond_count = 0
                ruby_count = 0
                emerald_count = 0
                trading = False  # Закрываем окно
    if f:
        buttons = draw_buy_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                print('vfdbhjnklmdfjdshv')
                new_position = miner_position[:]
                if event.key == pygame.K_w:
                    new_position[1] -= 1
                elif event.key == pygame.K_s:
                    new_position[1] += 1
                elif event.key == pygame.K_a:
                    new_position[0] -= 1
                elif event.key == pygame.K_d:
                    new_position[0] += 1
                    # Проверка границ и наличия камней
                if (0 <= new_position[0] < GRID_SIZE and
                        0 <= new_position[1] < GRID_SIZE and
                        tuple(new_position) not in rock_positions):
                    f = False
                    miner_position = new_position
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                for rect, item in buttons:
                    if rect.collidepoint(mouse_x, mouse_y):
                        # print(item['name'])
                        if item['name'] == "Лёгкий клинок":
                            if money <= 100:
                                print('недостаточно денег')
                            elif weapon == "Лёгкий клинок":
                                print(item['name'] + " уже куплен")
                                break
                            else:
                                money -= 100
                                weapon = "Лёгкий клинок"
                                miner_damage = 5 + 2
                                print('buy ' + item['name'], weapon)
                        elif item['name'] == "Тяжёлый меч":
                            if money <= 200:
                                print('недостаточно денег')
                            elif weapon == "Тяжёлый меч":
                                print(item['name'] + " уже куплен")
                                break
                            else:
                                money -= 200
                                weapon = "Тяжёлый меч"
                                miner_damage = 5 + 5
                                print('buy ' + item['name'], weapon)
                        elif item['name'] == "Эпический меч":
                            if money <= 500:
                                print('недостаточно денег')
                            elif weapon == "Эпический меч":
                                print(item['name'] + " уже куплен")
                                break
                            else:
                                money -= 500
                                weapon = "Эпический меч"
                                miner_damage = 5 + 10
                                print('buy ' + item['name'], weapon)
                        elif item['name'] == "Кожаная броня":
                            if money <= 150:
                                print('недостаточно денег')
                            elif armor == "Кожаная броня":
                                print(item['name'] + " уже куплен")
                                break
                            else:
                                money -= 150
                                armor = "Кожаная броня"
                                miner_health = 50 + 10
                                print('buy ' + item['name']
                                  , armor)
                        elif item['name'] == "Стальная броня":
                            if money <= 400:
                                print('недостаточно денег')
                            elif armor == "Стальная броня":
                                print(item['name'] + " уже куплен")
                                break
                            else:
                                money -= 400
                                armor = "Стальная броня"
                                miner_health = 50 + 25
                                print('buy ' + item['name'],
                                  armor)
                        elif item['name'] == "Мифриловая броня":
                            if money <= 800:
                                print('недостаточно денег')
                            elif armor == "Мифриловая броня":
                                print(item['name'] + " уже куплен")
                                break
                            else:
                                money -= 800
                                armor = "Мифриловая броня"
                                miner_health = 50 + 50
                                print('buy ' + item['name'],
                                  armor)
                        break

    # Отображение здоровья шахтёра
    miner_health_text = font.render(f"Шахтёр: {miner_health} HP",
                                    True, GREEN)
    screen.blit(miner_health_text, (100, WINDOW_SIZE + 10))
    # Отображение здоровья пауков
    for i, spider_position in enumerate(spider_positions):
        spider_health_text = font.render(f"Паук {i + 1}: {spider_healths[i]} HP",
                                         True, RED)
        screen.blit(spider_health_text, (WINDOW_SIZE - 150, 10 + i * 20))
    # Отображение
    inventory_text = font.render(f"Камни: {miner_inventory}", True, BLACK)
    screen.blit(inventory_text, (10, WINDOW_SIZE + 40))
    money_text = font.render(f"Монеты: {money}", True, BLACK)
    screen.blit(money_text, (100, WINDOW_SIZE + 100))
    damage_text = font.render(f"Урон: {miner_damage}", True, RED)
    screen.blit(damage_text, (100, WINDOW_SIZE + 50))

    diamond_text = font.render(f"Алмазы: {diamond_count}", True, (0, 255, 255))  # Голубой
    screen.blit(diamond_text, (10, WINDOW_SIZE + 70))
    ruby_text = font.render(f"Рубины: {ruby_count}", True, (255, 0, 0))  # Красный
    screen.blit(ruby_text, (10, WINDOW_SIZE + 100))
    emerald_text = font.render(
        f"Изумруды: {emerald_count}",
        True, (0, 255, 0)
    )  # Зелёный
    screen.blit(emerald_text,
                (10, WINDOW_SIZE + 130)
                )
    # Обновление экрана
    pygame.display.flip()
    # Проверка здоровья
    if miner_health <= 0:
        break
# Вывод результата
if miner_health <= 0:
    print(
        "Шахтёр проиграл!"
    )
# Завершение работы Pygame
pygame.quit()
