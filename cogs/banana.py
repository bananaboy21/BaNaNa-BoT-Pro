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
            """Check If The Bot Is Working."""
            em = discord.Embed()
            em.title = 'Pong!'
            em.description = "Bot Is Up And Working"
            await ctx.send(embed=em)
        
        
def setup(bot): 
    bot.add_cog(banana(bot))

