from random import choice

from app.Config import Config


class Player:
    """
    Represents a player of the game.
    """

    def __init__(self, game, token: str = 'Player 1', player_id: int = 0, player_dict=None):
        from app.Game import Game

        self.game: Game = game

        if player_dict is not None:
            self.__init_from_dict(player_dict)
        else:
            self.token = token
            self.player_id = player_id
            self.balance: int = Config.SALARY
            self.is_jailed: bool = False
            self.square_position: int = 1
            self.move_count_since_jail = 0
            self.has_exited = False
            # the two modes used to get out of jail.
            self.jail_bail_mode = False
            self.jail_feeling_lucky_mode = False

    def __init_from_dict(self, player_dict):
        from app.Square import PropertySquare

        # load player from dict
        self.token = player_dict['token']
        self.player_id = player_dict['player_id']
        self.balance: int = player_dict['balance']
        self.is_jailed: bool = player_dict['is_jailed']
        self.square_position = player_dict['square_position']
        self.move_count_since_jail = player_dict['move_count_since_jail']
        self.has_exited = player_dict['has_exited']
        # the two modes used to get out of jail.
        self.jail_bail_mode = player_dict['jail_bail_mode']
        self.jail_feeling_lucky_mode = player_dict['jail_feeling_lucky_mode']
        # assign any properties they players had previously
        for property_position in player_dict['properties']:
            property_: PropertySquare = self.game.board.get_square(property_position)
            property_.owner_token = self.token

    # methods
    def collect_salary(self):
        """
        Ask the player to collect a salary.
        """
        self.balance += Config.SALARY

    def pay_tax(self) -> int:
        """
        Ask the player to pay tax.
        :returns: int The tax that the user paid.
        """

        # get 10 percent of balance
        raw_tax = 0.1 * self.balance

        # round down to a multiple of 10
        tax = int(raw_tax - (raw_tax % 10))

        # update balance
        self.balance = self.balance - tax

        # return the tax deducted
        return tax

    def go_to_jail(self):
        """
        Ask the player to go to jail.
        """
        self.is_jailed = True
        self.move_count_since_jail = 0
        self.square_position = Config.JAIL_SQUARE_POSITION
        self.jail_feeling_lucky_mode = False
        self.jail_bail_mode = False

    def lose_to_chance(self) -> int:
        """
        Lose some money to chance
        :return: The lost money
        """

        # create amounts all the way to VND 300
        amounts = [i * 10 for i in range(1, 31)]

        # get the random amount
        amount = choice(amounts)

        # update the current balance
        self.balance = self.balance - amount

        return amount

    def gain_from_chance(self) -> int:
        """
        Gain some money from chance
        :return: The gained money
        """

        # create amounts all the way to VND 300
        amounts = [i * 10 for i in range(1, 21)]

        # get the random amount
        amount = choice(amounts)

        # update the current balance
        self.balance = self.balance + amount

        return amount

    def pay_rent(self, rent: int, owner_token: str, property_name: str):
        """
        Ask player to pay rent.
        """

        # pay the rent.
        self.balance -= rent
        print(f'{self.token} has paid {Config.CURRENCY} {rent} in rent for property: {property_name}!')

        # ask the owner to collect the rent.
        other_player = self.game.get_player(owner_token)
        other_player.collect_rent(rent=rent, property_name=property_name)

    def buy_property(self, property_square):
        """
        Ask the user to buy the property.
        :param property_square: The property square.
        """

        # ensure the property square is available.
        if property_square.owner_token is not None:
            return

        # buy the property
        self.balance -= property_square.price
        property_square.owner_token = self.token
        print(f'{self.token} bought {property_square.to_string()} successfully!')
        self.declare_balance()

    def collect_rent(self, rent: int, property_name: str):
        """
        Ask player to collect rent.
        :param property_name: The property from which we collect rent.
        :param rent: The rent to be collected.
        """
        self.balance += rent
        print(f'{self.token} has collected {Config.CURRENCY} {rent} in rent for property: {property_name}!')

    def declare_balance(self):
        """
        Declare the balance.
        """
        print(f'{self.token}: My balance is now: {Config.CURRENCY} {self.balance}')

    def is_bankrupt(self) -> bool:
        """
        :return: whether the player is bankrupt
        """
        return self.balance < 0

    def get_properties(self):
        from app.Square import PropertySquare
        # store the properties here.
        properties = []

        # filter the property squares that belong to this
        # user.
        for square in self.game.board.squares:
            if not isinstance(square, PropertySquare):
                continue
            if square.owner_token == self.token:
                properties.append(square)
        return properties

    def exit_game(self):
        """
        Exit the game.
        """
        # import the property square to avoid a circular import
        from app.Square import PropertySquare

        # mark the user as exited.
        self.has_exited = True
        print(f'{self.token} has exited the game due to bankruptcy. Balance is: {self.balance}')
        # disown all the properties that belong to this player.
        for prop in self.get_properties():
            print(f'{self.token} is disowning {prop.to_string()}')
            prop.owner_token = None

    def __play_jail_feeling_lucky_mode(self):
        """
        The user wants to throw at least one double in one of the next 3 turns.
        """

        # roll the dice first
        self.__roll_dice()

        # get the dice_pair
        die_pair = self.game.die_pair

        # increase the move count since jail
        self.move_count_since_jail += 1

        # get the dice total
        dice_total = die_pair.get_total_value()

        # the user rolled a double!
        if die_pair.is_double():
            # take the user out of jail. Move them out of jail, land them to them
            # on the appropriate square.
            print(f'{self.token} rolled a double! Getting out of jail.')
            self.is_jailed = False
            self.move_and_land_on_square(dice_total)
            return

        if self.move_count_since_jail < 3:
            # no double detected so far, ask the user to try their luck
            # the next time.
            print(f'{self.token} did not roll a double. Cannot get out of jail. Try next time.')
            return

        if self.move_count_since_jail == 3:
            # the user has rolled three times, no double was detected.
            # they need to pay 150 VND and move forward the
            # number of spaces shown by throw.
            print(f'{self.token} did not roll a double by the third turn.')
            self.pay_fine()
            self.is_jailed = False
            self.move_and_land_on_square(dice_total)

    def pay_fine(self):
        self.balance -= Config.JAIL_FINE
        print(f'{self.token} has paid a fine of {Config.CURRENCY} {Config.JAIL_FINE}.')
        self.declare_balance()

    def __play_jail_bail_mode_mode(self):
        """
        The user wishes to pay VND 150 in either of their next 2 turns.
        """

        if self.move_count_since_jail == 0:
            # this is the first move since being jailed.
            # ask the user to pay a fine.
            print(f'\n{self.token}, do you want to pay {Config.CURRENCY} {Config.JAIL_FINE} now?')
            print('[1] Yes  [2] No')
            answer = Config.DEFAULT_BAIL_MODE_PAY_NOW
            if not Config.IS_TEST_ENVIRONMENT:
                answer = input('Enter your choice (1/2) :>').strip()

            # ensure the user provided valid input
            if answer not in ['1', '2']:
                print('Invalid choice. Defaulting to: [1] Yes')
                answer = '1'

            if answer == '1':
                self.pay_fine()
                self.is_jailed = False
            else:
                print('Okay, you will pay in your next turn.')
        else:
            self.pay_fine()
            self.is_jailed = False

        # first roll the dice
        self.__roll_dice()

        # increment the number of moves since jailed
        self.move_count_since_jail += 1
        dice_total = self.game.die_pair.get_total_value()
        self.move_and_land_on_square(dice_total)

    def __roll_dice(self):
        # throw roll dice first
        # grab the dice
        die_pair = self.game.die_pair

        # roll the dice
        print(f'{self.token}: Rolling dice ...')
        die_pair.roll_pair()
        print(f'{self.token}: Dice results => {die_pair.get_results()}')

    def move_and_land_on_square(self, dice_total: int):
        for i in range(1, dice_total):
            # get the next position
            next_position = (self.square_position + i) % Config.MAX_SQUARE_COUNT
            if next_position == 0:
                next_position = Config.MAX_SQUARE_COUNT

            # get the square at that position
            square = self.game.board.get_square(position=next_position)

            # pass through the square
            square.pass_through(self)

        # land on the last square
        last_square_position = (self.square_position + dice_total) % Config.MAX_SQUARE_COUNT
        if last_square_position == 0:
            last_square_position = Config.MAX_SQUARE_COUNT
        self.square_position = last_square_position
        square = self.game.board.get_square(last_square_position)
        square.land_on(self)

    def __play_no_jail_mode(self):
        self.__roll_dice()

        # move through the squares
        dice_total = self.game.die_pair.get_total_value()
        self.move_and_land_on_square(dice_total=dice_total)

    def select_jail_strategy(self):
        """
        Define how the user will get out of jail.
        """
        print(f'\n{self.token}, how do you want to get out of jail? (Enter 1 or 2)')
        print(
            f'[1] Play at least a double for the next 3 turns.\n'
            f'    Pay {Config.CURRENCY} {Config.JAIL_FINE} if you fail by your third turn.'
        )
        print(f'[2] Pay {Config.CURRENCY} {Config.JAIL_FINE} in either of the next 2 turns.')

        user_response = Config.DEFAULT_JAIL_STRATEGY

        if not Config.IS_TEST_ENVIRONMENT:
            user_response = input('Enter your choice (1/2):> ').strip()

        if user_response not in ['1', '2']:
            print('Invalid selection. Defaulting to 2')
            user_response = '2'
        if user_response == '1':
            self.jail_feeling_lucky_mode = True
            self.jail_bail_mode = False
        else:
            self.jail_feeling_lucky_mode = False
            self.jail_bail_mode = True

    def play(self):
        # the user is not jailed,
        # so just play the usual way.
        if not self.is_jailed:
            self.__play_no_jail_mode()
            return

        # the user is jailed.
        if not (self.jail_feeling_lucky_mode or self.jail_bail_mode):
            # ask the user to select how they want to get out of jail.
            self.select_jail_strategy()

        if self.jail_feeling_lucky_mode:
            # play with the feeling lucky mode
            self.__play_jail_feeling_lucky_mode()
        else:
            # play with the bail mode
            self.__play_jail_bail_mode_mode()

    def to_dict(self):
        """
        Serialize the player to a dictionary
        """
        return {
            'token': self.token,
            'balance': self.balance,
            'is_jailed': self.is_jailed,
            'square_position': self.square_position,
            'has_exited': self.has_exited,
            'player_id': self.player_id,
            'move_count_since_jail': self.move_count_since_jail,
            'jail_bail_mode': self.jail_bail_mode,
            'jail_feeling_lucky_mode': self.jail_feeling_lucky_mode,
            'properties': [p.position for p in self.get_properties()]
        }