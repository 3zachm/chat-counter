import json
from twitchio.ext import commands
import os
import io
import configparser
import pathlib
import utils.file_manager as files
# set script_dir to proper path in the files script (for file locations)
files.script_dir = os.path.dirname(os.path.realpath(__file__))
files.make_config(files.config_loc())

config_file = pathlib.Path(files.config_loc()).read_text()
config = configparser.RawConfigParser(allow_no_value=True)
config.read_file(io.StringIO(config_file))

# make sure config file is properly filled
try:
    channel = config.get('twitch', 'channel')
    token = config.get('twitch', 'token')
    nickname = config.get('twitch', 'username')
    host = config.get('quickwit', 'host')
    index = config.get('quickwit', 'index')
except (configparser.NoSectionError, configparser.NoOptionError) as e:
    print(e)
    print("Ensure config file has all entries present."
          "If you recently pulled an update, consider regenerating the config")
    quit()

bot = commands.Bot(
    irc_token=token,
    nick=nickname,
    prefix='!',
    initial_channels=[channel]
)
ingest_url = f'http://{host}/api/v1/{index}/ingest'


@bot.event
async def event_ready():
    print(f'Ready | {bot.nick}')


@bot.event
async def event_message(message):
    if message.author.name.lower() == bot.nick.lower():
        return
    # POST request to /ingest with json body
    body = {
        "timestamp": message.tags['tmi-sent-ts'],
        "user_id": message.tags['user-id'],
        "user_name": message.author.name,
        "message": message.content,
        "badges": message.tags['badges'],
        "is_mod": message.tags['mod'] == 1,
        "is_sub": message.tags['subscriber'] == 1,
        "is_turbo": message.tags['turbo'] == 1,
        "color": message.tags['color']
    }
    await bot.http._session.post(ingest_url, data=json.dumps(body))
    # not worth using the command decorator for this
    if (
            (message.tags['mod'] == 1 or message.tags['badges'].find('broadcaster') != -1)
            and message.content == '!nukelogpoints'
       ):
        await message.channel.send('!gamble all')

bot.run()
