import toml
from sim.sim_space import SimSpace
from sim.creatures.comsumer import Consumer
from sim.creatures.producer import Producer
import numpy as np
from sim.emitter import LightSource, HeatSource
from flask import jsonify

def create_sim(num_producers=1, num_consumers=1, width=50):
    """
    Create a SimSpace object

    Params:
        num_producers(int): number of produces present in SimSpace

        num_consumers(int): numner of consumers present in SimSpace
        
        width(int): width to create NxN SimSpace(default width is 50)
    Return:
        sim(SimSpace): NxN SimSpace with specified features from parameters
    """
    # Change TOML gridsize
    with open("games/sprint_2_survival/config.toml", 'r') as f:
        config = toml.load(f)
    config['SimSpace']['grid_size'] = [width, width]
    with open('games/sprint_2_survival/config.toml', 'w') as f:
        toml.dump(config, f)
    # Create SimSpace
    sim = SimSpace(config)
    # Instantiate Organisms
    producers = [Producer(sim) for _ in range(num_producers)]
    consumers = [Consumer(sim) for _ in range(num_consumers)]

    # # Add Wall
    # for i in range(sim.grid_size[0]):
    #     sim.layer_system.wall_add([i, sim.grid_size[0] // 2])
    # Instantiate emitters(sim, pos, e_range, e_val)
    # emitters = [HeatSource(sim, [sim.grid_size[0] // 3, 1 * sim.grid_size[1] // 4], 25, 75),
    #             LightSource(sim, [(sim.grid_size[0] // 3), (sim.grid_size[1] // 4)], 50, 100)] 
    
    # add all instantiated objects to SimSpace
    sim.reset(producers + consumers, emitters=[])
    return sim


def get_sim_state(simulator, includeImageData=False):
    """
    Retrieves and jsonifies information about each grid space in a simulator
    
    Param: 
        simulator(SimSpace): SimSpace object
    Returns:
        gridspacesInformation(json): a list of all gridspaces where each gridspace has a tuple following the format:\n 
         (position, num_consumers, num_producers, has_a_wall, np.int16(self.temperature_val))
    """
    # Iterate over each grid space object
    simWidth = simulator.grid_size[0]
    gridspacesInformation = []
    for i in range(simWidth):
        for j in range(simWidth):
           # access and append each gridspaces' properties
           gridspacesInformation.append(simulator.layer_system.get_gridspace([i,j]).get_properties(includeImageData))
    # return information of all gridspaces
    return jsonify(gridspacesInformation)

def get_gridspace_state(simulator, position):
    return jsonify(simulator.layer_system.get_gridspace(position).get_properties(True))
    

# Get the information of all creatures at specified location
def get_creatures_wrapper(sim, position):
    creature_data = {"producers" : list(), "consumers" : list(), "emitters": list()}
    producers = sim.layer_system.get_producers(position)
    for producer in producers:
        creature_data["producers"].append(producer.creature_info)
    consumers = sim.layer_system.get_consumers(position)
    for consumer in consumers:
        creature_data["consumers"].append(consumer.creature_info)
    emitters = sim.layer_system.get_emitters(position)
    for emitter in emitters:
        creature_data["emitters"].append({"range":emitter.emit_range, "strength":emitter.emit_value})
    return jsonify(creature_data)

# Place a wall in the simulation at the specified location
def user_place_wall(sim, position):
    user_erase_space(sim, position)
    sim.layer_system.wall_add(position)

# Place a LightSource in the simulation at the specified location.
# If there is a wall there, no emitter will be placed
# Currently a preset for the strength/range of the emitter
def user_place_lightsource(sim, position):
    if not sim.layer_system.has_wall(position):
        new_light_source = LightSource(sim, position, 20, 100)
        # sim.reset(sim.creatures, new_emitter_list)
        sim.add_emitter(new_light_source)
        user_place_emitter_visual_helper(sim)

# Place a HeatSource in the simulation at the specified location.
# If there is a wall there, no emitter will be placed
# Currently a preset for the strength/range of the emitter
def user_place_heatsource(sim, position):
    if not sim.layer_system.has_wall(position):
        new_heat_source = HeatSource(sim, position, 20, 100)
        # sim.reset(sim.creatures, new_emitter_list)
        sim.add_emitter(new_heat_source)
        user_place_emitter_visual_helper(sim)

def user_place_emitter_visual_helper(sim):
    sim.layer_system.step(decayPheromones=False)
    for emitter in sim.emitters:
        emitter.step()

# Place a Consumer in the simulation at the specified location.
# If there is a wall there, no consumer will be placed
# Currently the genome is random
def user_place_consumer(sim, position):
    if not sim.layer_system.has_wall(position):
        new_creature = Consumer(sim, spawn_pos=position)
        new_creature_list = sim.creatures
        new_creature_list.append(new_creature)
        sim.add_creature(new_creature)


# Place a Prodcuer in the simulation at the specified location.
# If there is a wall there, no producer will be placed
# Currently the genome is random
def user_place_producer(sim, position):
    if not sim.layer_system.has_wall(position):
        new_creature = Producer(sim, spawn_pos=position)
        new_creature_list = sim.creatures
        new_creature_list.append(new_creature)
        sim.add_creature(new_creature)
        # sim.reset(new_creature_list, sim.emitters)


# Erase EVERYTHING (Creatures, Wall, Emitters) at the specified location.
def user_erase_space(sim, position):
    sim.layer_system.wall_remove(position)

    for creature in sim.creatures:
        if creature.position[0] == position[0] and creature.position[1] == position[1]:
            creature.remove()
    
    for emitter in sim.emitters:
        if emitter.position[0] == position[0] and  emitter.position[1] == position[1]:
            emitter.remove()

# EXPERIMENTAL
# Erase EVERYTHING in the simulation at ALL POSITIONS.
def user_clear_simulation(sim):
    for x in range(sim.layer_system.get_dimensions()[0]):
        for y in range(sim.layer_system.get_dimensions()[1]):
            user_erase_space(sim, [x, y])
