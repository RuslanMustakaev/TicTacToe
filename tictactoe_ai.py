"""TicTacToe that you can play against computer.
The computer have three levels of difficulty — easy, medium, and hard.
To start game enter command:>
start  [first player mode] [second player mode]
For player mode you can enter 'user', 'easy', 'medium', 'hard'
For example to start game with hard computer level enter:
'start user hard'
For quit game enter command 'exit'"""


import random
import minimax

SIZE_OF_BOARD = 3
EMPTY_SELL = '_'
HUMAN = 'user'
OPTIONS = ('easy', 'medium', 'hard',  HUMAN)


class Player:

    def __new__(cls, level, *args):
        if level == 'easy':
            return object.__new__(ComputerPlayerEasy)
        elif level == 'medium':
            return object.__new__(ComputerPlayerMedium)
        elif level == 'hard':
            return object.__new__(ComputerPlayerHard)
        elif level == HUMAN:
            return object.__new__(Human)

    def __init__(self, level, current_game):
        self.level = level
        self.game = current_game


class Human(Player):

    def __repr__(self):
        return 'Human'

    def new_turn(self):

        current_game = self.game

        while True:
            coord = input('Enter the coordinates:').split()
            if not is_numbers(coord):
                print('You should enter numbers!')
                continue

            x, y = [int(i) for i in coord]

            if not is_from_1_to_3(x, y):
                print('Coordinates should be from 1 to 3!')
                continue
            elif not current_game.status.empty_cell(x, y):
                print('This cell is occupied! Choose another one!')
                continue

            return x, y


class ComputerPlayer(Player):

    def __init__(self, level, current_game):

        super().__init__(level, current_game)
        # self.name = level + ' ' + str(self.number_of_player)
        self.name = level

    def __repr__(self):
        return self.name

    def __str__(self):
        return f'Making move level "{self.level}"'

    @staticmethod
    def random_move() -> (int, int):
        while True:
            x = random.randint(1, 3)
            y = random.randint(1, 3)
            if game.status.empty_cell(x, y):
                return x, y


class ComputerPlayerEasy(ComputerPlayer):
    number_of_player = 0

    def __new__(cls, **kwargs):
        cls.number_of_player += 1

    def new_turn(self) -> (int, int):
        print(self)
        x, y = self.random_move()
        return x, y


class ComputerPlayerMedium(ComputerPlayer):

    def new_turn(self) -> (int, int):

        print(self)

        current_game = self.game

        for x in range(1, SIZE_OF_BOARD + 1):
            for y in range(1, SIZE_OF_BOARD + 1):
                if current_game.check_possible_win_for_player(x, y):
                    return x, y

        for x in range(1, SIZE_OF_BOARD + 1):
            for y in range(1, SIZE_OF_BOARD + 1):
                if current_game.check_possible_win_for_opponent(x, y):
                    return x, y
        else:
            return self.random_move()


class ComputerPlayerHard(ComputerPlayer):

    def new_turn(self) -> (int, int):

        print(self)

        current_game = self.game
        if current_game.status.count_empty_cells() == 9:
            return self.random_move()
        else:
            # print(current_game.status.state)
            # print(current_game.player_turn)
            return minimax.find_best_move(current_game.status.state, current_game.player_turn)


