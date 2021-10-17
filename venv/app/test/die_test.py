"""
Test cases for the die.py module
"""
from app.config import Config
from app.die import Die


def test_roll():
    Config.IS_TEST_ENVIRONMENT = False

    """
    Test Die.roll() method
    """
    die = Die()
    for i in range(100):
        die.roll()
        assert die.value in [1, 2, 3, 4]

    Config.IS_TEST_ENVIRONMENT = True
