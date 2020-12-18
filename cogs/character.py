import discord
from discord.ext import commands
from data import DB

class Character(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=["c", "char"], invoke_without_command=True)
    async def character(self, ctx):
        await ctx.send(f"Incorrect usage. Use `{ctx.prefix}help character` for help.")

    @character.command(name="new", help="Creates a new character.")
    async def new(self, ctx, name):
        data = {
            "name" : name
        }
        characters = DB.collection("users").document(str(ctx.message.author.id)).collection("characters").stream()
        for character in characters:
            if character.id == name:
                results = "You already have a character named **" + name + "**. Use `!character load " + name + "` to switch to them."
                await ctx.send(results)
                return
        DB.collection("users").document(str(ctx.message.author.id)).collection("characters").document(name).set(data)
        DB.collection("users").document(str(ctx.message.author.id)).set({"active" : name})
        results = "Your new character, **" + name + "**, is loaded and ready to go!"
        await ctx.send(results)

    @character.command(name="load", help="Loads a character and makes them active.")
    async def load(self, ctx, name):
        characters = DB.collection("users").document(str(ctx.message.author.id)).collection("characters").stream()
        for character in characters:
            if character.id == name:
                DB.collection("users").document(str(ctx.message.author.id)).set({"active" : name})
                results = "**" + name + "** is loaded and ready to go!"
                await ctx.send(results)
                return

        results = "**" + name + "** isn't one of your characters. To create them type `!character new " + name + "`."
        await ctx.send(results)

    @character.command(name="set", help="Set a STAT or Skill to a certain level")
    async def set(self, ctx, statorskill, val):
        active = DB.collection("users").document(str(ctx.message.author.id)).get().to_dict()["active"]
        stats_stream = DB.collection("stats").stream()
        skills_stream = DB.collection("skills").stream()
        
        stats = []
        skills = []

        for stat in stats_stream:
            stats.append(stat.id) 
        for skill in skills_stream:
            skills.append(skill.id)

        if val is None or val.isnumeric() == False:
            results = "Please enter a number after the STAT or Skill. Try again."
            await ctx.send(results)
            return

        if statorskill.lower() in stats or statorskill.lower() in skills:
            character_ref = DB.collection("users").document(str(ctx.message.author.id)).collection("characters").document(active)
            character_ref.set(
                {
                   statorskill.lower() : val
                }, merge=True
            )
            
            results = "**" + active + "'s** *" + statorskill.capitalize() + "* is now set to " + str(val) + "."

        else:
            results = "\"" + statorskill + "\" isn't a STAT or Skill. Try again."
        
        await ctx.send(results)

    @character.command(name="view", help="View information about your character.")
    async def view(self, ctx):
        active = DB.collection("users").document(str(ctx.message.author.id)).get().to_dict()["active"]
        character = DB.collection("users").document(str(ctx.message.author.id)).collection("characters").document(active).get().to_dict()

        embed = discord.Embed(title=character["name"], description="Netrunner", color=0xff69b4)
        embed.set_thumbnail(url="https://i.imgur.com/cRIB0hg.jpg")
        embed.add_field(name="INT", value=character["intelligence"], inline=True)
        embed.add_field(name="REF", value=character["reflexes"], inline=True)
        embed.add_field(name="DEX", value=character["dexterity"], inline=True)
        embed.add_field(name="TECH", value=character["technique"], inline=True)
        embed.add_field(name="COOL", value=character["cool"], inline=True)
        embed.add_field(name="WILL", value=character["willpower"], inline=True)
        embed.add_field(name="LUCK", value=character["luck"], inline=True)
        embed.add_field(name="MOVE", value=character["movement"], inline=True)
        embed.add_field(name="BODY", value=character["body"], inline=True)
        embed.add_field(name="EMP", value=character["empathy"], inline=True)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Character(bot))