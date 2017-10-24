import discord
import os
import io
from discord.ext import commands 
bot = commands.Bot(command_prefix='*',description="This bot is weird. Deal with it.\n\nHelp Commands",owner_id=277981712989028353)


@bot.event
async def on_ready():
   print('Bot is online!') 


@bot.command()
async def say(ctx, *, message: str):
    """Say Something As The Bot""" 
    await ctx.send(message)
   
   
@bot.command()
async def ping(ctx):
    """Pong! Returns your websocket latency."""
    em = discord.Embed()
    em.title ='Pong! Websocket Latency:'
    em.description = f"{bot.ws.latency * 1000:.4f} ms"
    await ctx.send(embed=em)

   
     
if not os.environ.get('TOKEN'):
    print("no token found REEEE!")
bot.run(os.environ.get('TOKEN').strip('"'))


