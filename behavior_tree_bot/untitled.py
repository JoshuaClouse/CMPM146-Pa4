if neutral_planet in neutral_planets_with_only_enemy_fleets:
    enemy_fleet_list = [fleet for fleet in state.enemy_fleets() if fleet.destination_planet == neutral_planet.ID]
    enemy_fleet_list = sorted(enemy_fleet_list, key=lambda f: f.turns_remaining)
    planet_conquered = False
    conquered_turns = 0
    for fleet in enemy_fleet_list:
        if planet_conquered == False: # if the target star has not yet been conquered 
            if fleet.num_ships <= ships_needed: # if the enemy fleet is not big enough to capture it
                ships_needed -= fleet.num_ships
            else: # if the enemy fleet is big enough to capture it
                ships_needed = fleet.num_ships - ships_needed
                planet_conquered = True
                if state.distance(closest_my_planet, neutral_planet) > fleet.turns_remaining: # if my fleet can't get to the planet before its captured
                    conquered_turns = state.distance(closest_my_planet, neutral_planet) - fleet.turns_remaining
        else: # if the target star is captured
            ships_needed += fleet.num_ships
    ships_needed += conquered_turns * neutral_planet.growth_rate