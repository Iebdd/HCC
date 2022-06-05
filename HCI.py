import os
import sys
import requests
import datetime
import shutil
import argparse
import utils
# from tkinter import *
from contextlib import suppress
from datetime import datetime
import re

URL = 'https://universalis.app/api/v2/' #Universalis URL to get item prices
XIVDB = 'https://xivapi.com/item/'		#XIVDB data to, in theory, get item names
postamble = '?hq=True'

Worlds = [[['lich', 'odin', 'phoenix', 'shiva', 'twintania', 'zodiark'], ['cerberus', 'louisoix', 'moogle', 'omega', 'ragnarok', 'spriggan'], ['aegis', 'atomos', 'carbuncle', 'garuda', 'gungnir', 'kujata', 'ramuh', 'tonberry', 'typhon', 'unicorn'], ['alexander', 'bahamut', 'durandal', 'fenrir', 'ifrit', 'ridill', 'tiamat', 'ultima', 'valefor', 'yojimbo', 'zeromus'], ['anima', 'asura', 'belias', 'chocobo', 'hades', 'ixion', 'mandragora', 'masamune', 'pandaemonium', 'shinryu', 'titan'], ['adamantoise', 'cactuar', 'faerie', 'gilgamesh', 'jenova', 'midgardsomr', 'sargatanas', 'siren'], ['behemoth', 'excalibur', 'exodus', 'famfrit', 'hyperion', 'lamia', 'leviathan', 'ultros'], ['balmung', 'brynhildr', 'coeurl', 'diabolos', 'goblin', 'marlboro', 'mateus', 'zalera'], ['bismarck', 'ravana', 'sephirot', 'sophia', 'zurvan']], [['light'], ['chaos'], ['elemental'], ['gaia'], ['mana'], ['aether'], ['primal'], ['crystal'], ['materia']]]
#The ingame ids of the items to be requested. Ordered according to the occurence in the job window
id_weapon = [35020, 35039, 35022, 35026, 35035, 35028, 35031, 35032, 35037, 35021, 35023, 35025, 35033, 35038, 35024, 35027, 35036, 35029, 35030, 35034]
id_armour = [[35040, 35041, 35042, 35043, 35044], [35050, 35051, 35052, 35053, 35054], [35060, 35061, 35062, 35063, 35064], [35045, 35046, 35047, 35048, 35049], [35070, 35071, 35072, 35073, 35074], [35065, 35066, 35067, 35068, 35069]]
id_accessories = [35075, 35076, 35077, 35078, 35079, 35080, 35081, 35082, 35083, 35084, 35085, 35086, 35087, 35088, 35089, 35090, 35091, 35092, 35093, 35094]

weapon_names = ['Classical Longsword', 'Classical Shield', 'Classical Battleaxe', 'Classical Greatsword', 'Classical Gunblade', 'Classical Cane', 'Classical Codex', 'Classical Torquetum', 'Classical Milpreves', 'Classical Tonfa', 'Classical Spear', 'Classical Daggers', 'Classical Samurai Blade', 'Classical War Scythe', 'Classical Cavalry Bow', 'Classical Handgonne', 'Classical Chakrams', 'Classical Longpole', 'Classical Index', 'Classical Smallsword']
armour_names = [['Classical Hoplomachus\'s Headgear', 'Classical Hoplomachus\'s Lorica', 'Classical Hoplomachus\'s Manicae', 'Classical Hoplomachus\'s Loincloth', 'Classical Hoplomachus\'s Greaves'],['Classical Secutor\'s Mask', 'Classical Secutor\'s Lorica', 'Classical Secutor\'s Manicae', 'Classical Secutor\'s Loincloth', 'Classical Secutor\'s Caligae'],['Classical Dimachaerius\'s Mask', 'Classical Dimachaerius\'s Lorica', 'Classical Dimachaerius\'s Manicae', 'Classical Dimachaerius\'s Loincloth', 'Classical Dimachaerius\'s Caligae'],['Classical Eques\'s Headgear', 'Classical Eques\'s Chiton', 'Classical Eques\'s Manicae', 'Classical Eques\'s Loincloth', 'Classical Eques\'s Caligae'],['Classical Signifer\'s Horns', 'Classical Signifer\'s Chiton', 'Classical Signifer\'s Fingerless Gloves', 'Classical Signifer\'s Culottes', 'Classical Signifer\'s Caligae'],['Classical Medicus\'s Laurel Wreath', 'Classical Medicus\'s Chiton', 'Classical Medicus\'s Wrist Torque', 'Classical Medicus\'s Loincloth', 'Classical Medicus\'s Caligae']]
accessory_names = ['Classical Earrings of Fending', 'Classical Earrings of Slaying', 'Classical Earrings of Aiming', 'Classical Earrings of Healing', 'Classical Earrings of Casting', 'Classical Choker of Fending', 'Classical Choker of Slaying', 'Classical Choker of Aiming', 'Classical Choker of Healing', 'Classical Choker of Casting', 'Classical Wristband of Fending', 'Classical Wristband of Slaying', 'Classical Wristband of Aiming', 'Classical Wristband of Healing', 'Classical Wristband of Casting', 'Classical Ring of Fending', 'Classical Ring of Slaying', 'Classical Ring of Aiming', 'Classical Ring of Healing', 'Classical Ring of Casting']

