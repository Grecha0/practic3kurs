import pygame
from checkers.constants import Checker_1, Checker_2, BLUE, SQUARE_SIZE
from checkers.board import Board

class Game:
    def __init__(self, win):
        self._init()
        self.current_player = 'brown'  # Текущий игрок (начинает коричневый)
        self.win = win

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        
        if self.selected_square:
            row, col = self.selected_square
            pygame.draw.rect(self.win, (255, 255, 0), (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4)
        
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.selected_square = None
        self.board = Board()  # Инициализация игрового поля
        self.turn = Checker_1  # Игра начинается с темных шашек (Checker_1)
        self.valid_moves = {}

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()
        self.turn = Checker_1  # Сбрасываем на очередь темных шашек

    def is_over(self):
        return self.winner() is not None

    def select(self, row, col):
        piece = self.board.get_piece(row, col)

        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.selected_square = None
                self.select(row, col)
        
        if piece != 0 and piece.color == self.turn:  # Проверяем, чей сейчас ход
            all_moves = {piece: self.board.get_valid_moves(piece) for row in self.board.board for piece in row if piece != 0 and piece.color == self.turn}
            can_capture = any(any(len(skipped) > 0 for skipped in moves.values()) for moves in all_moves.values())

            if can_capture:
                moves = self.board.get_valid_moves(piece)
                if any(len(skipped) > 0 for skipped in moves.values()):
                    self.selected = piece
                    self.selected_square = (row, col)
                    self.valid_moves = moves
                    return True
            elif any(all_moves.values()):
                self.selected = piece
                self.selected_square = (row, col)
                self.valid_moves = self.board.get_valid_moves(piece)
                return True
        elif piece == 0:
            self.valid_moves = {}
            self.selected = piece
            self.selected_square = (row, col)
            
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            self.selected_square = (row, col)
            skipped = self.valid_moves.get((row, col))
            self.valid_moves = {}
            if skipped:
                self.board.remove(skipped)
                self.valid_moves = self.board.get_valid_moves(self.selected)
                if any(self.valid_moves.values()):
                    return True
            self.switch_turn()  # Переключаем очередь хода
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def switch_turn(self):
        self.valid_moves = {}
        self.turn = Checker_2 if self.turn == Checker_1 else Checker_1  # Переключение между темными и светлыми

    def play_turn(self, action, color):
        row, col, target_row, target_col = action
        if color != self.turn:  # Проверяем, чей ход
            return -1
        
        if not self.select(row, col):
            return -1
        
        if not self._move(target_row, target_col):
            return -1

        reward = 1
        skipped_pieces = self.valid_moves.get((target_row, target_col))
        if skipped_pieces:
            reward += len(skipped_pieces)

        if self.is_over():
            reward = 2 if self.winner() == color else -5
        return reward

    def get_available_moves(self, color):
        moves = []
        for row in range(len(self.board.board)):
            for col in range(len(self.board.board[row])):
                piece = self.board.get_piece(row, col)
                if piece is not None and hasattr(piece, 'color') and piece.color == color:  # Проверка на наличие атрибута color
                    valid_moves = self.board.get_valid_moves(piece)
                    for move, skipped in valid_moves.items():
                        moves.append((row, col, move[0], move[1]))
        return moves

    def get_winner(self):
        return self.board.winner()
