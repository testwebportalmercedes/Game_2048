import random
from logics import *
import pygame
import sys
from  database import  get_best, cur, insert_result
import json
import os # функции по работе с файловой системой


GAMERS_BD = get_best()

def draw_top_gamers():
    font_top = pygame.font.SysFont('comicsansms', 30) # Создаем шрифт для лучших играков
    font_gamer = pygame.font.SysFont('comicsansms', 15) # Создаем шрифт для лучших играков
    text_head = font_top.render('Best tries :', True, COLOR_SCOPE)  # Задаем шрифт для лучших играков
    screen.blit(text_head, (250,0))  # размещаем текст по координатам
    for index,gamer in enumerate(GAMERS_BD):
        name, scope = gamer
        s = f"{index+1}. {name} - {scope}"
        text_gamer = font_gamer.render(s, True, COLOR_SCOPE)  # Задаем шрифт для лучших играков
        screen.blit(text_gamer, (250, 30+25*index))  # размещаем текст по координатам


def draw_interface(score, delta = 0):  # функция отрисовки
    pygame.draw.rect(screen, WHITE, TITLE_REC)  # тогда передаем это
    font = pygame.font.SysFont('comicsansms', 70)  # Создаем шрифт
    font_score = pygame.font.SysFont('comicsansms', 48) # Создаем шрифт для score
    font_delta = pygame.font.SysFont('comicsansms', 35) # Создаем шрифт для score

    text_score = font_score.render('Score: ',True, COLOR_SCOPE) # Задаем шрифт
    text_score_value = font_score.render(f'{score}',True, COLOR_SCOPE) # Задаем шрифт для счетчика
    screen.blit(text_score, (20,15))  # размещаем текст по координатам
    screen.blit(text_score_value, (175,15))  # размещаем текст счета по координатам
    if delta >0:
        text_delta = font_delta.render(f'+{delta}', True, COLOR_SCOPE)  # Задаем шрифт
        screen.blit(text_delta, (170, 65)) #размещаем текст по координатам
    pretty_print(mas)
    draw_top_gamers()
    for row in range(BLOCK):
        for colum in range(BLOCK):
            value = mas[row][colum]  # находим значение которое храниться а массиве
            text = font.render(f'{value}', True, BLACK)  # Задаем цвет нашему тексту
            w = colum * BLOCK_SIZE + (colum + 1) * MARGIN  # Получаем значения размеров
            h = row * BLOCK_SIZE + (row + 1) * MARGIN + 110  # Получаем значения размеров
            pygame.draw.rect(screen, COLORS[value], (w, h, 110, 110))  # Создаем квадраты по размером
            if value != 0:
                font_w, font_h = text.get_size()  # размеры шрифта
                text_x = w + (BLOCK_SIZE - font_w) / 2  # координаты текста по х
                text_y = h + (BLOCK_SIZE - font_h) / 2  # координаты текста по y
                screen.blit(text, (text_x, text_y))  # к экрану прикрепляем текст


COLOR_SCOPE = (255,127,0)

COLORS = {
    0: (130, 130, 130),
    2: (255, 255, 255),
    4: (255, 255, 128),
    8: (255, 255, 0),
    16: (255, 235, 255),
    32: (255, 235, 255),
    64: (255, 235, 0),
    128: (255, 127, 0),
    256: (255, 127, 127),
    512: (255, 0, 127),
    1024: (255, 0, 127),
    2048: (127, 0, 127),
}
WHITE = (255, 255, 255)
GRAY = (130, 130, 130)
BLACK = (0, 0, 0)

BLOCK = 4
BLOCK_SIZE = 110
MARGIN = 10
WIDTH = BLOCK * BLOCK_SIZE + (BLOCK + 1) * MARGIN
HEIGHT = WIDTH + 110
TITLE_REC = pygame.Rect(0, 0, WIDTH, 110)
def init_const(): #функция для обнуления массива и счета
    global score,mas
    mas = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],

    ]
    score = 0               # переменная счета
    # Для начала игры с рандомными числами 2 или 4 в начале игры
    empty = get_empty_list(mas)  # Получаем наш список в котором стоят нули
    random.shuffle(empty)  # перемешиваем его
    random_num1 = empty.pop()  # получаем последний элемент
    random_num2 = empty.pop()  # получаем последний элемент

    x1, y1 = get_index_from_number(random_num1)  # Получаем координаты этого элемента
    mas = insert_2_or_4(mas, x1, y1)  # добавляем по этим координатам 2 или 4
    x2, y2 = get_index_from_number(random_num2)  # Получаем координаты этого элемента
    mas = insert_2_or_4(mas, x2, y2)  # добавляем по этим координатам 2 или 4
score = None
mas = None
USERNAME = None

path = os.getcwd() # сохраняем путь к проекту в переменную
if 'data.txt' in os.listdir(path): #Проверяем нашу файйл в нашей директории
    with open('data.txt') as file: # открыть файл
        data = json.load(file) # передаем в дату наш открытый файл
        score = data['score']
        mas = data['mas']
        USERNAME = data['user']
    full_path = os.path.join(path,'data.txt')#полный путь к файлу
    os.remove(full_path) #Удоляем файл
else:
    init_const()  # инициализация начальной матрицы
