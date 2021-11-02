"""
Test cases for the Die.py module
"""
from app.Config import Config
from app.Die import Die


def test_roll():
    """
    Test Die.roll() method.
    This checks that the Die class.
    It also checks that irrespective of the number of throws,
    the die class will always return a number between 1 and 4 (inclusive).
    """
    die = Die()
    for i in range(100):
        die.roll()
        assert die.value in [1, 2, 3, 4]
