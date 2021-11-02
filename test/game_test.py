import os

from app.Game import Game

"""
Following functions test the Game class.
"""


def test_get_player():
    """
    Test get player by token
    """
    game = Game(2)
    p1 = game.get_player("No such token")
    p2 = game.get_player('Player 1')

    assert p1 is None
    assert p2 is not None


def test_get_player_by_id():
    """
    Test get player by id.
    """
    game = Game(3)
    p1 = game.get_player_by_id(0)
    assert p1 is not None
    p2 = game.get_player_by_id(2)
    assert p2 is not None
    p3 = game.get_player_by_id(-9)
    assert p3 is None
    p4 = game.get_player_by_id(100)
    assert p4 is None


def test_is_game_over():
    """
    Tests whether game is over or not.
    Maximum number of rounds is 100, so any number of rounds more than that will end the game.
    """
    game = Game(3)
    assert not game.is_game_over()

    game.current_round = 101
    assert game.is_game_over()

    game.current_round = 1
    for index, player in enumerate(game.players):
        if index == 0:
            continue
        player.exit_game()

    assert game.is_game_over()


def test_create_players():
    """
    Test whether the number of players created matches the required number of players or not
    """
    game = Game(5)
    assert len(game.players)


def test_get_winners(capsys):
    """
    Test winners and test whether the console output is correct or not.
    """
    game = Game(3)

    # multiple winners.
    winners = game.get_winners()
    assert len(winners) == 3

    game.announce_winners()
    captured = capsys.readouterr()
    assert captured.out == '\n ------ GAME OVER --------\n' \
                           'The winners of the game are:-\n' \
                           'Player 1 with a balance of HKD 1500\n' \
                           'Player 2 with a balance of HKD 1500\n' \
                           'Player 3 with a balance of HKD 1500\n'

    # single winner
    for index, player in enumerate(game.players):
        if index == 2:
            continue
        player.exit_game()

    winners = game.get_winners()
    assert len(winners) == 1
    # testing the console output

    # winner with highest balance
    game = Game(5)
    game.players[0].balance = 10000
    winners = game.get_winners()
    assert len(winners) == 1
    assert winners[0].token == game.players[0].token


def test_save_game():
    """
    To test whether the game is being saved correctly or not.
    """
    game = Game(3)
    parent_path = os.path.dirname(os.getcwd())
    os.chdir(parent_path)
    filename = game.save_game()
    assert os.path.exists(parent_path + '\\saved_games\\' + filename)
