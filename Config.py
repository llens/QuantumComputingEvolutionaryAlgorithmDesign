import configparser


class Config:

    config: configparser.ConfigParser

    def __init__(self):
        # Read local file `config.ini`.
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

    def get_config_value(self, heading: str, name: str) -> str:
        return self.config.get(heading, name)