# print(get_empty_list(mas))
pretty_print(mas)




pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2048')

def draw_intro():
    img2048 = pygame.image.load('2048_logo.png')
    font = pygame.font.SysFont('comicsansms', 60)  # Создаем шрифт
    text_welcome = font.render('Welcome! ', True, WHITE)   # Задаем шрифт для welcom

    name = 'Введите имя'
    # для приметственного меню
    is_find_name = False  # Изначально имя не найдено

    while not is_find_name:
        for event in pygame.event.get():  # Функция для выхода из игры
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:  # обработка ввода текста удаления и энтер
                if event.unicode.isalpha():
                    if name =='Введите имя':
                        name = event.unicode
                    else:
                        name +=event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(name)>2:
                        global USERNAME
                        USERNAME = name
                        is_find_name = True
                        break

        screen.fill(BLACK)                          # Закрашиввем экран черным
        text_name = font.render(name, True, WHITE)  # Задаем шрифт для ввода
        rect_name = text_name.get_rect()
        rect_name.center = screen.get_rect().center
        screen.blit(pygame.transform.scale(img2048, [200,200]),[10,10])   # функция для изменения размера картинки
        screen.blit(text_welcome, (220, 80))  # размещаем текст по координатам
        screen.blit(text_name, rect_name)  # размещаем текст по координатам
        pygame.display.update()  # обновляем дисплей

    screen.fill(BLACK)  # Закрашиввем экран черным

def draw_geme_over():#функция для гейм овера
    global USERNAME, GAMERS_BD
    img2048 = pygame.image.load('2048_logo.png')
    font = pygame.font.SysFont('comicsansms', 35)  # Создаем шрифт Game over!
    text_game_over = font.render('Game over!', True, WHITE)  # Задаем текст для Game over!
    text_scope = font.render(f'Вы набрали: {score}', True, WHITE)  # Задаем текст для очков после проигрыша
    best_score = GAMERS_BD[0][1] #берем из базы данных из кортежа наш счет
    if score > best_score:
        text = 'Рекорд побит'
    else:
        text = f"Лучший результат: {best_score}"
    text_record = font.render(text, True, WHITE)  # Задаем текст для Game over!
    insert_result(USERNAME,score) # добавляем имя и результат в бд
    GAMERS_BD = get_best()

    make_disiction = False  #решение о новой игре
    while not make_disiction: # Игра идет пока ...

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # событие для выхода из игры
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN: # Если нажата другая кнопка
                if event.key == pygame.K_SPACE:
                    make_disiction = True # Перезапуск игры с этим же именем
                    init_const()
                elif event.key == pygame.K_RETURN:
                    USERNAME = None
                    make_disiction = True # Перезапуск игры с новым именем
                    init_const()

        screen.fill(BLACK)  # Закрашиввем экран черным
        screen.blit(text_game_over, (220, 80))  # размещаем текст гейм овер по координатам
        screen.blit(text_scope, (80, 300))  # размещаем текст кол-во очков по координатам
        screen.blit(text_record, (10, 400))  # размещаем текст рекорда по координатам
        screen.blit(pygame.transform.scale(img2048, [200,200]),[10,10])   # функция для изменения размера картинки
        pygame.display.update()  # обновляем дисплей
    screen.fill(BLACK)

def save_game():
    data = {
        'user' :USERNAME,
        'score': score,
        'mas': mas
    }
    with open('data.txt','w') as outfile:
        json.dump(data, outfile) #говорим что и куда хотим сохранить

def game_loop():
    global score,mas
    draw_interface(score)  # Функция отрисовки
    pygame.display.update()  # обновляем дисплей
    is_mas_move = False
    while is_zero_in_mas(mas) or can_move(mas):
        for event in pygame.event.get():  # Функция для выхода из игры
            if event.type == pygame.QUIT:
                save_game()
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:  # если тип события любая нажитая кнопка
                delta = 0
                if event.key ==pygame.K_LEFT:  #Если действие равно нажатие влево
                    mas,delta, is_mas_move = move_left(mas)       #Равен новому массиву

                elif event.key ==pygame.K_RIGHT:
                    mas,delta, is_mas_move = move_right(mas)

                elif event.key ==pygame.K_UP:
                    mas,delta,is_mas_move = move_up(mas)

                elif event.key ==pygame.K_DOWN:
                    mas,delta,is_mas_move = move_down(mas)

                score +=delta
                if is_zero_in_mas(mas) and is_mas_move:

                    empty = get_empty_list(mas)  # Получаем наш список в котором стоят нули
                    random.shuffle(empty)  # перемешиваем его
                    random_num = empty.pop()  # получаем последний элемент

                    x, y = get_index_from_number(random_num)  # Получаем координаты этого элемента
                    mas = insert_2_or_4(mas, x, y)  # добавляем по этим координатам 2 или 4
                    print(f'мы заполнили элемент под номером {random_num}')
                draw_interface(score, delta)                # Функция отрисовки
                pygame.display.update()  # обновляем дисплей
                is_mas_move = False
while True: # Для запуска игры с прежнем именем
    if USERNAME is None:
        draw_intro()  #Начальная заставка
    game_loop()   #Сам процесс игры
    draw_geme_over()  #Вызов функции гейм овер