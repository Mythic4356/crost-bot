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

e = ["https://github.com/Mythic4356/crost-bot/blob/main/bot-stuff/brick/images/0.png?raw=true",
     "https://github.com/Mythic4356/crost-bot/blob/main/bot-stuff/brick/images/1.png?raw=true",
     "https://github.com/Mythic4356/crost-bot/blob/main/bot-stuff/brick/images/2.png?raw=true",
    "https://github.com/Mythic4356/crost-bot/blob/main/bot-stuff/brick/images/3.png?raw=true",
    "https://github.com/Mythic4356/crost-bot/blob/main/bot-stuff/brick/images/4.png?raw=true",
    "https://github.com/Mythic4356/crost-bot/blob/main/bot-stuff/brick/images/5.png?raw=true",
    "https://github.com/Mythic4356/crost-bot/blob/main/bot-stuff/brick/images/6.png?raw=true",
    ]

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def site(ctx):
    msg = await ctx.send("Visit us in\nhttps://mythic4356.github.io/crost-bot/")

@bot.slash_command(description="p i n g")
async def ping(interaction: Interaction):
    await interaction.response.send_message("Pong!")

@bot.command(description="Play a game that will give you dementia")
async def brick(ctx):
    if ctx.author.id in brick_players:
        brick_players = []
        brick_players.append(ctx.author.id)
        parry_button = nextcord.ui.Button(label="Parry", style= nextcord.ButtonStyle.green,disabled=True )
        round = 0
        view = nextcord.ui.View()
        view.add_item(parry_button)
        parried = False
        win = True
    
        embed = nextcord.Embed(title="Brick Tennis", description=f"Round: {round}")
        msg = await ctx.send(" ", view=view,embed=embed )

        async def parry_callback(interaction:Interaction):
            nonlocal parried
            lock = asyncio.Lock()
            await lock.acquire()
            parried=True
            lock.release()
    
        parry_button.callback= parry_callback

        while win:
            parried = False
            for i in range(7):
                if i == 6:
                    parry_button.disabled=False
                    embed.description = f"Round: {round}\n PARRY NOW!"
                else:
                    parry_button.disabled=True
                    embed.description = f"Round: {round}"
                embed.set_image( e[i])
                await msg.edit(view=view, embed=embed)
                await asyncio.sleep(0.5)
                print("think fast chucklenuts")
            await asyncio.sleep(0.5)

            parry_button.disabled=True
            print(parried)
            print(win)
            if parried:
                round += 1
                embed.description = f"Round: {round}\n+ PARRY"
                embed.set_image( "https://github.com/Mythic4356/crost-bot/blob/main/bot-stuff/brick/images/7.png?raw=true",)
            else:
                win = False
                embed.description = f"Round: {round}\n imagine dying lmfao"
                embed.set_image( "https://github.com/Mythic4356/crost-bot/blob/main/bot-stuff/brick/images/heaven.jpg?raw=true")
            await msg.edit(view=view, embed=embed)
        
            print("---")
            print(parried)
            print(win)
            await asyncio.sleep(1)
            if win:
                for i in range(7):
                    embed.set_image( e[i*-1])
                    await msg.edit(view=view,embed=embed)
                    await asyncio.sleep(0.1)
                    print("rebound")
    else:
        ctx.reply("You already have an ongoing game!")
bot.run(TOKEN)