class GameState:

    def __init__(self, game):
        self.state = self.start()
        self.game = game

    @staticmethod
    def start():
        return [[EMPTY_SELL] * SIZE_OF_BOARD for _ in range(SIZE_OF_BOARD)]

    def show(self):

        stage = ''

        border = "-" * (SIZE_OF_BOARD ** 2)
        stage += border + '\n'

        for x in range(SIZE_OF_BOARD):
            row = '| '
            for y in range(SIZE_OF_BOARD):
                if self.state[x][y] == EMPTY_SELL:
                    row += " "
                else:
                    row += self.state[x][y]
                row = row + ' '
            row = row + '|'
            stage += row + '\n'

        stage += border + '\n'
        return stage

    def empty_cell(self, x: int, y: int) -> bool:
        return self.state[x - 1][y - 1] == EMPTY_SELL

    def count_empty_cells(self) -> int:
        return sum([self.state[i].count(EMPTY_SELL) for i in range(SIZE_OF_BOARD)])

    def check_win(self) -> bool:
        return self.check_state(self.state, self.game.player_turn)

    def check_possible_win(self, move: str, x: int, y: int) -> bool:

        if not self.empty_cell(x, y):
            return False
        possible_state = [[self.state[i][j] for j in range(SIZE_OF_BOARD)] for i in range(SIZE_OF_BOARD)]
        possible_state[x - 1][y - 1] = move
        return self.check_state(possible_state, move)

    @staticmethod
    def check_state(state, move) -> bool:

        # check rows for XXX or OOO
        if any([move * SIZE_OF_BOARD in "".join(row) for row in state]):
            return True

        # check columns for XXX or OOO
        if any([all([state[i][j] == move for i in range(SIZE_OF_BOARD)])
                for j in range(SIZE_OF_BOARD)]):
            return True

        # check diagonal for XXX or OOO
        if all([state[i][i] == move for i in range(SIZE_OF_BOARD)]):
            return True
        if all([state[SIZE_OF_BOARD - 1 - i][i] == move for i in range(SIZE_OF_BOARD)]):
            return True

        return False


class GameTicTacToe:
    PLAYERS = {'X': None, 'O': None}

    def __new__(cls, answer):

        if len(answer) != 3 or answer[1] not in OPTIONS or answer[2] not in OPTIONS:
            print('Bad parameters!')
        else:
            return object.__new__(cls)

    def __init__(self, answer):

        self.PLAYERS['X'] = Player(answer[1], self)
        self.PLAYERS['O'] = Player(answer[2], self)

        self.player_turn = list(self.PLAYERS.keys())[0]
        self.player = self.PLAYERS['X']

        self.status = GameState(self)

    def __repr__(self):
        return self.status.show()

    def start_game(self):

        print(self)

        while True:
            self.new_turn()
            result = self.check_results_of_round()
            if result is not None:
                print(result)
                break
            self.choose_player()

    def check_results_of_round(self):

        result = None

        if self.status.check_win():
            result = self.player_turn + ' wins'
        elif self.status.count_empty_cells() == 0:
            result = 'Draw'

        return result

    def choose_player(self):

        self.player_turn = self.change_player()
        self.player = self.PLAYERS[self.player_turn]

    def change_player(self, player_turn=None):

        if player_turn is None:
            player_turn = self.player_turn

        moves = list(self.PLAYERS.keys())
        return moves[1] if player_turn is None or player_turn == moves[0] else moves[0]

    def new_turn(self):

        x, y = self.player.new_turn()

        self.status.state[x - 1][y - 1] = self.player_turn
        print(self)

    def check_possible_win_for_player(self, x, y):

        return self.status.check_possible_win(self.player_turn, x, y)

    def check_possible_win_for_opponent(self, x, y):

        move = self.change_player()
        return self.status.check_possible_win(move, x, y)


def is_numbers(symbols: list) -> bool:
    if len(symbols) != 2:
        return False
    else:
        for s in symbols:
            if not s.isdigit():
                return False
        else:
            return True


def is_from_1_to_3(x: int, y: int) -> bool:
    numbers = [i for i in range(1, SIZE_OF_BOARD + 1)]
    return x in numbers and y in numbers


if __name__ == '__main__':

    while True:
        menu_answer = input('Input command: ').split()

        if menu_answer[0] == 'start':
            game = GameTicTacToe(menu_answer)
            if game is not None:
                game.start_game()

        elif menu_answer[0] == 'exit':
            break
        else:
            print('Bad parameters!')
