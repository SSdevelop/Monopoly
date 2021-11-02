from app.game import Game


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
    Test game is not over.
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
    Test if the players were created correctly.
    """
    game = Game(5)
    assert len(game.players)


def test_get_winners():
    """
    Test winners.
    """
    game = Game(5)

    # multiple winners.
    winners = game.get_winners()
    assert len(winners) == 5

    # single winner
    for index, player in enumerate(game.players):
        if index == 2:
            continue
        player.exit_game()

    winners = game.get_winners()
    assert len(winners) == 1

    # winner with highest balance
    game = Game(5)
    game.players[0].balance = 10000
    winners = game.get_winners()
    assert len(winners) == 1
    assert winners[0].token == game.players[0].token


