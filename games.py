import random

class Game:
    var_name = ""
    pretty_name = ""

    def generate_question(self):
        raise NotImplementedError

    def __str__(self):
        return self.var_name

    @staticmethod
    def shuffle_nums(num1, num2, chance=.5):
        if random.random() < chance:
            num1, num2 = num2, num1
        return num1, num2

class ElevenMultiplication(Game):
    var_name = "mult_11"
    pretty_name = "11's Multiplication"

    def generate_question(self):
        num1 = 11
        num2 = random.randint(11, 99)
        num1, num2 = self.shuffle_nums(num1, num2)
        return f'{num1} x {num2}', num1 * num2


class AddToTen(Game):
    var_name = "add_to_10"
    pretty_name = "Add to 10"

    def generate_question(self):
        first_digit = random.randint(1, 9)
        second_digit = random.randint(1, 9)
        number1 = first_digit * 10 + second_digit
        number2 = first_digit * 10 + (10-second_digit)
        return f'{number1} * {number2}', number1 * number2


class SimpleMultiplication(Game):
    var_name = "simple_mult"
    pretty_name = "Simple Multiplication"

    def generate_question(self):
        # Chance to get a specific one
        if random.random() <.1:
            num1, num2 = random.choice([[6,7],[6,8],
                                        [7,12]
                                        [8,12],
                                        ])
            num1, num2 = self.shuffle_nums(num1, num2)

        num1 = random.randint(3, 12)
        num2 = random.randint(3, 12)
        return f'{num1} * {num2}', num1 * num2


class LargeAddition(Game):
    var_name = "large_addition"
    pretty_name = "Large Addition"

    def generate_question(self):
        num1 = random.randint(100, 999)
        num2 = random.randint(100, 999)
        return f'{num1} + {num2}', num1 + num2


class LargeSubtraction(Game):
    var_name = "large_subtraction"
    pretty_name = "Large Subtraction"

    def generate_question(self):
        num1 = random.randint(100, 999)
        num2 = random.randint(100, 999)
        return f'{num1} - {num2}', num1 - num2


class RandomGame(Game):
    var_name = "random_game"
    pretty_name = "Random Game"

    def __init__(self):
        self.games = {c.var_name: c() for c in Game.__subclasses__() if c != self.__class__}

    def generate_question(self):
        game = random.choice(list(self.games.values()))
        return game.generate_question()

# Initialize games
game_dict = {c.var_name: c() for c in Game.__subclasses__()}
