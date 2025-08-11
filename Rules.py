from typing import Dict
from BaseClasses import CollectionState, MultiWorld
from worlds.AutoWorld import World
from .Regions import connect_regions
from .Locations import location_table
from .Options import SuperCatPlanetOptions
import re



def set_rules(world: World, extra_walls_table: Dict[str, str]):

    player = world.player
    multiworld = world.multiworld

    costume_rules(world, extra_walls_table)

    multiworld.get_location("Green Switch", player).access_rule = lambda state: state.has("Red Switch", player, 1) or state.has("Orange Switch", player, 1) or state.has("Blue Switch", player, 1) or state.has("Yellow Switch", player, 1)
    if world.options.cat_rando:
        multiworld.get_location("Cat [Jungle - Above Lava Caves 2]", player).access_rule = lambda state: wall_rule(state, world, extra_walls_table, "Jungle_Lava")
    if world.options.include_final_stage:
        multiworld.get_location("Strange Cat [Final - Not Much Longer Now]", player).access_rule = lambda state: state.has("Pastry Basket", player, 1)
        multiworld.get_location("Thing", player).access_rule = lambda state: state.has("Pastry Basket", player, 1)

    connect_regions(world, "Menu", "Village", None)
    
    connect_regions(world, "Village", "Jungle", lambda state: wall_rule(state, world, extra_walls_table, "Village_Jungle"), twoway=True)
    connect_regions(world, "Village", "Canyon", lambda state: wall_rule(state, world, extra_walls_table, "Village_Canyon"), twoway=True)

    connect_regions(world, "Canyon", "Void", lambda state: state.has("Orange Switch", player, 1))
    connect_regions(world, "Canyon", "Flowers", lambda state: state.has("Orange Switch", player, 1), twoway=True)

    connect_regions(world, "Jungle", "Lava Caves", lambda state: wall_rule(state, world, extra_walls_table, "Jungle_Lava"), twoway=True)
    connect_regions(world, "Jungle", "Flowers", lambda state: wall_rule(state, world, extra_walls_table, "Jungle_Flowers"), twoway=True)
    connect_regions(world, "Jungle", "Factory", lambda state: wall_rule(state, world, extra_walls_table, "Jungle_Factory"), twoway=True)

    connect_regions(world, "Mushrooms_outside", "Mushrooms", lambda state: wall_rule(state, world, extra_walls_table, "Lava_Mushrooms"), twoway=True)
    connect_regions(world, "Mushrooms", "Final", lambda state: state.count("Strange Cat", player) >= 16)

    connect_regions(world, "Factory", "Mushrooms_outside", lambda state: wall_rule(state, world, extra_walls_table, "Factory_Lava"), twoway=True)
    
    connect_regions(world, "Mushrooms_outside", "Lava Caves", None)
    connect_regions(world, "Lava Caves", "Mushrooms_outside", lambda state: state.has("Purple Switch", player, 1))
    connect_regions(world, "Lava Caves", "Crows_intro", lambda state: wall_rule(state, world, extra_walls_table, "Lava_Ice"), twoway=True)

    connect_regions(world, "Ice Caves", "Flowers", lambda state: wall_rule(state, world, extra_walls_table, "Flowers_Ice"), twoway=True)

    connect_regions(world, "Ice Caves", "Ice Caves_inner", lambda state: state.has("White Switch", player, 1), twoway=False)
    connect_regions(world, "Ice Caves_inner", "Ice Caves", None, twoway=False)

    connect_regions(world, "Ice Caves_inner", "Crows_intro", lambda state: wall_rule(state, world, extra_walls_table, "Lava_Ice"), twoway=True)

    connect_regions(world, "Crows_intro", "Crows", lambda state: (((state.has("Left Yellow Switch", player, 1) and \
        state.has("Right Yellow Switch", player, 1)) or \
        state.has("White Switch", player, 1)) and \
        state.has("Red Switch", player, 1) and \
        state.has("Orange Switch", player, 1) and \
        state.has("Blue Switch", player, 1)), twoway=True)

    connect_regions(world, "Crows", "Warp Room", None)

    connect_regions(world, "Void", "Ice Caves", lambda state: wall_rule(state, world, extra_walls_table, "Flowers_Ice"), twoway=False)



    multiworld.completion_condition[player] = lambda state: goal_rule(state, world)

    #goal = getattr(multiworld.worlds[player].options, "ending_required")
    #if(goal == 0):
    #    multiworld.completion_condition[player] = lambda state: state.can_reach("Crows", 'Region', player)
    #else:
    #    multiworld.completion_condition[player] = lambda state: state.can_reach("Thing", 'Location', player)
    #
    #if(getattr(multiworld.worlds[player].options, "cat_hunt_enabled")):
    #    multiworld.completion_condition[player] = lambda state: state.has("Cat", getattr(multiworld.worlds[player].options, "cat_hunt_target"))

