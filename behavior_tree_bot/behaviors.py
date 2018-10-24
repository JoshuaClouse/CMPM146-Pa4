import sys
sys.path.insert(0, '../')
from planet_wars import issue_order


def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    #weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    weakest_planet = min([planet for planet in state.enemy_planets() if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())], key=lambda p: p.num_ships + p.growth_rate * state.distance(strongest_planet.ID, p.ID), default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        fleet = weakest_planet.num_ships + weakest_planet.growth_rate * state.distance(strongest_planet.ID, weakest_planet.ID)
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, fleet + 1)


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)
    
    closest_my_planet = None
    closest_neutral_planet = None
    closest_distance = None

    for my_planet in state.my_planets():
        for neutral_planet in [planet for planet in state.neutral_planets() if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]:
            if my_planet.num_ships > neutral_planet.num_ships:

                if closest_distance == None:
                    closest_distance = state.distance(my_planet.ID, neutral_planet.ID)
                else:
                    cur_distance = state.distance(my_planet.ID, neutral_planet.ID)
                    if cur_distance < closest_distance:
                        closest_distance = cur_distance
                        closest_my_planet = my_planet
                        closest_neutral_planet = neutral_planet
    
    if not closest_my_planet or not closest_neutral_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, closest_my_planet.ID, closest_neutral_planet.ID, closest_neutral_planet.num_ships +1)
'''
def destination_in_fleet(state, destination):
    for fleet in state.my_fleets():
        if destination == fleet.destination_planet:
            return True
    return False
'''