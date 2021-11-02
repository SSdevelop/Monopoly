"""
Tests for the board class.
"""
from app.board import Board


def test_get_square():
    board = Board()
    s1 = board.get_square(4)
    s2 = board.get_square(13)
    s3 = board.get_square(20)

    assert s1.name == 'Income Tax'
    assert s2.name == 'Blue Chance'
    assert s3.name == 'Tai O'
