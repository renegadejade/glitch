import discord
from discord.ext import commands
from data import DB
import variables



class Character(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=["c", "char"], invoke_without_command=True)
    async def character(self, ctx):
        """Commands to help track combat."""
        await ctx.send(f"Incorrect usage. Use `{ctx.prefix}help character` for help.")


    @character.command(name="name", help="Set your character's name")
    async def name(self, ctx, name):
        data = {
            "name" : name
        }
        DB.collection("users").document(str(ctx.message.author.id)).set(data, merge=True)
        results = "Your character's name is " + name
        await ctx.send(results)

    @character.command(name="set", help="Set a STAT or Skill to a certain level")
    async def set(self, ctx, stat, val):
        if stat.lower() in variables.STATS and int(val) is not None:
            character_ref = DB.collection("users").document(str(ctx.message.author.id))
            character_ref.set(
                {
                    stat.lower() : val
                }, merge=True
            )
            character = character_ref.get()
            results = character.to_dict()["name"]+ "'s " + stat.upper() + " is now set to " + str(val)
        elif stat.lower() in variables.SKILLS and int(val) is not None:
            character_ref = DB.collection("users").document(str(ctx.message.author.id))
            character_ref.set(
                {
                    stat.lower() : val
                }, merge=True
            )
            character = character_ref.get()
            results = character.to_dict()["name"]+ "'s " + stat + " is now set to " + str(val)
        else:
            results = "\"" + stat + "\" isn't a STAT or Skill. Try again."
        
        await ctx.send(results)


def setup(bot):
    bot.add_cog(Character(bot))