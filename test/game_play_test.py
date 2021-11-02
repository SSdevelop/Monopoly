"""
Here, we test the various game scenarios
"""

from app.Config import Config
from app.Game import Game


def test_salary_start():
    """
    user always starts with amount equal to salary
    """
    game = Game(4)
    for player in game.players:
        assert player.square_position == 1
        assert player.balance == Config.SALARY


def test_land_on_go():
    """
    Player lands on 1, earn salary
    """
    game = Game(4)
    player = game.players[0]
    init_balance = player.balance
    go_square = game.board.get_square(1)
    go_square.land_on(player)
    assert player.balance == (init_balance + Config.SALARY)


def test_land_passthrough_go():
    """
    Player passes through 1, earn salary
    """
    game = Game(4)
    player = game.players[0]
    init_balance = player.balance
    go_square = game.board.get_square(1)
    go_square.pass_through(player)
    assert player.balance == (init_balance + Config.SALARY)


def test_land_on_property_then_buys():
    """
    Test user lands on a property cell.
    """
    game = Game(4)
    from app.Square import PropertySquare

    property_: PropertySquare = game.board.get_square(12)
    assert property_.owner_token is None
    player = game.players[0]
    init_balance = player.balance
    Config.DEFAULT_BUY_PROPERTY_CHOICE = '1'
    property_.land_on(player)

    assert property_.owner_token == player.token
    assert player.balance == (init_balance - property_.price)

    # the same user lands on a property they own, nothing should happen.
    # to their balance.
    init_balance = player.balance
    property_.land_on(player)

    assert player.balance == init_balance


def test_user_lands_on_unowned_property_declines_buy():
    """
    User lands on unowned property cell, they don't buy it. balance is intact.
    """

    game = Game(4)
    from app.Square import PropertySquare

    property_: PropertySquare = game.board.get_square(10)
    assert property_.owner_token is None
    player = game.players[0]
    init_balance = player.balance
    Config.DEFAULT_BUY_PROPERTY_CHOICE = '2'
    property_.land_on(player)

    assert property_.owner_token is None
    assert player.balance == init_balance


def test_player_lands_on_income_tax_then_pays_tax():
    """
     Player lands on income tax, they pay tax
    """
    game = Game(4)
    from app.Square import IncomeTaxSquare
    income_tax: IncomeTaxSquare = game.board.get_square(4)
    player = game.players[0]
    init_balance = player.balance
    income_tax.land_on(player)
    assert player.balance == (init_balance - 150)


def test_player_lands_in_jail_visiting_then_nothing_happens():
    """
    Player lands on in jail / visiting. Nothing happens
    """
    game = Game(4)
    from app.Square import InJailOrVisitingSquare
    jail_square: InJailOrVisitingSquare = game.board.get_square(6)
    player = game.players[0]
    init_balance = player.balance
    assert not player.is_jailed

    jail_square.land_on(player)
    assert not player.is_jailed
    assert init_balance == player.balance


def test_player_chance_then_lose_or_gain_money():
    """
    Player lands on a chance, they either lose or gain some money. balance is updated.
    """
    game = Game(4)
    from app.Square import ChanceSquare
    chance_sq: ChanceSquare = game.board.get_square(9)
    player = game.players[0]
    init_balance = player.balance

    chance_sq.land_on(player)
    assert player.balance < init_balance or player.balance > init_balance


def test_land_free_parking_nothing_happens():
    """
    Player lands on free parking. nothing happens
    """
    game = Game(4)
    from app.Square import FreeParkingSquare
    square: FreeParkingSquare = game.board.get_square(11)
    player = game.players[0]
    init_balance = player.balance
    square.land_on(player)

    assert player.balance == init_balance
    assert not player.is_jailed


def test_player_lands_on_go_to_jail_then_are_jailed():
    """
    Player lands on go to jail. They are jailed. Ensure Correct state and correct position.
    """
    game = Game(4)
    from app.Square import GoToJailSquare
    square: GoToJailSquare = game.board.get_square(16)
    player = game.players[0]

    assert not player.is_jailed
    assert player.square_position == 1

    square.land_on(player)

    assert player.is_jailed
    assert player.square_position == 6


def test_play_after_being_jailed_1():
    """
    it is the first turn of the player after being jailed.
    selected game mode is 'feeling lucky'
    their throw was not a double.
    player position should be the same. they are still in jail
    """
    game = Game(4)
    from app.Square import GoToJailSquare
    square: GoToJailSquare = game.board.get_square(16)
    player = game.players[0]
    square.land_on(player)

    Config.DEFAULT_JAIL_STRATEGY = '1'
    Config.DIE_1_VALUE = 1
    Config.DIE_2_VALUE = 4

    player.play()

    assert player.square_position == 6
    assert player.is_jailed


