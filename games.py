import random

class Game:
    var_name = ""
    pretty_name = ""

    def generate_question(self):
        raise NotImplementedError

    def __str__(self):
        return self.var_name

class ElevenMultiplication(Game):
    var_name = "mult_11"
    pretty_name = "11's Multiplication"

    def generate_question(self):
        multiplier = random.randint(0, 100)
        return f'11 x {multiplier}', 11 * multiplier


class AddToTen(Game):
    var_name = "add_to_10"
    pretty_name = "Add to 10"

    def generate_question(self):
        first_digit = random.randint(1, 9)
        second_digit = 10 - first_digit
        number1 = first_digit * 10 + random.randint(0, 9)
        number2 = second_digit * 10 + random.randint(0, 9)
        return f'{number1} + {number2}', number1 + number2


# Initialize games
game_dict = {c.var_name: c() for c in Game.__subclasses__()}
