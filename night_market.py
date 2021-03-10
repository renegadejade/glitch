"""
Generates Night Market Outputs
"""
import json
import operator
import random

from itertools import chain


def read_json(filename, relate, cost, subtype=None):
	"""
	Reads in the contents of a json file to use.
	:param filename: The name of the file to read in.
	:type filename: str
	:param relate: The operator function to compare with.
	:type relate: Any
	:param cost: The cost to compare against.
	:type cost: int
	:return: The items from the json file that match the specifications.
	:rtype: list
	:param subtype: The subtype of the item to search for
	:type subtype: str
	"""
	with open("night_market/" + filename + ".json") as json_file:
		item_list = json.load(json_file)
		if subtype:
			return [(i["name"], i["cost"]) for i in item_list if (relate(int(i["cost"]), cost)) and (i["type"] == subtype)]
		return [(i["name"], i["cost"]) for i in item_list if relate(int(i["cost"]), cost)]


def generate_night_market():
	"""
	Rolls 2 separate numbers on a D6 and appends the items from that category to the market list.
	:return: A list containing the Night Market Selection.
	:rtype: list
	"""
	def food_and_drugs(fad_roll):
		"""
		Returns up to 10 food and drug items.
		:param fad_roll: The Roll of a d10.
		:type fad_roll: int
		:return: A list containing this category's items.
		:rtype: list
		"""

		fad_switcher = {
			1:  [("Canned Goods", 10)],
			2:  [("Packaged Goods", 10)],
			3:  [("Frozen Goods", 10)],
			4:  [("Bags of Grain", 20)],
			5:  [("Kibble Pack", 10)],
			6:  [("Bags of Prepak", 20)],
			7:  read_json("street_drugs", operator.le, 20),
			8:  [("Poor Quality Alcohol", 10)],
			9:  [("Alcohol", 20)],
			10: [("Excellent Quality Alcohol", 100)],
			11: [("MRE", 10)],
			12: [("Live Chicken", 50)],
			13: [("Live Fish", 50)],
			14: [("Fresh Fruits", 50)],
			15: [("Fresh Vegetables", 50)],
			16: [("Root Vegetables", 20)],
			17: [("Live Pigs", 100)],
			18: [("Exotic Fruits", 100)],
			19: [("Exotic Vegetables", 100)],
			20: read_json("street_drugs", operator.eq, 50)
		}

		return list(chain.from_iterable(random.sample(list(fad_switcher.values()), fad_roll)))

	def personal_electronics(pe_roll):
		"""
		Returns up to 10 personal electronics items.
		:param pe_roll: The Roll of a d10.
		:type pe_roll: int
		:return: A list containing this category's items.
		:rtype: list
		"""

		pe_switcher = {
			1:  [("Agent", 100)],
			2:  read_json("programs_hardware", operator.le, 100),
			3:  [("Audio Recorder", 100)],
			4:  [("Bug Detector", 500)],
			5:  [("Chemical Analyzer", 1000)],
			6:  [("Computer", 50)],
			7:  [("Poor Quality Cyberdeck", 100), ("Cyberdeck", 500), ("Excellent Quality Cyberdeck", 1000)],
			8:  [("Disposable Cell Phone", 50)],
			9:  [("Instrument", 500)],
			10: read_json("programs_hardware", operator.eq, 500),
			11: [("Medscanner", 1000)],
			12: [("Homing Tracer", 500)],
			13: [("Radio Communicator", 100)],
			14: [("Techscanner", 1000)],
			15: [("Smart Glasses", 500)],
			16: [("Radar Detector", 500)],
			17: [("Scrambler/ Descrambler", 500)],
			18: [("Radio Scanner/ Music Player", 50)],
			19: [("Braindance Viewer", 1000)],
			20: [("Virtuality Goggles", 100)]
		}

		return list(chain.from_iterable(random.sample(list(pe_switcher.values()), pe_roll)))

	def weapons_and_armor(waa_roll):
		"""
		Returns up to 10 weapons or armor.
		:param waa_roll: The Roll of a d10.
		:type waa_roll: int
		:return: A list containing this category's items.
		:rtype: list
		"""

		waa_switcher = {
			1:  [("Medium Pistol", 50), ("Poor Quality Medium Pistol", 20), ("Excellent Quality Pistol", 100)],
			2:  [("Heavy Pistol", 100), ("Poor Quality Heavy Pistol", 50), ("Excellent Quality Heavy Pistol", 500), ("Very Heavy Pistol", 100), ("Poor Quality Very Heavy Pistol", 50), ("Excellent Quality Very Heavy Pistol", 500)],
			3:  [("SMG", 100), ("Poor Quality SMG", 50), ("Excellent Quality SMG", 500)],
			4:  [("Heavy SMG", 100), ("Poor Quality Heavy SMG", 50), ("Excellent Quality Heavy SMG", 500)],
			5:  [("Shotgun", 500), ("Poor Quality Shotgun", 100), ("Excellent Quality Shotgun", 1000)],
			6:  [("Assault Rifle", 500), ("Poor Quality Assault Rifle", 100), ("Excellent Quality Assault Rifle", 1000)],
			7:  [("Sniper Rifle", 500), ("Poor Quality Sniper Rifle", 100), ("Excellent Quality Sniper Rifle", 1000)],
			8:  [("Bow", 100), ("Poor Quality Bow", 50), ("Excellent Quality Bow", 500), ("Crossbow", 100), ("Poor Quality Crossbow", 50), ("Excellent Quality Crossbow", 500)],
			9:  [("Grenade Launcher", 500), ("Poor Quality Grenade Launcher", 100), ("Excellent Quality Grenade Launcher", 1000), ("Rocket Launcher", 500), ("Poor Quality Rocket Launcher", 100), ("Excellent Quality Rocket Launcher", 1000)],
			10: read_json("ammunition", operator.le, 500),
			11: random.sample(read_json("exotic_weapons", operator.ge, 0), 1),
			12: [("Light Melee Weapon", 50), ("Poor Quality Light Melee Weapon", 20), ("High Quality Light Melee Weapon", 100)],
			13: [("Medium Melee Weapon", 50), ("Poor Quality Medium Melee Weapon", 20), ("High Quality Medium Melee Weapon", 100)],
			14: [("Heavy Melee Weapon", 100), ("Poor Quality Heavy Melee Weapon", 50), ("High Quality Heavy Melee Weapon", 500)],
			15: [("Very Heavy Melee Weapon", 100), ("Poor Quality Very Heavy Melee Weapon", 50), ("Excellent Quality Very Heavy Melee Weapon", 500)],
			16: read_json("armor", operator.le, 100),
			17: read_json("armor", operator.eq, 500),
			18: read_json("armor", operator.eq, 1000),
			19: read_json("weapon_attachments", operator.le, 100),
			20: read_json("weapon_attachments", operator.ge, 500),
		}

		return list(chain.from_iterable(random.sample(list(waa_switcher.values()), waa_roll)))

	def cyberware(cw_roll):
		"""
		Returns up to 10 items from this category.
		:param cw_roll: The Roll of a d10.
		:type cw_roll: int
		:return: A list containing this category's items.
		:rtype: list
		"""

		cw_switcher = {
			1:  [("Cybereye", 100)],
			2:  [("Cyberaudio Suite", 500)],
			3:  [("Neural Link", 500)],
			4:  [("Cyberarm", 500)],
			5:  [("Cyberleg", 100)],
			6:  read_json("cyberware", operator.eq, 1000, "External"),
			7:  read_json("cyberware", operator.le, 500, "External"),
			8:  read_json("cyberware", operator.eq, 1000, "Internal"),
			9:  read_json("cyberware", operator.le, 500, "Internal"),
			10: [("Cybereye", 100)] + read_json("cyberware", operator.eq, 1000, "Cyberoptics"),
			11: [("Cybereye", 100)] + read_json("cyberware", operator.le, 500, "Cyberoptics"),
			12: [("Cyberaudio Suite", 500)] + read_json("cyberware", operator.eq, 1000, "Cyberaudio"),
			13: [("Cyberaudio Suite", 500)] + read_json("cyberware", operator.le, 500, "Cyberaudio"),
			14: [("Neural Link", 500), ("Chipware Socket", 500)] + read_json("cyberware", operator.eq, 1000, "Neuralware"),
			15: [("Neural Link", 500), ("Chipware Socket", 500)] + read_json("cyberware", operator.eq, 1000, "Neuralware"),
			16: [("Cyberarm", 500), ("Cyberleg", 500)] + read_json("cyberware", operator.eq, 1000, "Cyberlimbs"),
			17: [("Cyberarm", 500), ("Cyberleg", 500)] + read_json("cyberware", operator.le, 500, "Cyberlimbs"),
			18: read_json("cyberware", operator.ge, 0, "Fashionware"),
			19: read_json("cyberware", operator.ge, 0, "Borgware"),
			20: read_json("cyberware", operator.ge, 0),
		}

		return list(chain.from_iterable(random.sample(list(cw_switcher.values()), cw_roll)))

	def clothing_and_fashionware(caf_roll):
		"""
		Returns up to 10 fashion items.
		:param caf_roll: The Roll of a d10.
		:type caf_roll: int
		:return: A list containing this category's items.
		:rtype: list
		"""
		caf_switcher = {
			1:  read_json("fashion", operator.ge, 0, "Bag Lady Chic"),
			2:  read_json("fashion", operator.ge, 0, "Gang Colors"),
			3:  read_json("fashion", operator.ge, 0, "Generic Chic"),
			4:  read_json("fashion", operator.ge, 0, "Bohemian"),
			5:  read_json("fashion", operator.ge, 0, "Leisurewear"),
			6:  read_json("fashion", operator.ge, 0, "Nomad Leathers"),
			7:  read_json("fashion", operator.ge, 0, "Asia Pop"),
			8:  read_json("fashion", operator.ge, 0, "Urban Flash"),
			9:  read_json("fashion", operator.ge, 0, "Businesswear"),
			10: read_json("fashion", operator.ge, 0, "High Fashion"),

			18: read_json("fashion", operator.ge, 0, "Generic Chic"),
			19: read_json("fashion", operator.ge, 0, "Leisurewear"),
			20: read_json("fashion", operator.ge, 0, "Gang Colors"),
		}

		return list(chain.from_iterable(random.sample(list(caf_switcher.values()), caf_roll)))

	def survival_gear(sg_roll):
		"""
		Returns up to 10 survival items.
		:param sg_roll: The Roll of a d10.
		:type sg_roll: int
		:return: A list containing this category's items.
		:rtype: list
		"""
		sg_switcher = {
			1:  [("Anti-Smog Breathing Mask", 20)],
			2:  [("Auto Level Dampening Ear Protectors", 1000)],
			3:  [("Binoculars", 50)],
			4:  [("Carryall", 20)],
			5:  [("Flashlight", 20)],
			6:  [("Duct Tape", 20)],
			7:  [("Inflatable Bed & Sleep-bag", 20)],
			8:  [("Lock Picking Set", 20)],
			9:  [("Handcuffs", 50)],
			10: [("Medtech Bag", 100)],
			11: [("Tent and Camping Equipment", 50)],
			12: [("Rope (60m/yds)", 20)],
			13: [("Techtool", 100)],
			14: [("Personal CarePak", 20)],
			15: [("Radiation Suit", 1000)],
			16: [("Road Flare", 10)],
			17: [("Grapple Gun", 100)],
			18: [("Tech Bag", 500)],
			19: [("Shovel or Axe", 50)],
			20: [("Airhypo", 50)]
		}

		return list(chain.from_iterable(random.sample(list(sg_switcher.values()), sg_roll)))

	# Select 2 unique categories and pick 1-10 items from them
	roll = random.sample([food_and_drugs, personal_electronics, weapons_and_armor, cyberware, clothing_and_fashionware, survival_gear], 2)
	market = roll[0](random.randint(1, 11)) + roll[1](random.randint(1, 11))

	# Deduplicate the list, sort by name, and then sort by price
	market = list(set(market))
	market.sort()
	market.sort(key=lambda x: x[1])
	return market, roll
