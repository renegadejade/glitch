"""
The main script for running Glitch
"""

import os
import random
from os.path import dirname, join

import d20
import discord
from discord.ext import commands
from dotenv import load_dotenv

from night_market import generate_night_market

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
TOKEN = os.getenv('DISCORD_TOKEN')
COMMAND_PREFIX = "!"
random.seed()

bot = commands.Bot(command_prefix=COMMAND_PREFIX)


@bot.event
async def on_ready():
	"""
	Prints a message to the console to show that the bot is ready.
	"""
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('------')
	await bot.change_presence(status=discord.Status.online, activity=discord.Game("Cyberpunk RED"))


@bot.event
async def on_command_error(ctx, error):
	"""
	Reports an error in the usage of the bot.
	:param ctx: The Discord Commands Context.
	:type ctx: discord.ext.commands.context.Context
	:param error: The error to report.
	:type error: discord.ext.commands.errors.DiscordException
	"""
	results = "**There was an error while invoking the command.**\n**Debug**: "
	results += str(error)
	await ctx.send(results)


@bot.command()
async def about(ctx):
	"""
	Displays the about information for the bot.
	:param ctx: The Discord Commands Context.
	:type ctx: discord.ext.commands.context.Context
	"""
	embed = discord.Embed(title="Glitch", description="A Discord bot for playing Cyberpunk RED", color=0x2c84fa)
	embed.set_thumbnail(url="https://i.imgur.com/cRIB0hg.jpg")
	embed.add_field(name="Original Developer", value="John 'JT' Thomas", inline=False)
	embed.add_field(name="Current Developer", value="Frank Pasqualini", inline=False)
	embed.add_field(name="Documentation", value="https://glitch.red/", inline=False)
	embed.add_field(name="GitHub", value="https://github.com/frank-pasqualini/glitch/", inline=False)
	embed.set_footer(text="The bot and its authors are not affiliated with nor endorsed by R. Talsorian Games.")
	await ctx.send(embed=embed)


@bot.command(aliases=["market", "nm"], help="Randomly generates a Night Market")
async def night_market(ctx):
	"""
	Randomly generates a Night Market.
	:param manual: Whether to manually fill in options or not.
	:type manual: bool
	:param ctx: The Discord Commands Context.
	:type ctx: discord.ext.commands.context.Context
	"""
	market, rolls = generate_night_market()
	out = "This market is selling " + str(' '.join(word.title() for word in rolls[0].__name__.split('_'))) + " and " + str(' '.join(word.title() for word in rolls[1].__name__.split('_')) + "\n")
	out += "```\n"

	max_length_column = (max(len(element[0]) + 2 for element in market))
	i = 0
	for ele1, ele2 in market:
		fmt = "{:<" + str(max_length_column) + "}{}"
		out += fmt.format(ele1, ele2) + "\n"
		i += 1
		if i == 10:
			out += "```"
			await ctx.send(out)
			i = 0
			out = "```\n"
	out += "```"
	await ctx.send(out)


@bot.command(aliases=["r"], help="Rolls the amount of type of dice specified. Ex: 1d10, 5d6")
async def roll(ctx, roll_str):
	"""
	Rolls the amount of type of dice specified.
	:param ctx: The Discord Commands Context.
	:type ctx: discord.ext.commands.context.Context
	:param roll_str: The number and type of dice to roll.
	:type roll_str: str
	"""
	results = d20.roll(roll_str)
	await ctx.send(results)


# bot.load_extension("cogs.character")
# bot.load_extension("cogs.game")
bot.run(TOKEN)