weapons = []
armour = []
accessories = []
helmet = []
chest = []
legs = []
feet = []
hands = []
weapon = []
accessory = []
index = -1

#The amount of certificates items are worth. The first two weapons are worth 10 and 7 respectively, all other 17
er_weapon = [10, 7, 17]
er_armour = [11, 17, 11, 17, 11]
er_accessories = 7

parser = argparse.ArgumentParser()		#Define argument parser
parser.add_argument("World", help="The server or datacenter to be checked for items. If a DC is entered all worlds within will be considered. Defaults to (Light) Lich", nargs="?", default='Lich', type=str)	#Add optional argument
parser.add_argument('-w', action=argparse.BooleanOptionalAction, help="Specifies, whether the output should also be written to a file", default=False)
args = parser.parse_args() #Create object for passed argument
args.World = args.World.lower()

# top = Tk()
# # Code to add widgets will go here...
# top.mainloop()

for y in range(0, len(Worlds[0])):	#Validate the passed server
	with suppress(ValueError):				
		index = Worlds[0][y].index(args.World)
		DC = y
		is_dc = 0
		break

if index == -1:
	for x in range(0, len(Worlds[1])):	#Search Datacenters if server was not found
		with suppress(ValueError):
			index = Worlds[1][x][0].index(args.World)
			DC = x
			is_dc = 1
			break

if index == -1:		#Default to (Light) Lich if input could not be verified
	print('Unknown World/Datacenter. Defaulting to (Light) Lich') 
elif is_dc == 0:
	print(f'Searching in ({Worlds[1][DC][0].title()}) {Worlds[is_dc][DC][index].title()}')
else:
	print(f'Searching in {Worlds[is_dc][DC][index].title()}')
URL += Worlds[is_dc][DC][index] + '/'	#The URL pointing to the chosen world or datacenter

weapons = utils.get_items(URL, id_weapon, weapon_names) #Request weapons in sequence
for x in range(0, len(id_armour)):
	armour.append(utils.get_items(URL, id_armour[x], armour_names[x]))	#Request armour based on type in sequence
accessories = utils.get_items(URL, id_accessories, accessory_names)		#Request accessories in sequence
y = 0
for x in range(0, len(weapons)):
	weapons[x][0] = weapons[x][0] / er_weapon[y]	#Assign an exchange value to each items cheapest offer
	if y != 2:
		y += 1
for x in range(0, len(armour)):
	for y in range(0, len(armour[x])):
		armour[x][y][0] = armour[x][y][0] / er_armour[y]
for x in range(0, len(accessories)):
	accessories[x][0] = accessories[x][0] / er_accessories

helmet = [item[0] for item in armour]	#Take the first element of each of the armour lists for a new list
chest = [item[1] for item in armour]
hands = [item[2] for item in armour]
legs = [item[3] for item in armour]
feet = [item[4] for item in armour]



weapons = sorted(weapons, key=lambda x: x[0])	#Use lambda calculation to sort the lists based on the value of the first element (price)
helmet = sorted(helmet, key=lambda x: x[0])
chest = sorted(chest, key=lambda x: x[0])
legs = sorted(legs, key=lambda x: x[0])
feet = sorted(feet, key=lambda x: x[0])
hands = sorted(hands, key=lambda x: x[0])
accessories = sorted(accessories, key=lambda x: x[0])

weapons = utils.filter_list(weapons)	#Delete elements that are marked as too old (<24 hours)
helmet = utils.filter_list(helmet)
chest = utils.filter_list(chest)
legs = utils.filter_list(legs)
feet = utils.filter_list(feet)
hands = utils.filter_list(hands)
accessories = utils.filter_list(accessories)

cheapest = [weapons[0]] + [helmet[0]] + [chest[0]] + [legs[0]] + [feet[0]] + [hands[0]] + [accessories[0]]	#Compile all cheapest items per category into a new list
cheapest = sorted(cheapest, key=lambda x: x[0])	#Sort the new list based on price

