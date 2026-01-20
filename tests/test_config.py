from Config import Config


def test_get_config_value():
    config = Config()
    assert config.get_config_value('test_heading', 'test_name') == 'test_value'
