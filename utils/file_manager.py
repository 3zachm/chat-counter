import configparser
import os

script_dir = ''

def prefix_loc():
    return script_dir + '/prefixes.json'

def config_loc():
    return script_dir + '/config.ini'

def make_config(path):
    config = configparser.ConfigParser()
    if not os.path.exists(path):
        config['twitch'] = {
            'token': '',
            'channel': '',
            'username': ''}
        config['sql'] = {
            'user': 'default',
            'password': 'pass',
            'ip': '127.0.0.1',
            'database': 'default'}
        config.write(open(path, 'w'))
        print('Config generated. Please edit it with your token and SQL login.')
        quit()