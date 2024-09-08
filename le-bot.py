import os
import nextcord
from nextcord.ext import commands
from nextcord.ui import Button, View
from nextcord import Interaction, app_commands
from nextcord.abc import GuildChannel

TOKEN = os.environ["token"]

intents = nextcord.Intents.default()
intents.message_content = True
intents.members=True
bot = commands.Bot(command_prefix="quaso ", intents=intents)
bot.remove_command("help")
client = nextcord.Client(intents=intents)



@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

bot.run(TOKEN)