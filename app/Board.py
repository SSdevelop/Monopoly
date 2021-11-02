from typing import Optional

from app.Square import Square, GoSquare, PropertySquare, IncomeTaxSquare, InJailOrVisitingSquare, \
    FreeParkingSquare, GoToJailSquare, ChanceSquare


class Board:
    """
    The monopoly board.
    """

    def __init__(self):
        self.squares = [
            GoSquare(name='Go', position=1),
            PropertySquare(name='Central', position=2, price=800, rent=90),
            PropertySquare(name='Wan Chai', position=3, price=700, rent=65),
            IncomeTaxSquare(name='Income Tax', position=4),
            PropertySquare(name='Stanley', position=5, price=600, rent=60),
            InJailOrVisitingSquare(name='In Jail/Visiting', position=6),
            PropertySquare(name='Shek O', position=7, price=400, rent=10),
            PropertySquare(name='Mong Kok', position=8, price=500, rent=40),
            ChanceSquare(name='Red Chance', position=9),
            PropertySquare(name='Tsing Yi', position=10, price=400, rent=15),
            FreeParkingSquare(name='Free Parking', position=11),
            PropertySquare(name='Shatin', position=12, price=700, rent=75),
            ChanceSquare(name='Blue Chance', position=13),
            PropertySquare(name='Tuen Mun', position=14, price=400, rent=20),
            PropertySquare(name='Tai Po', position=15, price=500, rent=25),
            GoToJailSquare(name='Go To Jail', position=16),
            PropertySquare(name='Sai Kung', position=17, price=400, rent=10),
            PropertySquare(name='Yuen Long', position=18, price=400, rent=25),
            ChanceSquare(name='Yellow Chance', position=19),
            PropertySquare(name='Tai O', position=20, price=600, rent=25),
        ]

    def get_square(self, position: int) -> Optional[Square]:
        # check if the position is out of bounds
        if position <= 0 or position > len(self.squares):
            return None

        # calculate the index
        index = position - 1

        # return the target square
        return self.squares[index]
