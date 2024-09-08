import os
import json
import nextcord
from nextcord.ext import commands
from nextcord.ui import Button, View
from nextcord import Interaction
from nextcord.abc import GuildChannel


try:
    
    TOKEN = os.environ["token"]
    print("Token loaded from environment")
except:
    try:
        TOKEN = json.load(open("../crost-secret/token.json"))['Token']
        print("Token loaded from local config")
    except:
        print("No Token found from environment or config")

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