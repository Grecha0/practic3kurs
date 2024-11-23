import pygame
from checkers.constants import WIDTH, HEIGHT, Checker_1, Checker_2
from checkers.game import Game
from checkers_bot import CheckersBot

def train_bot(difficulty='medium', render=False):
    pygame.init()
    win = None
    if render:  # Только если нужно отображать окно
        win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Checkers Bot Training')

    game = Game(win)
    bot1 = CheckersBot(color=Checker_1, difficulty=difficulty)  # Бот за коричневых
    bot2 = CheckersBot(color=Checker_2, difficulty=difficulty)  # Бот за белых
    current_bot = bot1  # Начинаем с бота за коричневых

    episodes = 100000
    bot1_wins = 0
    bot2_wins = 0

    for episode in range(episodes):
        game.reset()
        total_reward = 0

        while not game.is_over():
            if game.turn != current_bot.color:
                game.switch_turn()
                continue

            action = current_bot.choose_action(game)
            if action is None:
                break

            # Игровой ход и обновление Q-таблицы текущего бота
            reward = game.play_turn(action, current_bot.color)
            current_bot.update_q_table(game, reward)
            total_reward += reward

            # Переключение на другого бота после каждого хода
            current_bot = bot1 if current_bot == bot2 else bot2

            if render:  # Отрисовываем, только если задан флаг render
                game.update()

        # Определяем победителя
        winner = game.get_winner()
        if winner == Checker_1:
            bot1_wins += 1
        elif winner == Checker_2:
            bot2_wins += 1

        # Завершающее обновление Q-таблицы
        if current_bot.last_state and current_bot.last_action:
            current_bot.update_q_table(game, reward=0)  # Завершающее обновление с нулевой наградой

        # Логирование каждые 100 эпизодов
        if episode % 100 == 0:
            bot1.save_model(filename=f'{difficulty}_bot1_model.pkl')
            bot2.save_model(filename=f'{difficulty}_bot2_model.pkl')
            print(
                f"Episode {episode}: Total Reward: {total_reward}, "
                f"Bot1 Wins: {bot1_wins}, Bot2 Wins: {bot2_wins}"
            )

    # Окончательное сохранение моделей после всех эпизодов
    bot1.save_model(filename=f'{difficulty}_bot1_model.pkl')
    bot2.save_model(filename=f'{difficulty}_bot2_model.pkl')

    if render:
        pygame.quit()

if __name__ == "__main__":
    train_bot(difficulty='medium', render=False)