# w_name = requests.get(XIVDB + str(weapons[0][3])).text
# h_name = requests.get(XIVDB + str(helmet[0][3])).text
# c_name = requests.get(XIVDB + str(chest[0][3])).text
# l_name = requests.get(XIVDB + str(legs[0][3])).text
# f_name = requests.get(XIVDB + str(feet[0][3])).text
# ha_name = requests.get(XIVDB + str(hands[0][3])).text
# a_name = requests.get(XIVDB + str(accessories[0][3])).text
# w_name = re.search(r'(?<="Name_en":").*(?=","Name_fr")', w_name).group(0)

if args.w == True:	#Write to file if -w option was chosen
	with open('Data.txt', 'w') as cover:
		cover.write('{:_^89}\n'.format('_'))
		cover.write('|{:^42}|{:^12}|{:^16}|{:^14}|\n'.format('Item Name', 'Slot', 'Price per Token', 'Server'))
		cover.write('|{:^42}|{:^12}|{:^16}|{:^14}|\n'.format('', '', '', ''))
		cover.write('|{:<42}|{:^12}|{:^16}|{:^14}|\n'.format(weapons[0][3], 'Weapon', int(weapons[0][0]), weapons[0][2].title()))
		cover.write('|{:<42}|{:^12}|{:^16}|{:^14}|\n'.format(helmet[0][3], 'Helmet', int(helmet[0][0]), helmet[0][2].title()))
		cover.write('|{:<42}|{:^12}|{:^16}|{:^14}|\n'.format(chest[0][3], 'Chest', int(chest[0][0]), chest[0][2].title()))
		cover.write('|{:<42}|{:^12}|{:^16}|{:^14}|\n'.format(hands[0][3], 'Hands', int(hands[0][0]), hands[0][2].title()))
		cover.write('|{:<42}|{:^12}|{:^16}|{:^14}|\n'.format(legs[0][3], 'Legs', int(legs[0][0]), legs[0][2].title()))
		cover.write('|{:<42}|{:^12}|{:^16}|{:^14}|\n'.format(feet[0][3], 'Feet', int(feet[0][0]), feet[0][2].title()))
		cover.write('|{:<42}|{:^12}|{:^16}|{:^14}|\n'.format(accessories[0][3], 'Accessory', int(accessories[0][0]), accessories[0][2].title()))
		cover.write('|{:^42}|{:^12}|{:^16}|{:^14}|\n'.format('', '', '', ''))
		cover.write('|{:<42}|{:^12}|{:^16}|{:^14}|\n'.format(cheapest[0][3], 'Overall', int(cheapest[0][0]), cheapest[0][2].title()))
		cover.write('{:_^89}'.format('_'))

print('\n{:_^89}'.format('_'))	#Create a line at least 89 characters long, padded with '_' and aligned to the center
print('|{:^42}|{:^12}|{:^16}|{:^14}|'.format('Item Name', 'Slot', 'Price per Token', 'Server'))
print('|{:^42}|{:^12}|{:^16}|{:^14}|'.format('', '', '', ''))
print('|{:<42}|{:^12}|{:^16}|{:^14}|'.format(weapons[0][3], 'Weapon', int(weapons[0][0]), weapons[0][2]))
print('|{:<42}|{:^12}|{:^16}|{:^14}|'.format(helmet[0][3], 'Helmet', int(helmet[0][0]), helmet[0][2]))
print('|{:<42}|{:^12}|{:^16}|{:^14}|'.format(chest[0][3], 'Chest', int(chest[0][0]), chest[0][2]))
print('|{:<42}|{:^12}|{:^16}|{:^14}|'.format(hands[0][3], 'Hands', int(hands[0][0]), hands[0][2]))
print('|{:<42}|{:^12}|{:^16}|{:^14}|'.format(legs[0][3], 'Legs', int(legs[0][0]), legs[0][2]))
print('|{:<42}|{:^12}|{:^16}|{:^14}|'.format(feet[0][3], 'Feet', int(feet[0][0]), feet[0][2]))
print('|{:<42}|{:^12}|{:^16}|{:^14}|'.format(accessories[0][3], 'Accessory', int(accessories[0][0]), accessories[0][2]))
print('|{:^42}|{:^12}|{:^16}|{:^14}|'.format('', '', '', ''))
print('|{:<42}|{:^12}|{:^16}|{:^14}|'.format(cheapest[0][3], 'Overall', int(cheapest[0][0]), cheapest[0][2]))
print('{:_^89}'.format('_'))

input("Press Enter to exit")
