import pygame
from .constants import Checker_1, Checker_2, BLUE, SQUARE_SIZE
from checkers.board import Board

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
    
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        
        # Подсветка выбранной клетки
        if self.selected_square:
            row, col = self.selected_square
            pygame.draw.rect(self.win, (255, 255, 0), (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4)
        
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.selected_square = None  # Добавлен атрибут для хранения выбранной клетки
        self.board = Board()
        self.turn = Checker_1
        self.valid_moves = {}

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.selected_square = None  # Сброс выделенной клетки при неудачном перемещении
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            # Получаем доступные ходы для всех шашек текущего цвета
            all_moves = {piece: self.board.get_valid_moves(piece) for row in self.board.board for piece in row if piece != 0 and piece.color == self.turn}

            # Проверяем, есть ли возможность съесть другую шашку текущего цвета
            can_capture = any(any(len(skipped) > 0 for skipped in moves.values()) for moves in all_moves.values())

            # Если есть возможность съесть другую шашку, разрешаем выбор только шашек,
            # которые могут съесть другую шашку
            if can_capture:
                moves = self.board.get_valid_moves(piece)
                if any(len(skipped) > 0 for skipped in moves.values()):
                    self.selected = piece
                    self.selected_square = (row, col)  # Сохраняем выбранную клетку
                    self.valid_moves = moves
                    return True
            # Если ни одна шашка не может съесть другую шашку, разрешаем выбор любой шашки
            elif any(all_moves.values()):
                self.selected = piece
                self.selected_square = (row, col)  # Сохраняем выбранную клетку
                self.valid_moves = self.board.get_valid_moves(piece)
                return True
        if piece == 0:
            self.valid_moves = {}
            self.draw_valid_moves(self.valid_moves)
            self.selected = piece
            self.selected_square = (row, col)
            
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            self.selected_square = (row, col)  # Обновляем выбранную клетку при перемещении
            skipped = self.valid_moves[(row, col)]
            self.valid_moves = {}
            if skipped:
                self.board.remove(skipped)
                self.valid_moves = self.board.get_valid_moves(self.selected)
                if any(self.valid_moves.values()):  
                    return True  
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == Checker_1:
            self.turn = Checker_2
        else:
            self.turn = Checker_1
