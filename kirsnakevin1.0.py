import os
import subprocess
from pathlib import Path
import pygame
import random
import time

def display_ascii_art():
    print(r"""
 ###       ####    ######            ##   ##    ##     ###  ##  #######   ###
  ##        ##      ##  ##           ###  ##   ####     ##  ##   ##   #    ##
  ##  ##    ##      ##  ##   #####   #### ##  ##  ##    ## ##    ## #      ##
  ## ##     ##      #####   ##       ## ####  ##  ##    ####     ####      ##
  ####      ##      ## ##    #####   ##  ###  ######    ## ##    ## #      ##
  ## ##     ##      ##  ##       ##  ##   ##  ##  ##    ##  ##   ##   #    ##
  ##  ##   ####    #### ##  ######   ##   ##  ##  ##   ###  ##  #######   ####
    """)

def find_exe_files():
    exe_files = []
    for file in Path('.').glob('*.exe'):
        exe_files.append(file.name)
    return sorted(exe_files)

def run_selected_program(choice, exe_files):
    if 1 <= choice <= len(exe_files):
        selected_exe = exe_files[choice-1]
        print(f"\nЗапускаем {selected_exe}...\n")
        try:
            subprocess.Popen([selected_exe], shell=True)
        except Exception as e:
            print(f"Ошибка при запуске: {e}")
    else:
        print("Неверный выбор!")

def run_snake_game():
    # Инициализация Pygame
    pygame.init()

    # Цвета
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)  # Добавим цвет для текста счета

    # Размеры экрана и блоков
    BLOCK_SIZE = 20
    SPEED = 15
    WIDTH, HEIGHT = 600, 400

    # Создание экрана
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Змейка')

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 30)
    score_font = pygame.font.SysFont(None, 35)  # Шрифт для счета

    def draw_snake(snake_list):
        for block in snake_list:
            pygame.draw.rect(screen, GREEN, [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])

    def message(msg, color):
        text = font.render(msg, True, color)
        screen.blit(text, [WIDTH / 6, HEIGHT / 3])

    def show_score(score):
        score_text = score_font.render(f"Счет: {score}", True, BLUE)
        screen.blit(score_text, [10, 10])  # Выводим счет в верхнем левом углу

    def game_loop():
        game_over = False
        game_close = False
        
        # Начальная позиция змейки
        x1 = WIDTH / 2
        y1 = HEIGHT / 2
        
        # Изменение позиции
        x1_change = 0
        y1_change = 0
        
        # Змейка
        snake_list = []
        length_of_snake = 1
        
        # Счетчик съеденных фруктов
        score = 0
        
        # Еда
        foodx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        foody = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        
        while not game_over:
            
            while game_close:
                screen.fill(BLACK)
                message(f"Игра окончена! Счет: {score} Нажмите Q-выход или C-играть снова", RED)
                pygame.display.update()
                
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_c:
                            game_loop()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and x1_change == 0:
                        x1_change = -BLOCK_SIZE
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT and x1_change == 0:
                        x1_change = BLOCK_SIZE
                        y1_change = 0
                    elif event.key == pygame.K_UP and y1_change == 0:
                        y1_change = -BLOCK_SIZE
                        x1_change = 0
                    elif event.key == pygame.K_DOWN and y1_change == 0:
                        y1_change = BLOCK_SIZE
                        x1_change = 0
            
            # Проверка границ
            if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
                game_close = True
                
            x1 += x1_change
            y1 += y1_change
            screen.fill(BLACK)
            
            # Рисуем еду
            pygame.draw.rect(screen, RED, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])
            
            # Обновляем змейку
            snake_head = []
            snake_head.append(x1)
            snake_head.append(y1)
            snake_list.append(snake_head)
            
            if len(snake_list) > length_of_snake:
                del snake_list[0]
                
            # Проверка на столкновение с собой
            for block in snake_list[:-1]:
                if block == snake_head:
                    game_close = True
                    
            draw_snake(snake_list)
            
            # Отображаем счет
            show_score(score)
            
            pygame.display.update()
            
            # Проверка съела ли змейка еду
            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
                foody = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
                length_of_snake += 1
                score += 1  # Увеличиваем счет при съедании фрукта
                
            clock.tick(SPEED)
            
        pygame.quit()
        quit()

    game_loop()

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        display_ascii_art()
        
        exe_files = find_exe_files()
        
        if not exe_files:
            print("В этой папке не найдено .exe файлов!")
            print("Нажмите Enter для запуска Змейки или 0 для выхода")
        else:
            print("Что вы хотите запустить?")
            for i, exe in enumerate(exe_files, 1):
                print(f"{i}) {exe}")
            print("\n0) Выход")
            print("Нажмите Enter для запуска Змейки")
        
        user_input = input("\nВаш выбор: ").strip()
        
        if user_input == "":
            run_snake_game()
        elif user_input == "0":
            break
        else:
            try:
                choice = int(user_input)
                if exe_files:
                    run_selected_program(choice, exe_files)
                else:
                    print("Неверный ввод! Попробуйте снова.")
            except ValueError:
                print("Пожалуйста, введите число!")
        
        if user_input != "":
            input("\nНажмите Enter чтобы продолжить...")

if __name__ == "__main__":
    main()
#v
