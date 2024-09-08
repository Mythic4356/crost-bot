import os
import json
import nextcord
from nextcord.ext import commands
from nextcord.ui import Button, View
from nextcord import Interaction
from nextcord.abc import GuildChannel
import asyncio
import PIL

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

e = ["0","1","2","3","4","5","6"]

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def brick(ctx):
    parry_button = nextcord.ui.Button(label="Parry", style= nextcord.ButtonStyle.green,disabled=True )
    quit_button = nextcord.ui.Button(label="Quit", style= nextcord.ButtonStyle.danger)
    round = 0
    view = nextcord.ui.View()
    view.add_item(parry_button)
    view.add_item(quit_button)
    parried = False
    win = True
    msg = await ctx.send("insert funny brick game haha", view=view)

    async def parry_callback(interaction:Interaction):
        nonlocal parried
        lock = asyncio.Lock()
        await lock.acquire()
        parried=True
        lock.release()

    parry_button.callback= parry_callback
    for i in range(7):
        if i == 6:
            parry_button.disabled=False
            
        else:
            parry_button.disabled=True
            
        await msg.edit(f"Round: {round}\n{e[i]}", view=view, file=nextcord.File(f"bot-stuff/brick/{e[i]}.png"))
        await asyncio.sleep(0.5)

    await asyncio.sleep(0.5)
    


    
    parry_button.disabled=True
    print(parried)
    if parried:
        await msg.edit("GOOD JOB U WON!!!", view=view, file=nextcord.File(f"bot-stuff/brick/7.png"))
        round += 1
    else:
        win = False
        await msg.edit("imagine losing", view=view, file=nextcord.File(f"bot-stuff/brick/heaven.jpg"))

    while win:
        parried = False
        for i in range(7):
            await msg.edit(f"round: {round}\n{e[i+1*-1]}",file=nextcord.File(f"bot-stuff/brick/{e[i*-1]}.png"))
            await asyncio.sleep(0.1)
        for i in range(7):
            if i == 6:
                parry_button.disabled=False
            else:
                parry_button.disabled=True
            await msg.edit(f"round: {round}\n{e[i]}", view=view, file=nextcord.File(f"bot-stuff/brick/{e[i]}.png"))
            await asyncio.sleep(0.5)
        await asyncio.sleep(0.5)

        parry_button.disabled=True
        if parried:
            round +=1
            await msg.edit("GOOD JOB U WON!!!", view=view)
        else:
            win = False
            await msg.edit("imagine losing", view=view, file=nextcord.File(f"bot-stuff/brick/heaven.jpg"))
bot.run(TOKEN)