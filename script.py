import socket
import logging
import os
import io
import utils.utils as utils
import configparser
import utils.file_manager as files
import utils.api.db as sql
import utils.user_db as users
from emoji import demojize

# set script_dir to proper path in the files script (for file locations)
files.script_dir = os.path.dirname(os.path.realpath(__file__))
files.make_config(files.config_loc())

with open(files.config_loc()) as c:
    discord_config = c.read()
config = configparser.RawConfigParser(allow_no_value=True)
config.read_file(io.StringIO(discord_config))

# make sure config file is properly filled
try:
    channel = config.get('twitch', 'channel')
    token = config.get('twitch', 'token')
    nickname = config.get('twitch', 'username')
    sql.user = config.get('sql', 'user')
    sql.password = config.get('sql', 'password')
    sql.host = config.get('sql', 'ip')
    sql.database = config.get('sql', 'database')
    sql.initiate()
except (configparser.NoSectionError, configparser.NoOptionError) as e:
    print(e)
    print("Ensure config file has all entries present. If you recently pulled an update, consider regenerating the config")
    quit()

server = 'irc.chat.twitch.tv'
port = 6667

sock = socket.socket()
sock.connect((server, port))
sock.send(f"PASS {token}\n".encode('utf-8'))
sock.send(f"NICK {nickname}\n".encode('utf-8'))
sock.send(f"JOIN {channel}\n".encode('utf-8'))
sock.send("CAP REQ :twitch.tv/tags\n".encode('utf-8'))

print("\nConnected!\n")

while True:
    resp = sock.recv(2048).decode('utf-8')

    if resp.startswith('PING'):
        sock.send("PONG\n".encode('utf-8'))
    elif len(resp) > 0:
        resp = demojize(resp)
        userid_index = resp.find("user-id=") + 9
        user_id = resp[userid_index : resp.find(";", userid_index)]
        message = resp[resp.find(channel) + len(channel) + 2:]
        if utils.findWholeWord("yepcock")(message) is not None:
            if (len(users.get_user(user_id))) < 1:
                users.insert_user(user_id)
            users.update_user("yep", user_id)
            users.update_user("cock", user_id)
            print(user_id + " " + message)
        else:
            if utils.findWholeWord("yep")(message) is not None:
                if (len(users.get_user(user_id))) < 1:
                    users.insert_user(user_id)
                users.update_user("yep", user_id)
                print(user_id + " " + message)
            if utils.findWholeWord("cock")(message) is not None:
                if (len(users.get_user(user_id))) < 1:
                    users.insert_user(user_id)
                users.update_user("cock", user_id)
                print(user_id + " " + message)