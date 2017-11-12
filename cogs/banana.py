import discord
import sys
import os
import io
from discord.ext import commands


class banana:

    def __init__(self, bot):
        self.bot = bot
        
        
    @commands.command()
        async def ping(self, ctx)
            """Playing Ping Pong. Returning your websocket latency."""
            em = discord.Embed()
            em.title = 'Pong! This is your websocket latency:'
            em.description = f"{bot.ws.latency * 1000:.4f} ms"
            await ctx.send(embed=em)
        
        
def setup(bot): 
    bot.add_cog(banana(bot))

