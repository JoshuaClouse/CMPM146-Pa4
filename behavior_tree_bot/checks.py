

def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

def have_attacked_allies(state):
	for fleet in state.enemy_fleets():
		if any(planet.ID == fleet.destination_planet for planet in state.my_planets()):
			return True
	return False

def early_game(state):
  total_planets = len(state.my_planets()) + len(state.neutral_planets()) + len(state.enemy_planets())
  if len(state.neutral_planets()) > total_planets/2:
    return True
  return False