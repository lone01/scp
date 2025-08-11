from typing import Dict, List, NamedTuple, Optional

from BaseClasses import MultiWorld, Region, Entrance
from worlds.AutoWorld import World
from .Locations import SCPLocation, location_table, cat_location_table, strange_cat_location_table, costume_location_table, hidden_costume_location_table, get_locations_by_category
from .Options import SuperCatPlanetOptions

class SCPRegionData(NamedTuple):
	locations: Optional[List[str]]
	region_exits: Optional[List[str]]

def create_regions(world: World):

	player = world.player
	multiworld = world.multiworld


	if(world.options.cat_rando):
		location_table.update(cat_location_table)
	if(world.options.strange_cat_rando):
		location_table.update(strange_cat_location_table)
	if(world.options.hidden_costume_rando):
		location_table.update(hidden_costume_location_table)
	
	scpareas = ["Village", "Canyon", "Jungle", "Factory", "Mushrooms_outside", "Mushrooms", "Lava Caves", "Ice Caves", "Ice Caves_inner", "Flowers", "Crows_intro", "Crows", "Warp Room", "Void", "Final"]
	
	regMenu = Region("Menu", player, multiworld)
	multiworld.regions.append(regMenu)

	regVillage = Region("Village", player, multiworld)
	villageLocNames = list(filter(lambda x: "Village - " in x, location_table))
	villageLocNames.extend(list(filter(lambda x: "Dye [" in x, location_table)))
	if(world.options.cat_rando):
		villageLocNames.append('Cat [Dye Shop]')
	regVillage.locations += [SCPLocation(player, loc_name, location_table[loc_name].address, regVillage) for loc_name in villageLocNames]
	multiworld.regions.append(regVillage)

	regCanyon = Region("Canyon", player, multiworld)
	canyonLocNames = list(filter(lambda x: "Canyon - " in x, location_table))
	canyonLocNames.extend(list(filter(lambda x: "Dress [" in x, location_table)))
	if(world.options.cat_rando):
		canyonLocNames.append('Cat [Dress Shop]')
	canyonLocNames.append('Orange Switch')
	regCanyon.locations += [SCPLocation(player, loc_name, location_table[loc_name].address, regCanyon) for loc_name in canyonLocNames]
	multiworld.regions.append(regCanyon)

	regJungle = Region("Jungle", player, multiworld)
	jungleLocNames = list(filter(lambda x: "Jungle - " in x, location_table))
	jungleLocNames.append('Green Switch')
	regJungle.locations += [SCPLocation(player, loc_name, location_table[loc_name].address, regJungle) for loc_name in jungleLocNames]
	multiworld.regions.append(regJungle)

	regFactory = Region("Factory", player, multiworld)
	factoryLocNames = list(filter(lambda x: "Factory - " in x, location_table))
	factoryLocNames.append('Blue Switch')
	regFactory.locations += [SCPLocation(player, loc_name, location_table[loc_name].address, regFactory) for loc_name in factoryLocNames]
	multiworld.regions.append(regFactory)

	regOutsideMush = Region("Mushrooms_outside", player, multiworld)
	outmushLocNames = []
	if(world.options.cat_rando):
		outmushLocNames.append("Cat [Lava Caves - Entrance from Factory]")
	regOutsideMush.locations += [SCPLocation(player, loc_name, location_table[loc_name].address, regOutsideMush) for loc_name in outmushLocNames]
	multiworld.regions.append(regOutsideMush)

	regMushrooms = Region("Mushrooms", player, multiworld)
	mushroomsLocNames = [ "Purple Switch" ]
	mushroomsLocNames.extend(list(filter(lambda x: "Wings [" in x, location_table)))
	if(world.options.cat_rando):
		mushroomsLocNames.append('Cat [Wings Shop]')
	if(world.options.hidden_costume_rando):
		mushroomsLocNames.append('Hidden Costume [Mushrooms - Left of Save]')
	regMushrooms.locations += [SCPLocation(player, loc_name, location_table[loc_name].address, regMushrooms) for loc_name in mushroomsLocNames]
	multiworld.regions.append(regMushrooms)

	regLava = Region("Lava Caves", player, multiworld)
	lavaLocNames = list(filter(lambda x: "Lava Caves - " in x, location_table))
	lavaLocNames.extend(['Right Yellow Switch', 'Left Yellow Switch'])
	if "Cat [Lava Caves - Entrance from Factory]" in lavaLocNames:
		lavaLocNames.remove("Cat [Lava Caves - Entrance from Factory]")
	regLava.locations += [SCPLocation(player, loc_name, location_table[loc_name].address, regLava) for loc_name in lavaLocNames]
	multiworld.regions.append(regLava)

	regIce = Region("Ice Caves", player, multiworld)
	iceLocNames = list(filter(lambda x: "Ice Caves - " in x, location_table))
	iceLocNames.append('White Switch')
	if "Cat [Ice Caves - By Crows]" in iceLocNames:
		iceLocNames.remove("Cat [Ice Caves - By Crows]")
	regIce.locations += [SCPLocation(player, loc_name, location_table[loc_name].address, regIce) for loc_name in iceLocNames]
	multiworld.regions.append(regIce)

	regIceInner = Region("Ice Caves_inner", player, multiworld)
	iceInnerLocNames = []
	if(world.options.cat_rando):
		iceInnerLocNames.append("Cat [Ice Caves - By Crows]")
	regIceInner.locations += [SCPLocation(player, loc_name, location_table[loc_name].address, regIceInner) for loc_name in iceInnerLocNames]
	multiworld.regions.append(regIceInner)

	regFlowers = Region("Flowers", player, multiworld)
	flowersLocNames = list(filter(lambda x: "Flowers - " in x, location_table))
	flowersLocNames.extend(list(filter(lambda x: "Hat [" in x, location_table)))
	if(world.options.cat_rando):
		flowersLocNames.append('Cat [Hat Shop]')
	flowersLocNames.append('Red Switch')
	regFlowers.locations += [SCPLocation(player, loc_name, location_table[loc_name].address, regFlowers) for loc_name in flowersLocNames]
	multiworld.regions.append(regFlowers)

	regCrowsIntro = Region("Crows_intro", player, multiworld)
	multiworld.regions.append(regCrowsIntro)

	regCrows = Region("Crows", player, multiworld)
	crowsLocNames = list(filter(lambda x: "Crows - " in x, location_table))
	regCrows.locations += [SCPLocation(player, loc_name, location_table[loc_name].address, regCrows) for loc_name in crowsLocNames]
	multiworld.regions.append(regCrows)

	regWarpRoom = Region("Warp Room", player, multiworld)
	if(world.options.strange_cat_rando):
		warproomLocNames = ["Strange Cat [Warp Room - Not Over Yet]"]
		regWarpRoom.locations += [SCPLocation(player, loc_name, location_table[loc_name].address, regWarpRoom) for loc_name in warproomLocNames]
	multiworld.regions.append(regWarpRoom)

	regVoid = Region("Void", player, multiworld)
	voidLocNames = list(filter(lambda x: "Void - " in x, location_table))
	regVoid.locations += [SCPLocation(player, loc_name, location_table[loc_name].address, regVoid) for loc_name in voidLocNames]
	multiworld.regions.append(regVoid)

	regFinal = Region("Final", player, multiworld)
	finalLocNames = list(filter(lambda x: "Final - " in x, location_table))
	finalLocNames.extend(['Pastry Basket', 'Thing'])
	if(world.options.include_final_stage):
		regFinal.locations += [SCPLocation(player, loc_name, location_table[loc_name].address, regFinal) for loc_name in finalLocNames]
	multiworld.regions.append(regFinal)

def create_region(world: World, name: str, data: SCPRegionData):

	player = world.player
	multiworld = world.multiworld

	region = Region(name, player, multiworld)
	if data.locations:
		for loc_name in data.locations:
			loc_data = location_table.get(loc_name)
			location = SCPLocation(player, loc_name, loc_data.code if loc_data else None, region)
			region.locations.append(location)

	return region

def connect_regions(world: World, source: str, target: str, rule=None, twoway=False):

	player = world.player
	multiworld = world.multiworld

	sourceRegion = multiworld.get_region(source, player)
	targetRegion = multiworld.get_region(target, player)
	sourceRegion.connect(targetRegion, rule=rule)
	if twoway:
		targetRegion.connect(sourceRegion, rule=rule)
