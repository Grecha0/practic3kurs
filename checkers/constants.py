import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

# rgb
Checker_1 = (69, 43, 18) #шашка #DARK_BROWN
Checker_2 = (255, 255, 255) #шашка 
Bucket_2 = (245, 233, 219) # квадрат поля на котором шашки не стоят #MILK
Bucket_1 = (166, 100, 39) # квадрат поля на котором шашки стоят #BROWN
BLUE = (0, 0, 255)
GREY = (128,128,128)


CROWN = pygame.transform.scale(pygame.image.load('image/crown.png'), (44, 25))
