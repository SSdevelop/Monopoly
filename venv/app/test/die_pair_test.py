"""
Test the die_pair.DiePair.py class.
"""
from app.die import Die
from app.die_pair import DiePair


def test_get_total_value():
    """
    Test the total outcome when we roll a pair
    """

    # ensure that 1 is the result every time
    # we roll die1
    die1 = Die()
    die1.die_pool = [1]

    # ensure that 4 is the result every time
    # we roll die2
    die2 = Die()
    die2.die_pool = [2]

    # create the die pair, roll the pair
    die_pair = DiePair()
    die_pair.die1 = die1
    die_pair.die2 = die2
    die_pair.roll_pair()

    # check the die results
    assert 3 == die_pair.get_total_value()


def test_is_double():
    """
    Test whether the we can detect when a user has rolled a double.
    """

    # ensure that 2 is the result every time
    # we roll die1
    die1 = Die()
    die1.die_pool = [2]

    # ensure that 2 is the result every time
    # we roll die2
    die2 = Die()
    die2.die_pool = [2]

    # create the die pair, roll the pair
    die_pair = DiePair()
    die_pair.die1 = die1
    die_pair.die2 = die2
    die_pair.roll_pair()

    # check the die results
    assert die_pair.is_double()
