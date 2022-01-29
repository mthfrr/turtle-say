#!/usr/bin/env python3
from distutils.command.clean import clean
from http import client
import discord
from datetime import datetime

from turtlesay import turtle_say

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    user = await client.fetch_user(362904607720210432)
    img = turtle_say(str(datetime.now().strftime("%m/%d/%Y %H:%M:%S")), 65)
    await user.send(file=discord.File(fp=img, filename='logindate.png'))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!say'):
        img = turtle_say("OUI OUI ALLER")
        await message.author.send(file=discord.File(fp=img, filename='turtle.png'))


with open("TOKEN") as f:
    TOKEN = f.read()
    
client.run(TOKEN)
