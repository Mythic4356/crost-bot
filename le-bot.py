import os
import json
import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import Interaction,app_commands, webhook
from discord import InteractionResponseType, integrations
from discord.abc import GuildChannel   
from modules.Constants import TimeLeft,brickImages
import asyncio
from PIL import ImageDraw, Image, ImageFont
import requests
import modules.db
import aiohttp

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
    if modules.db.load(f"users/{userid}") == False:
        modules.db.save(f"users/{userid}", 
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

@app_commands.user_install()
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.tree.command(description="ora")
async def uwu(ctx:Interaction):
    print("ez")
    msg = await ctx.response.send_message("OwO")

@app_commands.user_install()
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.tree.command(description="show the site")
async def sites(ctx:Interaction):
    print("ez")
    msg = await ctx.response.send_message("Visit us in\nhttps://mythic4356.github.io/crost-bot/")


@app_commands.user_install()
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.tree.command(name="bake")
async def bake(ctx):
    userid = ctx.user.id
    check(userid)
    modules.db.save(f"users/{userid}/croissants", (modules.db.load(f"users/{userid}/croissants") + 1))





@app_commands.user_install()
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.tree.command(description="p i n g")
async def ping(ctx: Interaction):
    await ctx.response.send_message("Pong!")




@app_commands.user_install()
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.tree.command(name="feed", description="Feed da gremlin")
async def feed(ctx: Interaction):
    await ctx.response.send_message("Later", ephemeral= True)


@app_commands.user_install()
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.tree.command(name="petpet", description="W.I.P")
async def petpet(ctx: commands.Context, user: discord.Member = None):
    pass

brick_players = []

@app_commands.user_install()
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.tree.command(name="brick", description="Play brick tennis with quaso cat")
async def brick(ctx: Interaction):

    e = brickImages
    if not ctx.user.id in brick_players:

        brick_players.append(ctx.user.id)
        parry_button = discord.ui.Button(label="Parry", style= discord.ButtonStyle.green,disabled=True )
        round = 0
        view = discord.ui.View()
        view.add_item(parry_button)
        parried = False
        win = True
    
        embed = discord.Embed(title="Brick Tennis", description=f"Round: {round}")
        msg = ctx.response
        await msg.send_message(" ", view=view,embed=embed)
        msg = await ctx.original_response()

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
                embed.set_image(url=e[i])
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
                embed.set_image(url="https://github.com/Mythic4356/crost-bot/blob/main/bot-stuff/brick/images/7.png?raw=true",)
            else:
                win = False
                embed.description = f"Round: {round}\n imagine dying lmfao"
                embed.set_image(url="https://github.com/Mythic4356/crost-bot/blob/main/bot-stuff/brick/images/heaven.jpg?raw=true")
                brick_players.remove(ctx.user.id)
            await msg.edit(view=view, embed=embed)
        
            print("---")
            print(parried)
            print(win)
            await asyncio.sleep(1)
            if win:
                print(e)
                e.reverse()
                for i in e:
                    embed.set_image(url=i)
                    await msg.edit(view=view,embed=embed)
                    await asyncio.sleep(0.1)
                    print("rebound " + str(i))
                e.reverse()
    else:
        print(brick_players)
        await ctx.response.send_message("You already have an ongoing game!")
bot.run(TOKEN)