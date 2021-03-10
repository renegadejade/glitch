"""
TODO
"""

import random

from discord.ext import commands

from data import DB, SKILLS


class Game(commands.Cog):
    """
    TODO
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=["g"], invoke_without_command=True)
    async def game(self, ctx):
        """
        TODO
        :param ctx:
        :type ctx:
        """
        await ctx.send(f"Incorrect usage. Use `{ctx.prefix}help game` for help.")

    @game.command(name="skill_check", aliases=["sc"], help="Rolls a skill check.")
    async def skill_check(self, ctx, skill_str, *args):
        """
        TODO
        :param ctx:
        :type ctx:
        :param skill_str:
        :type skill_str:
        :param args:
        :type args:
        :return:
        :rtype:
        """
        print(args)
        active = DB.collection("users").document(
            str(ctx.message.author.id)).get().to_dict()["active"]
        character = DB.collection("users").document(str(ctx.message.author.id)).collection(
            "characters").document(active).get().to_dict()

        stat = ""
        skill_exists = False

        for skill in SKILLS:
            if skill["name"] == skill_str:
                stat = skill["stat"]
                skill_exists = True

        if skill_exists and skill_str in character:
            skill_level = int(character[skill_str])
            stat_level = int(character[stat])
        elif skill_exists:
            DB.collection("users").document(str(ctx.message.author.id)).collection(
                "characters").document(active).set({skill_str: 0}, merge=True)
            skill_level = 0
            stat_level = int(character[stat])
        else:
            results = "**" + skill_str + "** is not a skill. Try again."
            await ctx.send(results)
            return
        luck = 0
        if "-l" in args:
            flag_position = args.index("-l")
            luck_str = str(args[flag_position + 1])
            if luck_str.isnumeric():
                luck = int(args[flag_position + 1])
            else:
                results = "Please enter a number after the -l flag."
                await ctx.send(results)
                return
            print(luck)
        elif "--luck" in args:
            flag_position = args.index("--luck")
            luck_str = args[flag_position + 1]
            if luck_str.isnumeric():
                luck = int(args[flag_position + 1])
            else:
                results = "Please enter a number after the --luck flag."
                await ctx.send(results)
                return
        mod = 0
        if "-m" in args:
            flag_position = args.index("-m")
            mod_str = str(args[flag_position + 1])
            if mod_str.lstrip("-").isnumeric():
                mod = int(args[flag_position + 1])
            else:
                results = "Please enter a number after the -m flag."
                await ctx.send(results)
                return
            print(mod)
        elif "--mod" in args:
            flag_position = args.index("--mod")
            mod_str = args[flag_position + 1]
            if mod_str.lstrip("-").isnumeric():
                mod = int(args[flag_position + 1])
            else:
                results = "Please enter a number after the --mod flag."
                await ctx.send(results)
                return
        roll = random.randint(1, 10)
        total = skill_level + stat_level + roll + luck + mod

        results = character["name"] + " rolled a " + \
            str(roll) + " for a total result of: **" + str(total) + "**"
        results += "\n" + stat.capitalize() + ": " + str(stat_level) + "|" + skill_str.capitalize() + \
            ": " + str(skill_level) + "|Roll: " + str(roll) + \
            "|LUCK: " + str(luck) + "|Mod: " + str(mod)
        if roll == 10:
            crit = random.randint(1, 10)
            total += crit
            results += "\n**CRITICAL**: Rolling...\nCrit Roll: " + \
                str(crit) + "\nNew Total: **" + str(total) + "**"
        if roll == 1:
            crit = random.randint(1, 10)
            total -= crit
            results += "\n**CRITICAL FAILURE**: Rolling...\nCrit Roll: " + \
                str(crit) + "\nNew Total: **" + str(total) + "**"

        await ctx.send(results)


def setup(bot):
    """
    TODO
    :param bot:
    :type bot:
    """
    bot.add_cog(Game(bot))
