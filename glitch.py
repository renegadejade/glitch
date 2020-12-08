import os
from os.path import join, dirname
from dotenv import load_dotenv
import discord
from discord.ext import commands
import random
import math
import re
import json


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
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Cyberpunk RED | " + COMMAND_PREFIX + "help"))

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command(aliases=["market", "nm"])
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



bot.run(TOKEN)
