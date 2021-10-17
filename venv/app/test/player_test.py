"""
Player test cases
"""
from app.config import Config
from app.game import Game
from app.player import Player

game = Game(player_count=3)

Config.IS_TEST_ENVIRONMENT = True


def test_collect_salary():
    """
    Test player collects salary
    """
    initial_balance = 300
    player = game.players[0]
    player.balance = initial_balance
    player.collect_salary()

    assert player.balance == (initial_balance + Config.SALARY)


def test_pay_tax():
    """
    Test the player paying tax.
    """
    player = game.players[0]
    player.balance = 30
    tax_paid = player.pay_tax()

    assert tax_paid == 0
    assert player.balance == 30

    player.balance = 300
    tax_paid = player.pay_tax()

    assert tax_paid == 30
    assert player.balance == 270

    player.balance = 420
    tax_paid = player.pay_tax()

    assert tax_paid == 40
    assert player.balance == 380


def test_go_to_jail():
    """
    Test that the player goes to jail.
    """
    player = Player(game)
    player.move_count_since_jail = 2
    player.go_to_jail()

    assert player.move_count_since_jail == 0
    assert player.is_jailed
    assert player.square_position == Config.JAIL_SQUARE_POSITION
    assert not player.jail_feeling_lucky_mode
    assert not player.jail_bail_mode


def test_lost_to_chance():
    """
    Test that the player has lost some cash to chance.
    """
    player = Player(game)
    prev_balance = player.balance
    player.lose_to_chance()
    curr_balance = player.balance
    assert prev_balance > curr_balance
    assert ((prev_balance - curr_balance) % 10) == 0
    assert (prev_balance - curr_balance) <= 300


def test_gain_from_chance():
    """
    Test that the player has gained some cash from chance.
    """
    player = Player(game)
    prev_balance = player.balance
    player.gain_from_chance()
    curr_balance = player.balance
    assert curr_balance > prev_balance
    assert ((curr_balance - prev_balance) % 10) == 0
    assert (curr_balance - prev_balance) <= 200


def test_pay_rent():
    """
    Test a player paying rent to another player.
    """
    from app.square import PropertySquare

    # create some players.
    p1 = game.players[0]
    p2 = game.players[1]

    # assign property to player 1
    prop_square: PropertySquare = game.board.get_square(2)
    prop_square.owner_token = p1.token

    # expected balances
    p1_bal = p1.balance + prop_square.rent
    p2_bal = p2.balance - prop_square.rent

    # ask player 2 to pay rent
    p2.pay_rent(prop_square.rent, p1.token, prop_square.name)

    assert p1.balance == p1_bal
    assert p2.balance == p2_bal


def test_buy_property():
    """
    Test buy a new property.
    """

    from app.square import PropertySquare

    local_game = Game(2)
    p1 = local_game.players[0]
    property_ = local_game.board.get_square(2)

    assert isinstance(property_, PropertySquare)
    assert property_.owner_token is None

    # expected balance
    p1_bal = p1.balance - property_.price

    p1.buy_property(property_)
    assert p1.balance == p1_bal


def test_exit_game():
    """
    Test player has exited the game.
    """
    player = game.players[0]
    player.balance = 10000
    prop1 = game.board.get_square(2)
    prop2 = game.board.get_square(3)
    prop3 = game.board.get_square(5)

    player.buy_property(prop1)
    player.buy_property(prop2)
    player.buy_property(prop3)

    properties_ = player.get_properties()
    assert len(properties_) == 3
    assert not player.has_exited

    player.exit_game()
    assert player.has_exited
    assert len(player.get_properties()) == 0


def test_pay_fine():
    """
    Test that the player correctly pays a fine.
    """
    player = game.players[0]
    expected_balance = player.balance - Config.JAIL_FINE
    player.pay_fine()
    assert player.balance == expected_balance


def test_move_and_land_on_square():
    """
    Test move and land on a square.
    """
    player = game.players[0]
    player.move_and_land_on_square(2)
    assert player.square_position == 3

    player.move_and_land_on_square(8)
    assert player.square_position == 11

    player.move_and_land_on_square(8)
    assert player.square_position == 19

    player.move_and_land_on_square(4)
    assert player.square_position == 3

    player.square_position = 17
    player.move_and_land_on_square(8)
    assert player.square_position == 5


def test_to_dict():
    """
    Test that the player serializes properly.
    """
    game = Game(3)
    expected_dict = {
        'token': 'Player 1',
        'balance': 10000,
        'is_jailed': False,
        'square_position': 3,
        'has_exited': True,
        'player_id': 2,
        'move_count_since_jail': 2,
        'jail_bail_mode': False,
        'jail_feeling_lucky_mode': False,
        'properties': [2, 3]
    }

    player = Player(
        game=game,
        token='Player 1',
        player_id=0
    )
    player.balance = 10000
    player.is_jailed = False
    player.square_position = 3
    player.has_exited = True
    player.player_id = 2
    player.move_count_since_jail = 2
    player.buy_property(game.board.get_square(2))
    player.buy_property(game.board.get_square(3))
    player.balance = 10000
    assert player.to_dict() == expected_dict
