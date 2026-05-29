import configparser
config = configparser.ConfigParser()
config.read('config/config.ini')

class ReadConfig:
    URL = config.get('common','url')
    USERNAME = config.get('common','username')
    PASSWORD = config.get('common','password')
