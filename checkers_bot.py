import random
import pickle
import os  # Добавляем для проверки существования файла модели

class CheckersBot:
    def __init__(self, color, difficulty, model_path=None):
        self.color = color
        self.q_table = {}  # Инициализация пустой Q-таблицы по умолчанию
        self.model_path = model_path  # Устанавливаем путь к модели при инициализации

        # Устанавливаем параметры в зависимости от сложности
        if difficulty == 'easy':
            self.alpha = 0.05
            self.gamma = 0.9
            self.epsilon = 0.5
        elif difficulty == 'medium':
            self.alpha = 0.1
            self.gamma = 0.9
            self.epsilon = 0.2
        elif difficulty == 'hard':
            self.alpha = 0.1
            self.gamma = 0.95
            self.epsilon = 0.05

        self.last_state = None
        self.last_action = None

        # Загрузка модели, если указан путь к модели
        if self.model_path:
            self.load_model(self.model_path)

    def get_state(self, game):
        # Состояние игры представлено строкой доски
        return str(game.board)

    def choose_action(self, game):
        if game.turn != self.color:
            return None  # Если не наш ход, бот ничего не делает

        state = self.get_state(game)
        if state not in self.q_table:
            self.q_table[state] = {}

        available_actions = game.get_available_moves(self.color)
        if not available_actions:
            return None  # Нет доступных ходов

        # epsilon-жадный метод для выбора действия
        if random.uniform(0, 1) < self.epsilon:
            action = random.choice(available_actions)
        else:
            q_values = [self.q_table[state].get(action, 0) for action in available_actions]
            max_q_value = max(q_values)
            best_actions = [action for action, q in zip(available_actions, q_values) if q == max_q_value]
            action = random.choice(best_actions)

        self.last_state = state
        self.last_action = action

        return action
    
    def count_pieces(self, game):
        """
        Считаем шашки на поле
        """
        bot_pieces = 0
        opponent_pieces = 0

        for row in game.board.board:
            for piece in row:
                if piece != 0:
                    if piece.color == self.color:
                        bot_pieces += 1
                    else:
                        opponent_pieces += 1

        return bot_pieces, opponent_pieces


    def update_q_table(self, game, reward):
        state = self.get_state(game)

        bot_pieces_before, opponent_pieces_before = self.count_pieces(game)

        if self.last_state is not None and self.last_action is not None:
            available_actions = game.get_available_moves(self.color)
            if available_actions:
                next_q_values = [self.q_table[state].get(action, 0) for action in available_actions]
                max_next_q_value = max(next_q_values)

                # Проверяем изменения количества шашек
                bot_pieces_after, opponent_pieces_after = self.count_pieces(game)
                piece_difference = (opponent_pieces_before - opponent_pieces_after) - (bot_pieces_before - bot_pieces_after) 


                if piece_difference > 0:
                    reward += piece_difference
                elif piece_difference < 0:
                    reward += 2 * piece_difference  # -2 за каждую потерянную шашку

                # Проверка на смену хода
                if game.turn == self.color:
                    if not hasattr(self, 'no_switch_bonus') or self.no_switch_bonus is None:
                        self.no_switch_bonus = 1  # Инициализируем бонус, если он отсутствует или равен None
                    reward += self.no_switch_bonus
                    self.no_switch_bonus *= 2  # Увеличиваем бонус в геометрической прогрессии
                else:
                    if hasattr(self, 'no_switch_bonus') and self.no_switch_bonus:
                        reward += self.no_switch_bonus
                    self.no_switch_bonus = 0  # Обнуляем бонус



                # Обновляем Q-таблицу
                self.q_table[self.last_state][self.last_action] = (
                    (1 - self.alpha) * self.q_table[self.last_state].get(self.last_action, 0)
                    + self.alpha * (reward + self.gamma * max_next_q_value)
                )

        self.last_state = state
        self.last_action = None


    def save_model(self, filename=None):
        filename = filename or self.model_path or 'checkers_bot_model.pkl'
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load_model(self, model_path=None):
        model_path = model_path or self.model_path
        if model_path and os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                self.q_table = pickle.load(f)
            print(f"Модель успешно загружена из {model_path}")
        else:
            print(f"Модель не найдена по пути {model_path}, создается новая модель для {self.color}.")
            self.q_table = {}
