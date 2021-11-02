from app.Config import Config


def test_config():
    """
    Checks the Config class. The Config class defines certain configuration settings
    for the game. This function checks that those configurations are assigned correctly,
    and the configurations can be changed whenever required.
    """
    config = Config()
    assert config.CURRENCY == 'HKD'
    assert config.SALARY == 1500
    assert config.JAIL_SQUARE_POSITION == 6
    assert config.MAX_ROUND_COUNT == 100
    assert config.MAX_PLAYER_COUNT == 6
    assert config.MIN_PLAYER_COUNT == 2
    assert config.MAX_SQUARE_COUNT == 20
    assert config.JAIL_FINE == 150
    assert config.IS_TEST_ENVIRONMENT
    assert config.DEFAULT_BUY_PROPERTY_CHOICE == '2'
    assert config.DEFAULT_JAIL_STRATEGY == '1'
    assert config.DEFAULT_BAIL_MODE_PAY_NOW == '1'
    assert config.DIE_1_VALUE == 4
    assert config.DIE_2_VALUE == 1

    config.IS_TEST_ENVIRONMENT = False
    config.CURRENCY = 'USD'

    assert config.CURRENCY == 'USD'
    assert not config.IS_TEST_ENVIRONMENT
