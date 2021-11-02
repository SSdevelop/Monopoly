from abc import ABC, abstractmethod
from random import choice

from app.config import Config
from app.player import Player


class Square(ABC):
    """
    Represents an abstract square on the board.
    """

    def __init__(self, position: int, name: str):
        self.position = position
        self.name = name

    # methods
    @abstractmethod
    def land_on(self, player: Player):
        """
        Define what happens when a player lands on this square.
        :param player:  The player that lands on the square.
        """
        print(f'{player.token} has landed on: {self.to_string()}')

    def pass_through(self, player: Player):
        """
        Defines what happens when a player passes through this square.
        By default, do nothing.
        :param player: The player.
        """
        pass

    def to_string(self):
        return f'Square {self.position} ({self.name})'


# Define the various types of squares

# ---------------------------------------------------------
class GoSquare(Square):

    def land_on(self, player: Player):
        super(GoSquare, self).land_on(player)
        player.collect_salary()
        print(f'{player.token} has collected a salary!')
        # ask the player to declare balance
        player.declare_balance()

    def pass_through(self, player: Player):
        player.collect_salary()
        print(f'{player.token} has passed through {self.to_string()}')
        print(f'{player.token} has collected a salary!')
        # ask the player to declare balance
        player.declare_balance()


# ---------------------------------------------------------

class PropertySquare(Square):
    def __init__(self, price: int, rent: int, position: int, name: str, owner_token: str = None):
        super().__init__(position, name)
        self.owner_token = owner_token
        self.rent = rent
        self.price = price

        # whether the user should be prompted to buy
        self.should_prompt_buy = True
        self.automated_buy_prompt = '2'

    def land_on(self, player: Player):
        super(PropertySquare, self).land_on(player)

        # do nothing if the player owns the property.
        if player.token == self.owner_token:
            return

        # ask if the property is interested in
        # owning this property
        if self.owner_token is None:
            print(f'{player.token}, do you wish to buy this property for {Config.CURRENCY} {self.price}?')
            print(f'Your current balance is: {player.balance} '
                  f'and you will be able to collect {Config.CURRENCY} {self.rent} in rent.')
            print('[1] Yes         [2] No')

            if Config.IS_TEST_ENVIRONMENT:
                answer = Config.DEFAULT_BUY_PROPERTY_CHOICE
            else:
                answer = input('Enter your choice (1/2):>').strip()

            if answer not in ['1', '2']:
                print('Invalid answer. Defaulting to [2] No.')
                answer = '2'

            # the user wishes to purchase a property.
            if answer == '1':
                player.buy_property(self)
            else:
                print('Okay. Not buying now.')

            return

        # pay rent if the player does not own
        # the property and the property is
        # is owned by someone else.
        player.pay_rent(rent=self.rent, owner_token=self.owner_token, property_name=self.name)

        # ask the player to declare balance
        player.declare_balance()


# ---------------------------------------------------------

class IncomeTaxSquare(Square):

    def land_on(self, player: Player):
        super(IncomeTaxSquare, self).land_on(player)
        tax = player.pay_tax()
        print(f'{player.token} has paid a tax of {Config.CURRENCY} {tax}!')
        # ask the player to declare balance
        player.declare_balance()


# ---------------------------------------------------------

class InJailOrVisitingSquare(Square):

    def land_on(self, player: Player):
        super(InJailOrVisitingSquare, self).land_on(player)


# ---------------------------------------------------------

class ChanceSquare(Square):

    def land_on(self, player: Player):
        super(ChanceSquare, self).land_on(player)

        # straws from which to pull the
        # user's luck
        straws = (True, False)

        # whether the user is lucky
        is_lucky = choice(straws)
        if is_lucky:
            amount = player.gain_from_chance()
            print(f'{player.token} gained {Config.CURRENCY} {amount}!')
            # ask the player to declare balance
            player.declare_balance()
        else:
            amount = player.lose_to_chance()
            print(f'{player.token} lost {Config.CURRENCY} {amount}!')
            # ask the player to declare balance
            player.declare_balance()


# ---------------------------------------------------------

class FreeParkingSquare(Square):

    def land_on(self, player: Player):
        super(FreeParkingSquare, self).land_on(player)


# ---------------------------------------------------------

class GoToJailSquare(Square):

    def land_on(self, player: Player):
        super(GoToJailSquare, self).land_on(player)
        player.go_to_jail()
        print(f'{player.token} has been jailed!')
