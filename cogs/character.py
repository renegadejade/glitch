import discord
from discord.ext import commands
from data import DB
import variables



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
            if character.to_dict()["name"] == name:
                results = "You already have a character named **" + name + "**. Use `!character load " + name + "` to switch to them."
                await ctx.send(results)
                return
        DB.collection("users").document(str(ctx.message.author.id)).collection("characters").add(data)
        character_id = ""
        for character in characters:
            if character.to_dict()["name"] == name:
                character_id = character.id
        DB.collection("users").document(str(ctx.message.author.id)).set({"active" : character_id})
        results = "Your new character, **" + name + "** is loaded and ready to go!"
        await ctx.send(results)

    @character.command(name="load", help="Loads a character and makes them active.")
    async def load(self, ctx, name):
        characters = DB.collection("users").document(str(ctx.message.author.id)).collection("characters").stream()
        character_id = ""
        for character in characters:
            if character.to_dict()["name"] == name:
                character_id = character.id
                DB.collection("users").document(str(ctx.message.author.id)).set({"active" : character_id})
                results = "**" + name + "** is loaded and ready to go!"
                await ctx.send(results)
                return

        results = "**" + name + "** isn't one of your characters. To create them type `!character new " + name + "`."
        await ctx.send(results)
        
        

    # @character.command(name="name", help="Set your character's name")
    # async def name(self, ctx, name):
    #     data = {
    #         "name" : name
    #     }
    #     DB.collection("users").document(str(ctx.message.author.id)).set(data, merge=True)
    #     results = "Your character's new name is " + name + "."
    #     await ctx.send(results)

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

        print(stats)
        if statorskill.lower() in stats or skills and int(val) is not None:
            character_ref = DB.collection("users").document(str(ctx.message.author.id)).collection("characters").document(active)
            character_ref.set(
                {
                    statorskill.lower() : val
                }, merge=True
            )
            character = character_ref.get()
            results = character.to_dict()["name"]+ "'s " + statorskill.capitalize() + " is now set to " + str(val)
        else:
            results = "\"" + statorskill + "\" isn't a STAT or Skill. Try again."
        
        await ctx.send(results)


def setup(bot):
    bot.add_cog(Character(bot))