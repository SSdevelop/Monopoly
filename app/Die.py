from random import choice


class Die:
    """
    This class represents a single die
    that can be rolled
    """
    die_pool = [1, 2, 3, 4]

    def __init__(self, value: int = None):
        self.value = value

    def roll(self):
        """
        Roll this die and update the
        current die value
        """

        # select one number from possible numbers
        self.value = choice(self.die_pool)

