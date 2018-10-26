import sys
sys.path.insert(0, '../')
from planet_wars import issue_order
import math

def attack_weakest_enemy_planet(state):
    closest_my_planet = None
    closest_enemy_planet = None
    closest_distance = math.inf
    fleet_size = 0

    no_my_fleet_on_the_way_enemy_planet = [planet for planet in state.enemy_planets() if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]

    for my_planet in state.my_planets():
        for enemy_planet in state.enemy_planets():   
            
            cur_distance = state.distance(my_planet.ID, enemy_planet.ID)

            if enemy_planet in no_my_fleet_on_the_way_enemy_planet:

                if cur_distance < closest_distance:

                    
                    ships_needed = enemy_planet.num_ships + 1
                    
                    enemy_fleet_list = [fleet for fleet in state.enemy_fleets() if fleet.destination_planet == enemy_planet.ID]

                    if enemy_fleet_list:
                        for fleet in enemy_fleet_list:
                            ships_needed += fleet.num_ships

                    ships_needed += state.distance(my_planet.ID, enemy_planet.ID) * enemy_planet.growth_rate

                
                # Don't send ships out if there is a coming fleet, unless Total amound > ivading fleet amount + amount to send out
                enemy_fleet_list = [fleet for fleet in state.enemy_fleets() if fleet.destination_planet == my_planet.ID]
                total_attack_force = 0
                if enemy_fleet_list:
                    for fleet in enemy_fleet_list:
                        total_attack_force += fleet.num_ships
                
                if my_planet.num_ships > ships_needed + total_attack_force:
                    
                    closest_distance = cur_distance
                    closest_my_planet = my_planet
                    closest_enemy_planet = enemy_planet
                    fleet_size = ships_needed
            
    if not closest_my_planet or not closest_enemy_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, closest_my_planet.ID, closest_enemy_planet.ID, fleet_size)


