"""
The main script for running Glitch
"""

import json
import os
import random
from os.path import dirname, join

import d20
import discord
from discord.ext import commands
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
TOKEN = os.getenv('DISCORD_TOKEN')
COMMAND_PREFIX = "!"
random.seed()

bot = commands.Bot(command_prefix=COMMAND_PREFIX)
NM_TYPES = ["Ammunition", "Armor", "Cyberdeck Hardware", "Cyberware", "Exotic Weapons", "Gear", "Melee Weapons", "Programs", "Ranged Weapons", "Street Drugs", "Weapon Attachments"]


# with open("night_market/ammunition.json") as json_file:
# 	AMMUNITION = json.load(json_file)
# with open("night_market/armor.json") as json_file:
# 	ARMOR = json.load(json_file)
# with open("night_market/cyberdeck_hardware.json") as json_file:
# 	CYBERDECK_HARDWARE = json.load(json_file)
# with open("night_market/cyberware.json") as json_file:
# 	CYBERWARE = json.load(json_file)
# with open("night_market/exotic_weapons.json") as json_file:
# 	EXOTIC_WEAPONS = json.load(json_file)
# with open("night_market/gear.json") as json_file:
# 	GEAR = json.load(json_file)
# with open("night_market/melee_weapons.json") as json_file:
# 	MELEE_WEAPONS = json.load(json_file)
# with open("night_market/programs.json") as json_file:
# 	PROGRAMS = json.load(json_file)
# with open("night_market/ranged_weapons.json") as json_file:
# 	RANGED_WEAPONS = json.load(json_file)
# with open("night_market/street_drugs.json") as json_file:
# 	STREET_DRUGS = json.load(json_file)
# with open("night_market/weapon_attachments.json") as json_file:
# 	WEAPON_ATTACHMENTS = json.load(json_file)


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
	:param ctx: The Discord Commands Context.
	:type ctx: discord.ext.commands.context.Context
	"""

	# if command == "-c":
	# 	for_sale = []
	# 	types = random.sample(NM_TYPES, 2)
	# 	types.sort()
	# 	if "Ammunition" in types:
	# 		for_sale.append(random.sample(AMMUNITION, random.randint(1, 5)))
	# 	if "Armor" in types:
	# 		for_sale.append(random.sample(ARMOR, random.randint(1, 5)))
	# 	if "Cyberdeck Hardware" in types:
	# 		for_sale.append(random.sample(CYBERDECK_HARDWARE, random.randint(1, 5)))
	# 	if "Cyberware" in types:
	# 		for_sale.append(random.sample(CYBERWARE, random.randint(1, 5)))
	# 	if "Exotic Weapons" in types:
	# 		for_sale.append(random.sample(EXOTIC_WEAPONS, random.randint(1, 5)))
	# 	if "Gear" in types:
	# 		for_sale.append(random.sample(GEAR, random.randint(1, 5)))
	# 	if "Melee Weapons" in types:
	# 		for_sale.append(random.sample(MELEE_WEAPONS, random.randint(1, 5)))
	# 	if "Programs" in types:
	# 		for_sale.append(random.sample(PROGRAMS, random.randint(1, 5)))
	# 	if "Ranged Weapons" in types:
	# 		for_sale.append(random.sample(RANGED_WEAPONS, random.randint(1, 5)))
	# 	if "Street Drugs" in types:
	# 		for_sale.append(random.sample(STREET_DRUGS, random.randint(1, 5)))
	# 	if "Weapon Attachments" in types:
	# 		for_sale.append(random.sample(WEAPON_ATTACHMENTS, random.randint(1, 5)))
	# 	print(for_sale)
	# 	for_scale_str = ""
	# 	for item in for_sale[0]:
	# 		for_scale_str += item["name"] + " - " + item["cost"] + "eb\n"
	# 	for_scale_str += "-----\n"
	# 	for item in for_sale[1]:
	# 		for_scale_str += item["name"] + " - " + item["cost"] + "eb\n"
	# 	results = ":heavy_dollar_sign::heavy_dollar_sign::heavy_dollar_sign:**FOR SALE TONIGHT**:heavy_dollar_sign::heavy_dollar_sign::heavy_dollar_sign:\n"
	# 	results += "**" + types[0] + "** & **" + types[1] + "**\n-----\n"
	# 	results += for_scale_str
	# 	print(results)
	# 	await ctx.send(results)
	with open("night_market/generic.json") as generic_file:
		data = json.load(generic_file)
		market_types = random.sample(data, 2)
		amount_1 = random.randint(1, 10)
		amount_2 = random.randint(1, 10)

		for_sale = random.sample(market_types[0]["shelves"], amount_1)
		for goods in random.sample(market_types[1]["shelves"], amount_2):
			for_sale.append(goods)

		for_sale.sort()
		for_scale_str = "\n".join(for_sale)

		results = "This night market sells **" + str(market_types[0]["type"]) + " and " + str(market_types[1]["type"] + "**") + "\nIt's current offerings are: \n" + for_scale_str
		await ctx.send(results)


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
