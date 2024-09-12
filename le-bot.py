import os
import json
import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import Interaction,app_commands
from discord import InteractionResponseType, integrations
from discord.abc import GuildChannel   
from modules.Constants import TimeLeft,brickImages
import asyncio
from PIL import ImageDraw, Image, ImageFont
from pilmoji import Pilmoji
import requests
import db


try:
    TOKEN = os.environ["token"]
    print("Token loaded from environment")
except:
    try:
        TOKEN = json.load(open("../crost-secret/token.json"))['Token']
        print("Token loaded from local config")
    except:
        print("No Token found from environment or config")


intents = discord.Intents.default()
intents.message_content = True
intents.members=True
bot = commands.Bot(command_prefix="quaso ", intents=intents)
bot.remove_command("help")
client = discord.Client(intents=intents)

def check(userid):
    if db.load(f"users/{userid}") == False:
        db.save(f"users/{userid}", 
                {
                    "croissants": 0
                }
            )
        return False
    else:
        return True
    

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await bot.tree.sync()
    print(f"synced slash commands for {bot.user}")

@bot.hybrid_command
async def bake(ctx):
    userid = ctx.user.id
    check(userid)
    db.save(f"users/{userid}/croissants", (db.load(f"users/{userid}/croissants") + 1))





@bot.hybrid_command(name="site",with_app_command= True, description="Visit Our Site!")
async def site(ctx: commands.Context):
    msg = await ctx.send("Visit us in\nhttps://mythic4356.github.io/crost-bot/")

@bot.hybrid_command(description="p i n g")
async def ping(ctx: commands.Context):
    await ctx.response.send_message("Pong!")

brick_players = []

@bot.hybrid_command(name="feed",with_app_command= True, description="Feed da gremlin")
async def feed(ctx: commands.Context):
    await Interaction.response.send_message("Later")

@bot.hybrid_command(name="petpet",with_app_command= True, description="W.I.P")
async def petpet(ctx: commands.Context, user: discord.Member = None):
    pass

@bot.hybrid_command(name="brick",with_app_command= True, description="Play brick tennis with quaso cat")
async def brick(ctx: commands.Context):
    e = brickImages
    if not ctx.author.id in brick_players:

        brick_players.append(ctx.author.id)
        parry_button = discord.ui.Button(label="Parry", style= discord.ButtonStyle.green,disabled=True )
        round = 0
        view = discord.ui.View()
        view.add_item(parry_button)
        parried = False
        win = True
    
        embed = discord.Embed(title="Brick Tennis", description=f"Round: {round}")
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
                brick_players.remove(ctx.user.id)
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
        print(brick_players)
        await ctx.send("You already have an ongoing game!")
bot.run(TOKEN)