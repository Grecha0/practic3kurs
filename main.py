import pygame
import sys
from button import ImageButton
import pygame
import sys
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, Checker_1, Checker_2, BLUE, GREY, Bucket_1, Bucket_2
from checkers.game import Game

# Инициализация pygame
pygame.init()

# Параметры экрана
WIDTH, HEIGHT = 800, 800
MAX_FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

screen = pygame.display.set_mode((WIDTH, HEIGHT))
main_background = pygame.image.load("image/background1.jpg")
game_background = pygame.image.load("image/background2.jpg")
setting_background_0 = pygame.image.load("image/background3_0.jpg")
setting_background_1 = pygame.image.load("image/background3_1.jpg")
ii_background = pygame.image.load("image/background4.jpg")
clock = pygame.time.Clock()

# Загрузка и установка курсора
cursor = pygame.image.load("image/cursor.png")
pygame.mouse.set_visible(False)  # Скрываем стандартный курсор

def main_menu():
    # Создание кнопок
    start_button = ImageButton(WIDTH/2-(252/2), 330, 252, 74, "", "image/green_button2.jpg", "image/green_button2_hover.jpg", "mp3/click.wav")
    settings_button = ImageButton(WIDTH/2-(252/2), 385, 252, 74, "", "image/green_button2.jpg", "image/green_button2_hover.jpg", "mp3/click.wav")
    exit_button = ImageButton(WIDTH/2-(252/2), 435, 252, 74, "", "image/green_button2.jpg", "image/green_button2_hover.jpg", "mp3/click.wav")

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == start_button:
                print("Кнопка 'Старт' была нажата!")
                fade()
                new_game()

            if event.type == pygame.USEREVENT and event.button == settings_button:
                print("Кнопка 'Настройки' была нажата!")
                fade()
                settings_menu()

            if event.type == pygame.USEREVENT and event.button == exit_button:
                running = False
                pygame.quit()
                sys.exit()

            for btn in [start_button, settings_button, exit_button]:
                btn.handle_event(event)

        for btn in [start_button, settings_button, exit_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        # Отображение курсора в текущей позиции мыши
        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x-2, y-2))

        pygame.display.flip()

current_background = setting_background_0
def settings_menu():
    global current_background
    global Checker_1
    global Bucket_1
    global Bucket_2
    # Создание кнопок
    theme_button = ImageButton(WIDTH/2-(252/2), 320, 252, 74, "", "image/green_button2.jpg", "image/green_button2_hover.jpg", "mp3/click.wav")
    back_button = ImageButton(WIDTH/2-(252/2), 380, 252, 74, "", "image/green_button2.jpg", "image/green_button2_hover.jpg", "mp3/click.wav")

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(current_background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Возврат в меню
                if event.key == pygame.K_ESCAPE:
                    fade()
                    running = False

            if event.type == pygame.USEREVENT and event.button == back_button:
                print(Checker_1, Bucket_1, Bucket_2)
                fade()
                running = False

            if event.type == pygame.USEREVENT and event.button == theme_button:
                # При нажатии кнопки смены темы меняем текущий фон
                if current_background == setting_background_0:
                    current_background = setting_background_1
                    Checker_1 = (0, 0, 0)
                    Bucket_1 = (96, 96, 96)
                    Bucket_2 = (255, 255, 255)
                elif current_background == setting_background_1:
                    current_background = setting_background_0
                    Checker_1 = (69, 43, 18)
                    Bucket_1 = (166, 100, 39)
                    Bucket_2 = (245, 233, 219)
                
            for btn in  [theme_button, back_button]:
                btn.handle_event(event)

        for btn in [theme_button, back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        # Отображение курсора в текущей позиции мыши
        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x-2, y-2))

        pygame.display.flip()

def new_game():
    print(Checker_1, Bucket_1, Bucket_2)
    # Создание кнопок
    local_button = ImageButton(WIDTH/2-(252/2), 330, 252, 74, "", "image/green_button2.jpg", "image/green_button2_hover.jpg", "mp3/click.wav")
    ii_button = ImageButton(WIDTH/2-(252/2), 380, 252, 74, "", "image/green_button2.jpg", "image/green_button2_hover.jpg", "mp3/click.wav")
    back_button = ImageButton(WIDTH/2-(252/2), 430, 252, 74, "", "image/green_button2.jpg", "image/green_button2_hover.jpg", "mp3/click.wav")

    running = True
    while running:
        screen.fill((0, 0, 0))

        screen.blit(game_background, (0, 0))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Возврат в меню
                if event.key == pygame.K_ESCAPE:
                    running = False

            # Возврат в меню
            if event.type == pygame.USEREVENT and event.button == back_button:
                running = False

            if event.type == pygame.USEREVENT and event.button == local_button:
                fade()
                new_game_local()

            if event.type == pygame.USEREVENT and event.button == ii_button:
                fade()
                new_game_ii()

            for btn in [ii_button, local_button, back_button]:
                btn.handle_event(event)

        for btn in [ii_button, local_button,back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        # Отображение курсора в текущей позиции мыши
        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x-2, y-2))

        pygame.display.flip()

def new_game_ii():
    izi_button = ImageButton(WIDTH/2-(252/2), 300, 252, 74, "", "image/green_button2.jpg", "image/green_button2_hover.jpg", "mp3/click.wav")
    medium_button = ImageButton(WIDTH/2-(252/2), 355, 252, 74, "", "image/green_button2.jpg", "image/green_button2_hover.jpg", "mp3/click.wav")
    hard_button = ImageButton(WIDTH/2-(252/2), 410, 252, 74, "", "image/green_button2.jpg", "image/green_button2_hover.jpg", "mp3/click.wav")
    back_button = ImageButton(WIDTH/2-(252/2), 450, 252, 74, "", "image/green_button2.jpg", "image/green_button2_hover.jpg", "mp3/click.wav")

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(ii_background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Возврат в меню
                if event.key == pygame.K_ESCAPE:
                    fade()
                    running = False

            if event.type == pygame.USEREVENT and event.button == back_button:
                fade()
                running = False

            for btn in  [izi_button, medium_button, hard_button, back_button]:
                btn.handle_event(event)

        for btn in [izi_button, medium_button, hard_button, back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        # Отображение курсора в текущей позиции мыши
        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x-2, y-2))

        pygame.display.flip()

# затемнение
def fade():
    running = True
    fade_alpha = 0  # Уровень прозрачности для анимации

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Анимация затухания текущего экрана
        fade_surface = pygame.Surface((WIDTH, HEIGHT))
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))

        # Увеличение уровня прозрачности
        fade_alpha += 5
        if fade_alpha >= 105:
            fade_alpha = 255
            running = False

        pygame.display.flip()
        clock.tick(MAX_FPS)  # Ограничение FPS
        
        
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col
        
        
def new_game_local():
    
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(MAX_FPS)

        if game.winner() != None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()
        
        # Отображение курсора в текущей позиции мыши
        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x-2, y-2))

        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main_menu()