import pygame
from .constants import Bucket_1, ROWS, Checker_1, SQUARE_SIZE, COLS, Checker_2, Bucket_2
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.Checker_1_left = self.Checker_2_left = 12
        self.Checker_1_kings = self.Checker_2_kings = 0
        self.create_board()

    def draw_squares(self, win):
        win.fill(Bucket_1)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, Bucket_2, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        # Превращаем шашку в дамку только при достижении противоположного ряда
        if piece.color == Checker_1 and row == 0:
            piece.make_king()
            self.Checker_1_kings += 1
        elif piece.color == Checker_2 and row == ROWS - 1:
            piece.make_king()
            self.Checker_2_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, Checker_2))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, Checker_1))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == Checker_1:
                    self.Checker_1_left -= 1
                else:
                    self.Checker_2_left -= 1

    def winner(self):
        if self.Checker_1_left <= 0:
            return Checker_2
        elif self.Checker_2_left <= 0:
            return Checker_1
        return None 

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row
        can_capture = False

        if piece.king:
            # Дамки могут ходить и захватывать во всех направлениях
            moves.update(self._king_moves(piece, row, piece.col))

        if piece.color == Checker_1:
            # Простая шашка Checker_1 может ходить только вверх
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
            # Проверка захвата назад
            moves.update(self._traverse_backward_left(row + 1, min(row + 3, ROWS), 1, piece.color, left, check_for_capture=True))
            moves.update(self._traverse_backward_right(row + 1, min(row + 3, ROWS), 1, piece.color, right, check_for_capture=True))
            if any(moves.values()):
                can_capture = True

        elif piece.color == Checker_2:
            # Простая шашка Checker_2 может ходить только вниз
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))
            # Проверка захвата назад
            moves.update(self._traverse_backward_left(row - 1, max(row - 3, -1), -1, piece.color, left, check_for_capture=True))
            moves.update(self._traverse_backward_right(row - 1, max(row - 3, -1), -1, piece.color, right, check_for_capture=True))
            if any(moves.values()):
                can_capture = True

        # Если можно захватить, оставляем только ходы с захватом
        if can_capture:
            moves = {key: value for key, value in moves.items() if value}

        return moves

    def _king_moves(self, piece, row, col):
        moves = {}
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Все четыре диагональные направления

        for direction in directions:
            moves.update(self._traverse_king(row, col, direction[0], direction[1], piece.color))

        return moves

    def _traverse_king(self, start_row, start_col, row_step, col_step, color):
        moves = {}
        last = None
        r, c = start_row + row_step, start_col + col_step
        
        while 0 <= r < ROWS and 0 <= c < COLS:
            current = self.board[r][c]
            
            if current == 0:  # Пустая клетка
                if last:  # Если шашка уже была найдена
                    # Дамка может встать на любую клетку за съеденной шашкой
                    moves[(r, c)] = [last]
                else:
                    moves[(r, c)] = []
            elif isinstance(current, Piece):
                if current.color != color:
                    if last:  # Если уже была одна шашка
                        break  # Нельзя перепрыгнуть через две шашки подряд
                    else:
                        last = current  # Запоминаем шашку, которую можно съесть
                else:
                    break  # Если это своя шашка, останавливаемся
                
            r += row_step
            c += col_step

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]

            if current == 0:
                # Добавляем возможность простого хода
                if not skipped:
                    moves[(r, left)] = last
                else:
                    if last:
                        moves[(r, left)] = skipped + last
                break

            elif isinstance(current, Piece):
                if current.color == color:
                    break
                else:
                    last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]

            if current == 0:
                # Добавляем возможность простого хода
                if not skipped:
                    moves[(r, right)] = last
                else:
                    if last:
                        moves[(r, right)] = skipped + last
                break

            elif isinstance(current, Piece):
                if current.color == color:
                    break
                else:
                    last = [current]

            right += 1

        return moves

    def _traverse_backward_left(self, start, stop, step, color, left, skipped=[], check_for_capture=False):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]

            if current == 0:
                # Если мы проверяем возможность хода, но не захвата, выходим
                if not skipped and not check_for_capture:
                    break
                # Если есть шашка для захвата
                if last:
                    moves[(r, left)] = skipped + last
                break

            elif isinstance(current, Piece):
                if current.color == color:
                    break
                else:
                    last = [current]

            left -= 1

        return moves

    def _traverse_backward_right(self, start, stop, step, color, right, skipped=[], check_for_capture=False):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]

            if current == 0:
                # Если мы проверяем возможность хода, но не захвата, выходим
                if not skipped and not check_for_capture:
                    break
                # Если есть шашка для захвата
                if last:
                    moves[(r, right)] = skipped + last
                break

            elif isinstance(current, Piece):
                if current.color == color:
                    break
                else:
                    last = [current]

            right += 1

        return moves