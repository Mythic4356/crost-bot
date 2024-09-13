import os
import json
import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import Interaction,app_commands
from discord import InteractionResponseType, integrations
from discord.abc import GuildChannel   
import asyncio
from PIL import ImageDraw, Image, ImageFont
import requests
import db


async def site(ctx:commands.Context):
    msg = await ctx.send("Visit us in\nhttps://mythic4356.github.io/crost-bot/")
    await print("Oh Yeah! Vector!")
