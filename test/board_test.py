"""
Tests for the board class.
"""
from app.Board import Board


def test_get_square():
    """
    Tests the board class by checking whether the correct squares are assigned or not.
    If correct squares are assigned, it means that the board is created correctly.
    """
    board = Board()
    s1 = board.get_square(4)
    s2 = board.get_square(13)
    s3 = board.get_square(20)
    s4 = board.get_square(-1)

    assert s1.name == 'Income Tax'
    assert s2.name == 'Blue Chance'
    assert s3.name == 'Tai O'
    assert s4 is None
