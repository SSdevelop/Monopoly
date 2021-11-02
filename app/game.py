from typing import List, Optional

from app.board import Board
from app.config import Config
from app.die_pair import DiePair
from app.player import Player
from json import dumps, loads
from pathlib import Path


class Game:
    """
    Defines the game.
    """

    def __init__(self, player_count: int=2, game_dict=None):
        self.board = Board()
        self.die_pair = DiePair()
        self.game_aborted = False

        # create the players.
        if game_dict is not None:
            self.current_round = game_dict['current_round']
            self.current_player_id = game_dict['current_player_id']
            self.players = [Player(game=self, player_dict=player_dict) for player_dict in game_dict['players']]
        else:
            self.players = self.create_players(player_count)
            self.current_player_id = 0
            self.current_round = 1


    def launch_game(self):
        # show the current turn
        print(f'\nCurrent Round: {self.current_round}\n')

        while not self.is_game_over():
            # get the current player from the board.
            player = self.get_player_by_id(self.current_player_id)

            # ensure the player is valid
            if player.has_exited:
                continue

            if not Config.IS_TEST_ENVIRONMENT:
                # prompt user to press enter to play their turn
                print(f'\n ---- Turn of: {player.token} -------')
                print(f'1. Play your turn')
                print(f'2. Save and exit game')
                choice = input('Enter your choice (1/2) :>').strip()
                if choice != '1':
                    if choice != '2':
                        print('Invalid choice. Will save and exit game.')

                    self.current_player_id = player.player_id
                    self.save_game()
                    self.game_aborted = True
                    break

            # ask the player to take their turn
            player.play()

            # check if the player is bankrupt
            if player.is_bankrupt():
                player.exit_game()

            # once the player is finished with their check if this was the last player
            if self.current_player_id == (len(self.players) - 1):

                # increase the round
                self.current_round += 1

                # set the next player as the first one
                self.current_player_id = 0

                if self.current_round <= 100:
                    # show the current round
                    print(f'\nCurrent Round: {self.current_round}\n')
            else:
                # move to the next player.
                self.current_player_id += 1

        if not self.game_aborted:
            self.announce_winners()

    def announce_winners(self):
        print('\n ------ GAME OVER --------')
        print('The winners of the game are:-')
        for winner in self.get_winners():
            print(f'{winner.token} with a balance of {Config.CURRENCY} {winner.balance}')

    def is_game_over(self) -> bool:
        # get the number of players remaining
        active_player_count = len(self.get_active_players())

        # return whether there is only one player or we have finished 100 rounds.
        return active_player_count == 1 or self.current_round > Config.MAX_ROUND_COUNT

    def create_players(self, player_count: int) -> List[Player]:
        """
        Create players from the player count.
        :param player_count: The number of players.
        :return:  The created players.
        """
        # ensure the player number is correct.
        if player_count < Config.MIN_PLAYER_COUNT or player_count > Config.MAX_PLAYER_COUNT:
            raise ValueError(f'Invalid number of players: {player_count}')

        players = [Player(token=f'Player {i}', player_id=i - 1, game=self) for i in range(1, player_count + 1)]
        return players

    def get_player_by_id(self, player_id) -> Optional[Player]:
        """
        Lookup a player using their id.
        :param player_id:  The player id.
        :return:  The player.
        """
        try:
            return self.players[player_id]
        except:
            return None

    def get_player(self, player_token: str) -> Optional[Player]:
        """
        Lookup a player using their token.
        :param player_token: The player token
        :return: The player or none if not found.
        """

        # filter players
        filtered_players = [player for player in self.players if player.token == player_token]
        if len(filtered_players) == 0:
            return None
        return filtered_players[0]

    def get_winners(self) -> List[Player]:
        """
        :return: The winners of the game.
        """
        # the highest balance
        highest_balance = 0

        # active players
        active_players = self.get_active_players()

        # determine the highest balance from the players.
        for player in active_players:
            if player.balance > highest_balance:
                highest_balance = player.balance

        # collect the winners with highest balance
        return [winner for winner in active_players if winner.balance == highest_balance]

    def get_active_players(self) -> List[Player]:
        """
        :return: The number of players who are yet to retire.
        """
        return [player for player in self.players if not player.has_exited]

    def to_dict(self):
        """
        Convert the game to a dictionary
        """
        return {
            'players': [player.to_dict() for player in self.players],
            'current_player_id': self.current_player_id,
            'current_round': self.current_round,
        }

    def get_file_name(self):
        """
        Get the file name to save a monopoly game.
        """
        path = Path('saved_games').joinpath('config.json')
        with path.open('r+') as f:
            config = loads(f.read())
            counter = config['counter']
            config['counter'] = counter + 1
            f.seek(0)
            f.write(dumps(config, indent=4))

            return f'monopoly_{counter}.json'

    def save_game(self):
        """
        Save the game to file.
        """
        file_name = self.get_file_name()
        path = Path('saved_games').joinpath(file_name)
        with path.open('w') as f:
            game_data = self.to_dict()
            f.write(dumps(game_data, indent=4))
            print(f'Game was saved as: {file_name}. Use this name to load it.')