def costume_rules(world: World, extra_walls_table: Dict[str, str]):

    player = world.player
    multiworld = world.multiworld

    dye_locs = list(filter(lambda x: "Dye [" in x, location_table))
    drs_locs = list(filter(lambda x: "Dress [" in x, location_table))
    hat_locs = list(filter(lambda x: "Hat [" in x, location_table))
    wng_locs = list(filter(lambda x: "Wings [" in x, location_table))

    costume_locs = []
    costume_locs.extend(dye_locs)
    costume_locs.extend(drs_locs)
    costume_locs.extend(hat_locs)
    costume_locs.extend(wng_locs)
    
    catcount = 0
    strangecatcount = 0
    
    costint: Dict[str, int] = {} # my attempt at fixing a problem, probably stupid!!!

    for loc in costume_locs:
        cost = re.sub(r"\D", "", loc)
        try:
            costint = int(cost)
            multiworld.get_location(loc, player).access_rule = lambda state, costint=costint: enough_cats(state, world, extra_walls_table, costint)
        except ValueError:
            if(loc == "Dye [Black - ???]"):
                multiworld.get_location(loc, player).access_rule = lambda state: enough_cats(state, world, extra_walls_table, 1, strange=True)
            elif(loc == "Dye [Brown - HAT]"):
                multiworld.get_location(loc, player).access_rule = lambda state: state.can_reach("Flowers", 'Region', player)
            elif(loc == "Dye [Rainbow Flash - ALL]"):
                multiworld.get_location(loc, player).access_rule = lambda state: enough_cats(state, world, extra_walls_table, 168)
            elif(loc == "Dye [Rainbow Roll - ALL]"):
                multiworld.get_location(loc, player).access_rule = lambda state: enough_cats(state, world, extra_walls_table, 168)
            elif(loc == "Dye [Themed - ALL]"):
                multiworld.get_location(loc, player).access_rule = lambda state: enough_cats(state, world, extra_walls_table, 168)
            elif(loc == "Wings [Jet - BLU]"):
                multiworld.get_location(loc, player).access_rule = lambda state: state.has("Blue Switch", player, 1)
            elif(loc == "Wings [Scarlet - ???]"):
                multiworld.get_location(loc, player).access_rule = lambda state: enough_cats(state, world, extra_walls_table, 150) and state.can_reach("Flowers", 'Region', player)

            

            
def enough_cats(state: CollectionState, world: World, extra_walls_table: Dict[str, str], cost: int, strange = False) -> bool:
    
    player = world.player
    multiworld = world.multiworld

    catcount = 0
    if(not strange):
        if world.options.cat_rando:
            catcount = state.count("Cat", player)
        else:
            if state.can_reach("Village", "Region", player):
                catcount += 18
            if state.can_reach("Canyon", "Region", player):
                catcount += 29
            if state.can_reach("Jungle", "Region", player):
                catcount += 22
                if wall_rule(state, world, extra_walls_table, "Jungle_Lava") or not world.options.extra_walls:
                    catcount += 1
            if state.can_reach("Factory", "Region", player):
                catcount += 25
            if state.can_reach("Mushrooms_outside", "Region", player):
                catcount += 1
            if state.can_reach("Mushrooms", "Region", player):
                catcount += 1
            if state.can_reach("Lava Caves", "Region", player):
                catcount += 19
            if state.can_reach("Ice Caves", "Region", player):
                catcount += 24
            if state.can_reach("Flowers", "Region", player):
                catcount += 19
            if state.can_reach("Crows", "Region", player):
                catcount += 10
            if state.can_reach("Final", "Region", player):
                catcount += 1
    else:
        if world.options.strange_cat_rando:
            catcount = state.count("Strange Cat", player)
        else:
            if state.can_reach("Village", "Region", player):
                catcount += 2
            if state.can_reach("Canyon", "Region", player):
                catcount += 1
            if state.can_reach("Jungle", "Region", player):
                catcount += 1
            if state.can_reach("Factory", "Region", player):
                catcount += 1
            if state.can_reach("Lava Caves", "Region", player):
                catcount += 1
            if state.can_reach("Ice Caves", "Region", player):
                catcount += 3
            if state.can_reach("Flowers", "Region", player):
                catcount += 2
            if state.can_reach("Crows", "Region", player):
                catcount += 1
            if state.can_reach("Warp Room", "Region", player):
                catcount += 1
            if state.can_reach("Void", "Region", player):
                catcount += 3
            if state.can_reach("Final", "Region", player) and state.has("Pastry Basket", player, 1):
                catcount += 1
    return (catcount >= cost)



def create_extra_walls(world: World) -> Dict[str, str]:

    player = world.player
    multiworld = world.multiworld

    reg_links = ["Village_Jungle", "Village_Canyon", "Jungle_Lava", "Jungle_Flowers", "Jungle_Factory", "Factory_Lava", "Lava_Mushrooms", "Lava_Ice", "Flowers_Ice"]
    switches = ["Red Switch", "Orange Switch", "Yellow Switch", "Blue Switch", "White Switch", "Purple Switch"]
    next3 = [multiworld.random.choice(switches) for _ in range(3)]
    switches = switches + next3
    multiworld.random.shuffle(switches)

    walls = {key: value for key, value in (zip(reg_links, switches))}
    #print(walls)
    return walls

def wall_rule(state: CollectionState, world: World, walls: Dict[str, str], regs: str) -> bool:

    player = world.player
    multiworld = world.multiworld

    if(not world.options.extra_walls):
        return True
    
    switch = walls[regs]
    can_pass = False
    if(switch == "Yellow Switch"):
        if(state.has("Left Yellow Switch", player, 1) and state.has("Right Yellow Switch", player, 1)):
            can_pass = True
    elif state.has(switch, player, 1):
        can_pass = True
    return can_pass
    

def goal_rule(state: CollectionState, world: World) -> bool:

    player = world.player
    multiworld = world.multiworld

    can_goal = True
    goal = world.options.ending_required
    cats = world.options.cat_hunt_target
    

    if(goal == 0):
        can_goal = state.can_reach("Crows", 'Region', player)
    else:
        can_goal = state.can_reach("Thing", 'Location', player)
    
    if(not world.options.cat_hunt_enabled):
        cats = 0
    if(not state.has("Cat", player, cats)):
        can_goal = False
    
    return can_goal