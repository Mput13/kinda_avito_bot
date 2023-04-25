import configparser


def get_token():
    config = configparser.ConfigParser()
    return config.read()
