from .Config import Config
from .Die import Die


class DiePair:
    """
    This class represents a pair of dice.
    """

    def __init__(self):
        # define the two dice
        self.die1 = Die()
        self.die2 = Die()

        if Config.IS_TEST_ENVIRONMENT:
            self.die1.die_pool = [Config.DIE_1_VALUE]
            self.die2.die_pool = [Config.DIE_2_VALUE]

    def roll_pair(self):
        """
        Roll the pair of dice.
        """

        self.die1.roll()
        self.die2.roll()

    def get_total_value(self) -> int:
        """
        :return:int The total value of the two dice.
        """
        return self.die1.value + self.die2.value

    def is_double(self) -> bool:
        """
        :return:bool Whether the current roll constitutes a pair.
        """
        return self.die1.value == self.die2.value

    def get_results(self):
        """
        Show the results of the current throw.
        """
        return f'Die 1: {self.die1.value}, Die 2: {self.die2.value}'
