# launch the game here.
from app.Game import Game
from app.Config import Config
from pathlib import Path
from json import loads

if __name__ == '__main__':
    # the game is being played (not executed by tests)
    Config.IS_TEST_ENVIRONMENT = False

    print('----------- Welcome to MONOPOLY -------------')
    print('1. Load Game  From file')
    print('2. Start A New Game')
    choice = input('Enter your selection :>')
    if choice == '1':
        file_name = input('Enter the file name (e.g monopoly_1.json) :>').strip()
        path = Path('saved_games').joinpath(file_name)
        if not path.exists():
            print(f'Error: File {file_name} was not found in the folder \'saved games\'. Try again.')

        try:
            with path.open('r') as f:
                game_dict = loads(f.read())
            # create the game
            game = Game(game_dict=game_dict)
            print('\nThe game was loaded successfully!\n')
            game.launch_game()
        except:
            print(f'Error. File {file_name} could not be read. Try again.')
    else:
        players_num = input('Enter the number of players (2 - 6):>').strip()
        if players_num not in ['2', '3', '4', '5', '6']:
            print('Invalid number of players. Defaulting to: 2')
            players_num = '2'

        # convert the player number to an integer.
        players_num = int(players_num)

        # create the game
        game = Game(player_count=players_num)
        game.launch_game()