def test_play_after_being_jailed_2():
    """
    it is the 3rd turn of the user after being jailed.
    selected game mode is 'feeling lucky'
    their throw was not a double.
    user should pay fine. No longer jailed. Position should change.
    """
    game = Game(4)
    from app.Square import GoToJailSquare
    square: GoToJailSquare = game.board.get_square(16)
    player = game.players[0]
    square.land_on(player)

    Config.DEFAULT_JAIL_STRATEGY = '1'
    Config.DIE_1_VALUE = 1
    Config.DIE_2_VALUE = 4
    player.move_count_since_jail = 2

    init_balance = player.balance

    player.play()

    assert player.square_position != 6
    assert not player.is_jailed
    assert player.balance < init_balance


def test_play_after_being_jailed_3():
    """
    it is the 2nd turn of the user after being jailed.
    selected game mode is 'feeling lucky'
    their throw was a double.
    user should get out of jail. Pos and state should change.
    """

    Config.DEFAULT_JAIL_STRATEGY = '1'
    Config.DIE_1_VALUE = 1
    Config.DIE_2_VALUE = 1

    game_temp = Game(4)
    from app.Square import GoToJailSquare
    square: GoToJailSquare = game_temp.board.get_square(16)
    player = game_temp.players[1]
    square.land_on(player)
    player.move_count_since_jail = 1

    init_balance = player.balance

    player.play()

    assert player.square_position != 6
    assert not player.is_jailed
    assert player.balance == init_balance


def test_play_after_being_jailed_4():
    """
    it is the first turn of the user after being jailed.
    selected strategy is 'bail mode'
    they have agreed to not to pay for this round.
    the user's position should change. They haven't cleared the bail, so are still
    technically in jail.
    """

    Config.DEFAULT_JAIL_STRATEGY = '2'
    Config.DEFAULT_BAIL_MODE_PAY_NOW = '2'

    game = Game(4)
    from app.Square import GoToJailSquare
    square: GoToJailSquare = game.board.get_square(16)
    player = game.players[0]
    square.land_on(player)

    init_balance = player.balance

    player.play()

    assert player.square_position != 6
    assert player.is_jailed
    assert player.balance == init_balance


def test_play_after_being_jailed_5():
    """
    it is the first turn of the user after being jailed.
    selected strategy is 'bail mode'
    they have agreed to pay for this round.
    the user's position should change. jail status is updated, no longer jailed.
    balance should change.
    """

    Config.DEFAULT_JAIL_STRATEGY = '2'
    Config.DEFAULT_BAIL_MODE_PAY_NOW = '1'

    game = Game(4)
    from app.Square import GoToJailSquare
    square: GoToJailSquare = game.board.get_square(16)
    player = game.players[0]
    square.land_on(player)

    init_balance = player.balance

    player.play()

    assert player.square_position != 6
    assert not player.is_jailed
    assert player.balance < init_balance


def test_play_after_being_jailed_6():
    """
    it is the second turn of the user after being jailed.
    selected strategy is 'bail mode'
    player is forced to pay fine.
    the user's position should change. jail status should be updated.
    """

    Config.DEFAULT_JAIL_STRATEGY = '2'

    game = Game(4)
    from app.Square import GoToJailSquare
    square: GoToJailSquare = game.board.get_square(16)
    player = game.players[0]
    square.land_on(player)

    init_balance = player.balance

    player.move_count_since_jail = 1

    player.play()

    assert player.square_position != 6
    assert not player.is_jailed
    assert player.balance < init_balance


def test_player_lands_on_owned_property_then_pays_rent():
    """
    User lands on property owned by someone else, they pay rent
    """
    from app.Square import PropertySquare

    game = Game(4)
    # player 1 buys property.
    property_: PropertySquare = game.board.get_square(10)
    assert property_.owner_token is None
    player = game.players[0]
    init_balance = player.balance
    Config.DEFAULT_BUY_PROPERTY_CHOICE = '1'
    property_.land_on(player)

    assert property_.owner_token == player.token
    assert player.balance == (init_balance - property_.price)

    init_balance = player.balance

    # player 2 lands on property of player 1
    player2 = game.players[1]
    init_balance2 = player2.balance
    property_.land_on(player2)

    assert player2.balance == (init_balance2 - property_.rent)
    assert player.balance == (init_balance + property_.rent)
