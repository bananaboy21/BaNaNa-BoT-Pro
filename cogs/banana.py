 import discord
import sys
import os
import io
from discord.ext import commands


class banana:

    def __init__(self, bot):
        self.bot = bot
        
        
    @commands.command()
    async def ping(self, ctx):
        """Totally cannot play Ping Pong. Or...return a websocket latency..."""
        em = discord.Embed()
        em.title = 'Pong! Websocket Latency:'
        em.description = f"{bot.ws.latency * 1000:.4f} ms"
        await ctx.send(embed=em)
