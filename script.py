from twitchio.ext import commands
import os
import io
import utils.utils as utils
import configparser
import utils.file_manager as files
import utils.api.db as sql
import utils.user_db as users
import utils.log_db as log
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


bot = commands.Bot(
    irc_token=token,
    nick=nickname,
    prefix='!',
    initial_channels=[channel]
)

@bot.event
async def event_ready():
    print(f'Ready | {bot.nick}')

def inc_user(column, user_id, new_user):
    if new_user:
        users.insert_user(user_id)
    users.update_user(str(column), user_id)

@bot.event
async def event_message(message):
    user_id = str(message.tags['user-id'])
    log.insert_log(user_id, message.author.name, message.content, message.tags)
    yep = utils.findWholeWord("yep")(message.content) is not None
    cock = utils.findWholeWord("cock")(message.content) is not None
    yepcock = utils.findWholeWord("yepcock")(message.content) is not None
    new_user = (len(users.get_user(user_id))) < 1
    if yep:
        inc_user("yep", user_id, new_user)
        yepcock = False
    if cock:
        inc_user("cock", user_id, new_user)
        yepcock = False
    if yepcock:
        inc_user("yep", user_id, new_user)
        inc_user("cock", user_id, new_user)
    #await bot.handle_commands(message)

bot.run()