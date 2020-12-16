import discord
from discord.ext import commands
from data import DB

class IniativeTracker(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=["t"], invoke_without_command=True)
    async def test(self, ctx):
        """Commands to help track combat."""
        await ctx.send(f"Incorrect usage. Use `{ctx.prefix}help init` for help.")


def setup(bot):
    bot.add_cog(IniativeTracker(bot))