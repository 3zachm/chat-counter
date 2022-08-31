from twitchio.ext import commands
import os
import io
import configparser
import pathlib
import utils.file_manager as files
import utils.api.db as sql
import utils.log_db as log

# set script_dir to proper path in the files script (for file locations)
files.script_dir = os.path.dirname(os.path.realpath(__file__))
files.make_config(files.config_loc())

discord_config = pathlib.Path(files.config_loc()).read_text()
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

@bot.event
async def event_message(message):
    if message.author.name.lower() == bot.nick.lower():
        return
    user_id = str(message.tags['user-id'])
    log.insert_log(user_id, message.author.name, message.content, message.tags)
    # not worth using the command decorator for this, update to new twitchio if needed later cause it no longer uses irc logins
    if (message.tags['mod'] == '1' or message.tags['badges'].find('broadcaster') != -1) and message.content == '!nukelogpoints':
        await message.channel.send('!gamble all')

bot.run()