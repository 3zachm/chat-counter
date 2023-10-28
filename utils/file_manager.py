import configparser
import os

script_dir = ''

def config_loc():
    return script_dir + '/config.ini'

def make_config(path):
    config = configparser.ConfigParser()
    if not os.path.exists(path):
        config['twitch'] = {
            'token': '',
            'channel': '',
            'username': ''}
        config['quickwit'] = {
            'host': 'localhost:7280',
            'index': 'default'}
        config.write(open(path, 'w'))
        print('Config generated. Please edit it with your token and SQL login.')
        quit()