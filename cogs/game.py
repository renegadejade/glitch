import discord
from discord.ext import commands
from data import DB, SKILLS
import random

class Game(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=["g"], invoke_without_command=True)
    async def game(self, ctx):
        await ctx.send(f"Incorrect usage. Use `{ctx.prefix}help game` for help.")

    @game.command(name="skillcheck", aliases=["sc"], help="Rolls a skill check.")
    async def skillcheck(self, ctx, skillStr, *args):
        print(args)
        active = DB.collection("users").document(str(ctx.message.author.id)).get().to_dict()["active"]
        character = DB.collection("users").document(str(ctx.message.author.id)).collection("characters").document(active).get().to_dict()

        skill_level = 0
        stat_level = 0
        stat = ""
        skill_exists = False

        for skill in SKILLS:
            if skill["name"] == skillStr:
                stat = skill["stat"]
                skill_exists = True

        if skill_exists and skillStr in character:
            skill_level = int(character[skillStr])
            stat_level = int(character[stat])
        elif skill_exists:
            DB.collection("users").document(str(ctx.message.author.id)).collection("characters").document(active).set({skillStr:0}, merge = True)
            skill_level = 0
            stat_level = int(character[stat])
        else:
            results = "**" + skillStr + "** is not a skill. Try again."
            await ctx.send(results)
            return
        luck = 0
        if "-l" in args:
            flag_position = args.index("-l")
            luckStr = str(args[flag_position + 1])
            if luckStr.isnumeric():
                luck = int(args[flag_position + 1])
            else:
                results = "Please enter a number after the -l flag."
                await ctx.send(results)
                return
            print(luck)
        elif "--luck" in args:
            flag_position = args.index("--luck")
            luckStr = args[flag_position + 1]
            if luckStr.isnumeric():
                luck = int(args[flag_position + 1])
            else:
                results = "Please enter a number after the --luck flag."
                await ctx.send(results)
                return
        mod = 0
        if "-m" in args:
            flag_position = args.index("-m")
            modStr = str(args[flag_position + 1])
            if modStr.lstrip("-").isnumeric():
                mod = int(args[flag_position + 1])
            else:
                results = "Please enter a number after the -m flag."
                await ctx.send(results)
                return
            print(mod)
        elif "--mod" in args:
            flag_position = args.index("--mod")
            modStr = args[flag_position + 1]
            if modStr.lstrip("-").isnumeric():
                mod = int(args[flag_position + 1])
            else:
                results = "Please enter a number after the --mod flag."
                await ctx.send(results)
                return
        roll = random.randint(1,10)
        total = skill_level + stat_level + roll + luck + mod

        results = character["name"] + " rolled a " + str(roll) + " for a total result of: **" + str(total) + "**"
        results += "\n" + stat.capitalize() + ": " + str(stat_level) + "|" + skillStr.capitalize() + ": " + str(skill_level) + "|Roll: " + str(roll) + "|LUCK: " + str(luck) + "|Mod: " + str(mod)
        if roll == 10:
            crit = random.randint(1,10)
            total += crit
            results += "\n**CRITICAL**: Rolling...\nCrit Roll: " + str(crit) + "\nNew Total: **" + str(total) + "**"
        if roll == 1:
            crit = random.randint(1,10)
            total -= crit
            results += "\n**CRITICAL FAILURE**: Rolling...\nCrit Roll: " + str(crit) + "\nNew Total: **" + str(total) + "**"

        await ctx.send(results)

def setup(bot):
    bot.add_cog(Game(bot))