def spread_to_weakest_neutral_planet(state):
    closest_my_planet = None
    closest_neutral_planet = None
    closest_distance = math.inf
    fleet_size = 0

    my_fleet_on_the_way_neutral_planets = [planet for planet in state.neutral_planets() if any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    no_my_fleet_on_the_way_neutral_planets = [planet for planet in state.neutral_planets() if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]

    enemy_fleet_on_the_way_neutral_planets = [planet for planet in state.neutral_planets() if any(fleet.destination_planet == planet.ID for fleet in state.enemy_fleets())]
    no_enemy_fleet_on_the_way_neutral_planets = [planet for planet in state.neutral_planets() if not any(fleet.destination_planet == planet.ID for fleet in state.enemy_fleets())]
    
    # Planet with both fleets on the wayc
    neutral_planets_with_both_fleets = list(set(my_fleet_on_the_way_neutral_planets) & set(enemy_fleet_on_the_way_neutral_planets))

    # Planet with only my fleet
    neutral_planets_with_only_my_fleets = list(set(my_fleet_on_the_way_neutral_planets) - set(neutral_planets_with_both_fleets))

    # Planet with only enemy fleet
    neutral_planets_with_only_enemy_fleets = list(set(enemy_fleet_on_the_way_neutral_planets) - set(neutral_planets_with_both_fleets))


    for my_planet in state.my_planets():      

        for neutral_planet in state.neutral_planets():

            cur_distance = state.distance(my_planet.ID, neutral_planet.ID)

            if neutral_planet in no_my_fleet_on_the_way_neutral_planets:

                if cur_distance < closest_distance:
                    
                    ships_needed = neutral_planet.num_ships

                    # in case there are enemy fleets heading toward target planet
                    if neutral_planet in neutral_planets_with_only_enemy_fleets: 
                        enemy_fleet_list = [fleet for fleet in state.enemy_fleets() if fleet.destination_planet == neutral_planet.ID]
                        enemy_fleet_list = sorted(enemy_fleet_list, key=lambda f: f.turns_remaining)
                        planet_conquered = False
                        conquered_turns = 0
                        
                        for fleet in enemy_fleet_list:
                            if planet_conquered == False: # if the target planet has not yet been conquered 
                                if fleet.num_ships <= ships_needed: # if the enemy fleet is not big enough to capture it
                                    ships_needed -= fleet.num_ships
                                else: # if the enemy fleet is big enough to capture it
                                    ships_needed = fleet.num_ships - ships_needed
                                    planet_conquered = True
                                    
                                    if state.distance(my_planet.ID, neutral_planet.ID) > fleet.turns_remaining: # if my fleet can't get to the planet before its captured
                                        conquered_turns = state.distance(my_planet.ID, neutral_planet.ID) - fleet.turns_remaining
                                    
                            else: # if the target planet is captured
                                ships_needed += fleet.num_ships
                            
                        ships_needed += conquered_turns * neutral_planet.growth_rate
                    
                    """
                    # in case there are both enemy fleets and my fleets heading toward the same planet
                    if neutral_planet in neutral_planets_with_both_fleets:
                        enemy_fleet_list = [fleet for fleet in state.enemy_fleets() if fleet.destination_planet == neutral_planet.ID]
                        my_fleet_list = [fleet for fleet in state.my_fleets() if fleet.destination_planet == neutral_planet.ID]
                        total_fleet_list = list(set(enemy_fleet_list) | set(my_fleet_list))
                        total_fleet_list = sorted(total_fleet_list, key=lambda f: f.turns_remaining)
                        planet_owner = 0 # 0 is not captured, 1 is you, 2 is opponent
                        conquered_turns = 0 # turns of you captured the planet

                        for fleet in total_fleet_list:
                            if fleet.owner == 1:
                                if planet_owner == 0:
                                    if fleet.num_ships <= ships_needed:
                                        ships_needed -= fleet.num_ships
                                    else:
                                        ships_needed = fleet.num_ships - ships_needed
                                        planet_owner = 1

                                        try:
                                            conquered_turns = total_fleet_list[total_fleet_list.index(fleet)+1].turns_remaining - fleet.turns_remaining
                                            ships_needed -= conquered_turns * neutral_planet.growth_rate
                                        except:
                                            ships_needed = -1



                                elif planet_owner == 1:
                                    ships_needed -= fleet.num_ships

                                    try:
                                        conquered_turns = total_fleet_list[total_fleet_list.index(fleet)+1].turns_remaining - fleet.turns_remaining
                                        ships_needed -= conquered_turns * neutral_planet.growth_rate
                                    except:
                                        ships_needed = -1

                                elif planet_owner == 2:
                                    if fleet.num_ships <= ships_needed:
                                        ships_needed -= fleet.num_ships
                                    else:
                                        ships_needed = fleet.num_ships - ships_needed
                                        planet_owner = 1

                                        try:
                                            conquered_turns = total_fleet_list[total_fleet_list.index(fleet)+1].turns_remaining - fleet.turns_remaining
                                            ships_needed -= conquered_turns * neutral_planet.growth_rate
                                        except:
                                            ships_needed = -1

                            if fleet.owner == 2:
                                if planet_owner == 0:
                                    if fleet.num_ships <= ships_needed:
                                        ships_needed -= fleet.num_ships
                                    else:
                                        ships_needed = fleet.num_ships - ships_needed
                                        planet_owner = 1

                                        try:
                                            conquered_turns = total_fleet_list[total_fleet_list.index(fleet)+1].turns_remaining - fleet.turns_remaining
                                            ships_needed += conquered_turns * neutral_planet.growth_rate
                                        except:
                                            conquered_turns = state.distance(my_planet.ID, neutral_planet.ID)
                                            ships_needed += conquered_turns * neutral_planet.growth_rate

                                elif planet_owner == 1:
                                    if fleet.num_ships <= -ships_needed:
                                        ships_needed += fleet.num_ships
                                    else:
                                        ships_needed += fleet.num_ships
                                        planet_owner = 1

                                        try:
                                            conquered_turns = total_fleet_list[total_fleet_list.index(fleet)+1].turns_remaining - fleet.turns_remaining
                                            ships_needed += conquered_turns * neutral_planet.growth_rate
                                        except:
                                            conquered_turns = state.distance(my_planet.ID, neutral_planet.ID)
                                            ships_needed += conquered_turns * neutral_planet.growth_rate

                                elif planet_owner == 2:
                                    ships_needed += fleet.num_ships

                                    try:
                                        conquered_turns = total_fleet_list[total_fleet_list.index(fleet)+1].turns_remaining - fleet.turns_remaining
                                        ships_needed += conquered_turns * neutral_planet.growth_rate
                                    except:
                                        conquered_turns = state.distance(my_planet.ID, neutral_planet.ID)
                                        ships_needed += conquered_turns * neutral_planet.growth_rate
                    """

                     # Don't send ships out if there is a coming fleet, unless Total amound > ivading fleet amount + amount to send out
                    enemy_fleet_list = [fleet for fleet in state.enemy_fleets() if fleet.destination_planet == my_planet.ID]
                    total_attack_force = 0
                    if enemy_fleet_list:
                        for fleet in enemy_fleet_list:
                            total_attack_force += fleet.num_ships
                    
                    if my_planet.num_ships > ships_needed + total_attack_force and ships_needed > 0:
                        closest_distance = cur_distance
                        closest_my_planet = my_planet
                        closest_neutral_planet = neutral_planet
                        fleet_size = ships_needed
                    

    if not closest_my_planet or not closest_neutral_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, closest_my_planet.ID, closest_neutral_planet.ID, fleet_size+1)


