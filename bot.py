#!/usr/bin/env python3
from http import client
import discord
from datetime import datetime
import shlex

from turtlesay import turtle_say

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    user = await client.fetch_user(362904607720210432)
    img = turtle_say(str(datetime.now().strftime("%m/%d/%Y %H:%M:%S")), 65)
    await user.send(file=discord.File(fp=img, filename='logindate.png'))

def turtle_say_help():
    return "!say <message//second line> [-s maxsize] [-p interline-pad [left-pad [right-pad]]]"

def turtle_parser(s: str) -> dict:
    try:
        tokens = shlex.split(s)
        assert tokens.pop(0) == "!say"
        args = {} # text size padm padl padr

        print(tokens)

        next_tok = 'text'
        for tok in tokens:
            if next_tok == 's':
                args['size'] = int(tok)
                next_tok = 'text'
            elif next_tok == 'p':
                if 'padl' in args:
                    args['padr'] = float(tok)
                    next_tok = 'text'
                elif 'padm' in args:
                    args['padl'] = float(tok)
                else:
                    args['padm'] = float(tok)
            elif tok == '-s':
                next_tok = 's'                        
            elif tok == '-p':
                next_tok = 'p'
            else:
                if 'text' not in args:
                    args['text'] = tok
                else:
                    args['text'] += " " + tok                    
        return args
    except Exception as e:
        print(e)
        return {} 
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!say'):
        args = turtle_parser(message.content)
        if args == {}:
            await message.author.send(turtle_say_help())
            return
        img = turtle_say(**args)
        await message.author.send(file=discord.File(fp=img, filename='turtle.png'))


with open("TOKEN") as f:
    TOKEN = f.read()
    
client.run(TOKEN)
