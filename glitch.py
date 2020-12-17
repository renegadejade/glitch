import os
from data import DB
from os.path import join, dirname
from dotenv import load_dotenv
import discord
from discord.ext import commands
import random
import math
import re
import json
import d20
import cogs.character
import variables


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
TOKEN = os.getenv('DISCORD_TOKEN')
COMMAND_PREFIX = "!"

bot = commands.Bot(command_prefix=COMMAND_PREFIX)
NM_TYPES = ["Ammunition", "Armor", "Cyberdeck Hardware", "Cyberware", "Exotic Weapons", "Gear", "Melee Weapons", "Programs", "Ranged Weapons", "Street Drugs", "Weapon Attachments"]


# NM_TYPES = ["ammunition", "armor", "cyberdeck_hardware", "cyberware", "exoticweapons", "gear", "melee_weapons", "programs", "ranged_weapons", "street_drugs", "weapon_attachments"]
AMMUNITION = []
ARMOR = []
CYBERDECK_HARDWARE = []
CYBERWARE= []
EXOTIC_WEAPONS = []
GEAR = []
MELEE_WEAPONS = []
PROGRAMS = []
RANGED_WEAPONS = []
STREET_DRUGS = []
WEAPON_ATTACHMENTS = []

with open("nightmarket/glitch/ammunition.json") as json_file:
        AMMUNITION = json.load(json_file)
with open("nightmarket/glitch/armor.json") as json_file:
        ARMOR = json.load(json_file)
with open("nightmarket/glitch/cyberdeckhardware.json") as json_file:
        CYBERDECK_HARDWARE = json.load(json_file) 
with open("nightmarket/glitch/cyberware.json") as json_file:
        CYBERWARE = json.load(json_file)       
with open("nightmarket/glitch/exoticweapons.json") as json_file:
        EXOTIC_WEAPONS = json.load(json_file)  
with open("nightmarket/glitch/gear.json") as json_file:
        GEAR = json.load(json_file)
with open("nightmarket/glitch/meleeweapons.json") as json_file:
        MELEE_WEAPONS = json.load(json_file)    
with open("nightmarket/glitch/programs.json") as json_file:
        PROGRAMS = json.load(json_file)
with open("nightmarket/glitch/rangedweapons.json") as json_file:
        RANGED_WEAPONS = json.load(json_file)
with open("nightmarket/glitch/streetdrugs.json") as json_file:
        STREET_DRUGS = json.load(json_file)
with open("nightmarket/glitch/weaponattachments.json") as json_file:
        WEAPON_ATTACHMENTS = json.load(json_file)        
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Cyberpunk RED"))

@bot.event
async def on_command_error(ctx, error):
    results = "**There was an error while invoking the command.**\n**Debug**: "
    results += str(error)
    await ctx.send(results)

@bot.command()
async def ping(ctx):
    await ctx.send("pong")

@bot.command()
async def about(ctx):
    embed = discord.Embed(title="Glitch", description="A Discord bot for playing Cyberpunk RED", color=0xff69b4)
    embed.set_thumbnail(url="https://i.imgur.com/cRIB0hg.jpg")
    embed.add_field(name="Developer", value="John 'JT' Thomas", inline=False)
    embed.add_field(name="Documentation", value="https://glitch.red/", inline=False)
    embed.add_field(name="GitHub", value="https://github.com/zensomancer/glitch/", inline=False)
    embed.set_footer(text="The bot and its author are not affiliated with nor endorsed by R. Talsorian Games.")
    await ctx.send(embed=embed)

@bot.command(aliases=["market", "nm"], help="Randomly generates a Night Market | pass -g or -c for different generators")
async def nightmarket(ctx, command):
    if command == "-c":
        forsale = []
        types = random.sample(NM_TYPES, 2)
        types.sort()
        if "Ammunition" in types:
            forsale.append(random.sample(AMMUNITION, random.randint(1,5)))
        if "Armor" in types:
            forsale.append(random.sample(ARMOR, random.randint(1,5)))
        if "Cyberdeck Hardware" in types:
            forsale.append(random.sample(CYBERDECK_HARDWARE, random.randint(1,5)))
        if "Cyberware" in types:
            forsale.append(random.sample(CYBERWARE, random.randint(1,5)))
        if "Exotic Weapons" in types:
            forsale.append(random.sample(EXOTIC_WEAPONS, random.randint(1,5)))
        if "Gear" in types:
            forsale.append(random.sample(GEAR, random.randint(1,5)))
        if "Melee Weapons" in types:
            forsale.append(random.sample(MELEE_WEAPONS, random.randint(1,5)))
        if "Programs" in types:
            forsale.append(random.sample(PROGRAMS, random.randint(1,5)))
        if "Ranged Weapons" in types:
            forsale.append(random.sample(RANGED_WEAPONS, random.randint(1,5)))
        if "Street Drugs" in types:
            forsale.append(random.sample(STREET_DRUGS, random.randint(1,5)))
        if "Weapon Attachments" in types:
            forsale.append(random.sample(WEAPON_ATTACHMENTS, random.randint(1,5)))
        print(forsale)
        forsalestr = ""
        for item in forsale[0]:
            forsalestr += item["name"] + " - " + item["cost"] + "eb\n"
        forsalestr += "-----\n"
        for item in forsale[1]:
            forsalestr += item["name"] + " - " + item["cost"] + "eb\n"
        results = ":heavy_dollar_sign::heavy_dollar_sign::heavy_dollar_sign:**FOR SALE TONIGHT**:heavy_dollar_sign::heavy_dollar_sign::heavy_dollar_sign:\n"
        results += "**" + types[0] + "** & **" + types[1] + "**\n-----\n"
        results += forsalestr
        print(results)
        await ctx.send(results)
    elif command == "-g":
        with open("nightmarket/generic/generic.json") as json_file:
            data = json.load(json_file)
            nm = random.sample(data, 2)
            print(str(nm[0]["type"]) + " " + str(nm[1]["type"]))
            k1 = random.randint(1,5)
            k2 = random.randint(1,5)
            forsale = random.sample(nm[0]["shelves"], k1)
            for goods in random.sample(nm[1]["shelves"], k2):
                forsale.append(goods)
            print(str(forsale))
            forsale.sort()
            forsalestr = "\n".join(forsale)
            print(forsalestr)
            results = "This night market sells **" + str(nm[0]["type"]) + " and " + str(nm[1]["type"] + "**")
            results += "\nIt's current offerings are: \n" + forsalestr
            await ctx.send(results)