def defend_from_enemy_fleet(state):
    closest_my_planet = None
    closest_ally_planet = None
    closest_distance = math.inf
    fleet_size = 0

    allies_under_attack = [planet for planet in state.my_planets() if any(planet.ID == fleet.destination_planet for fleet in state.enemy_fleets())]

    no_my_fleet_on_the_way_ally_planet = [planet for planet in state.my_planets() if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]

    for my_planet in state.my_planets():      

        for my_ally in allies_under_attack:

            cur_distance = state.distance(my_planet.ID, my_ally.ID)

            if my_ally in no_my_fleet_on_the_way_ally_planet:

                if cur_distance < closest_distance:
                    
                    ships_needed = my_ally.num_ships

                    planet_owner = 1 # 0 is not captured, 1 is you, 2 is opponent

                    enemy_fleet_list = [fleet for fleet in state.enemy_fleets() if fleet.destination_planet == my_ally.ID]
                    enemy_fleet_list = sorted(enemy_fleet_list, key=lambda f: f.turns_remaining)
                    
                    conquered_turns = enemy_fleet_list[0].turns_remaining # turns of you captured the planet
                    ships_needed = -my_ally.num_ships - my_ally.growth_rate * conquered_turns # actual number of ships when enemy fleet arrives
                    
                    for fleet in enemy_fleet_list:
                        if planet_owner == 1: # if the target planet has not yet been conquered 
                            if fleet.num_ships < -ships_needed: # if the enemy fleet is not big enough to capture it
                                ships_needed += fleet.num_ships
                                
                                try: # if there are more than one fleet
                                    conquered_turns = enemy_fleet_list[enemy_fleet_list.index(fleet)+1].turns_remaining - fleet.turns_remaining
                                    ships_needed -= conquered_turns * my_ally.growth_rate
                                except:
                                    ships_needed = -1

                            else: # if the enemy fleet is big enough to capture it
                                ships_needed += fleet.num_ships
                                planet_owner = 2
                                conquered_turns = state.distance(my_ally.ID, my_planet.ID)
                                ships_needed += conquered_turns * my_ally.growth_rate

                        else: # if the target planet is captured
                            ships_needed += fleet.num_ships
                            planet_owner = 2

                enemy_fleet_list = [fleet for fleet in state.enemy_fleets() if fleet.destination_planet == my_planet.ID]
                total_attack_force = 0
                if enemy_fleet_list:
                    for fleet in enemy_fleet_list:
                        total_attack_force += fleet.num_ships
                
                 # Don't send ships out if there is a coming fleet, unless Total amound > ivading fleet amount + amount to send out
                if my_planet.num_ships > ships_needed + total_attack_force and ships_needed > 0:
                    closest_distance = cur_distance
                    closest_my_planet = my_planet
                    closest_ally_planet = my_ally
                    fleet_size = ships_needed

    if not closest_my_planet or not closest_ally_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, closest_my_planet.ID, closest_ally_planet.ID, fleet_size+1)







