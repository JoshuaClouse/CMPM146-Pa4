import sys
#logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
sys.path.insert(0, '../')
from planet_wars import issue_order


def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 3:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    #logging.debug("please display")
    if len(state.my_fleets()) >= 3:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)

def spread_to_closest_neutral_planet(state):

    if len(state.my_fleets()) >= 3:
        return False
    distance = None
    closestNeutralPlanet = None
    closestOwnedPlanet = None
    logging.debug("please display")
    for neutral_planet in state.neutral_planets():
        for my_planet in state.my_planets():
            if neutral_planet.num_ships < my_planet.numships * .7:
                if closestNeutralPlanet == None:
                    closestNeutralPlanet = neutral_planet
                    closestOwnedPlanet = my_planet
                    distance = state.distance(my_planet.ID, neutral_planet.ID)
                elif state.distance(my_planet.ID, neutral_planet.ID) < distance:
                    closestNeutralPlanet = neutral_planet
                    closestOwnedPlanet = my_planet
                    distance = state.distance(my_planet.ID, neutral_planet.ID)
    return issue_order(state, closestOwnedPlanet.ID, closestNeutralPlanet.ID, closestOwnedPlanet.num_ships * .7)
    return False