@bot.command()
async def view(ctx):
    user_ref = DB.collection("users").document(str(ctx.message.author.id))
    user = user_ref.get()
    stats = ""
    stats += "INT:" + user.to_dict()["int"] + "|"
    stats += "REF:" + user.to_dict()["ref"] + "|"
    stats += "DEX:" + user.to_dict()["dex"] + "|"
    stats += "TECH:" + user.to_dict()["tech"] + "|"
    stats += "COOL:" + user.to_dict()["cool"] + "|"
    stats += "WILL:" + user.to_dict()["will"] + "|"
    stats += "LUCK:" + user.to_dict()["luck"] + "|"
    stats += "MOVE:" + user.to_dict()["move"] + "|"
    stats += "BODY:" + user.to_dict()["body"] + "|"
    stats += "EMP:" + user.to_dict()["emp"]

    embed = discord.Embed(title=user.to_dict()["name"], color=0xff69b4)
    # embed.add_field(name="INT", value=user.to_dict()["intelligence"], inline=True)
    # embed.add_field(name="REF", value=user.to_dict()["reflexes"], inline=True)
    # embed.add_field(name="DEX", value=user.to_dict()["dexterity"], inline=True)
    # embed.add_field(name="TECH", value=user.to_dict()["technique"], inline=True)
    # embed.add_field(name="COOL", value=user.to_dict()["cool"], inline=True)
    # embed.add_field(name="WILL", value=user.to_dict()["willpower"], inline=True)
    # embed.add_field(name="LUCK", value=user.to_dict()["luck"], inline=True)
    # embed.add_field(name="MOVE", value=user.to_dict()["movement"], inline=True)
    # embed.add_field(name="BODY", value=user.to_dict()["body"], inline=True)
    # embed.add_field(name="EMP", value=user.to_dict()["empathy"], inline=True)
    embed.add_field(name="STATS", value=stats, inline=True)
    await ctx.send(embed=embed)

@bot.command(aliases=["sc"])
async def skillcheck(ctx, skill):
    char_ref = DB.collection("users").document(str(ctx.message.author.id))
    char = char_ref.get()
    skill_level = 0
    stat_level = 0
    stat = ""
    if skill.lower() in char.to_dict() and variables.SKILLS:
        skill_level = skill_level = int(char.to_dict()[skill])
    elif skill.lower() in variables.SKILLS:
        char_ref.set(
            {
                skill : "0"
            }, merge=True
        )
    else:
        await ctx.send("That's not a skill. Try again.")
        return
    if skill.lower() in variables.SKILLS: 
        if skill.lower() in variables.WILL_SKILLS:
            stat = "WILL"
            stat_level = int(char.to_dict()["will"])
        if skill.lower() in variables.INT_SKILLS:
            stat = "INT"
            stat_level = int(char.to_dict()["int"])
        if skill.lower() in variables.REF_SKILLS:
            stat = "REF"
            stat_level = int(char.to_dict()["ref"])
        if skill.lower() in variables.DEX_SKILLS:
            stat = "DEX"
            stat_level = int(char.to_dict()["dex"])
        if skill.lower() in variables.TECH_SKILLS:
            stat = "TECH"
            stat_level = int(char.to_dict()["tech"])
        if skill.lower() in variables.COOL_SKILLS:
            stat = "COOL"
            stat_level = int(char.to_dict()["cool"])
        if skill.lower() in variables.EMP_SKILLS:
            stat = "EMP"
            stat_level = int(char.to_dict()["emp"])
    roll = random.randint(1,10)
    total = skill_level + stat_level + roll
    results = char.to_dict()["name"] + " rolled a " + str(roll) + " for a total result of: **" + str(total) + "**"
    results += "\n" + stat + ": " + str(stat_level) + "|" + skill.capitalize() + ": " + str(skill_level) + "|Roll: " + str(roll)
    if roll == 10:
        crit = random.randint(1,10)
        total += crit
        results += "\n**CRITICAL**: Rolling...\nCrit Roll: " + str(crit) + "\nNew Total: **" + str(total) + "**"
    if roll == 1:
        crit = random.randint(1,10)
        total -= crit
        results += "\n**CRITICAL FAILURE**: Rolling...\nCrit Roll: " + str(crit) + "\nNew Total: **" + str(total) + "**"

    await ctx.send(results)

@bot.command(aliases=["r"])
async def roll(ctx, rollStr):
    results = d20.roll(rollStr)
    await ctx.send(results)

bot.load_extension("cogs.character")
bot.run(TOKEN)
