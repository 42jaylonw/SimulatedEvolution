import toml
from sim.sim_space import SimSpace
from sim.creatures.comsumer import Consumer
from sim.creatures.producer import Producer
from sim import presets as preset
from sim.emitter import LightSource, HeatSource
from flask import jsonify
from games.survival.survival import SurvivalSim

def create_sim(num_producers=1, num_consumers=1, width=50):
    """
    Create a SimSpace object

    Params:
        num_producers(int): number of produces present in SimSpace

        num_consumers(int): number of consumers present in SimSpace
        
        width(int): width to create NxN SimSpace(default width is 50)
    Return:
        sim(SimSpace): NxN SimSpace with specified features from parameters
    """
    # Change TOML gridsize
    with open("games/survival/config.toml", 'r') as f:
        config = toml.load(f)
    config['SimSpace']['grid_size'] = [width, width]
    with open('games/survival/config.toml', 'w') as f:
        toml.dump(config, f)
    # Create SimSpace
    #sim = SimSpace(config)
    sim = SurvivalSim(config)
    # Instantiate Organisms
    producers = [Producer(sim) for _ in range(num_producers)]
    consumers = [Consumer(sim) for _ in range(num_consumers)]
    
    # add all instantiated objects to SimSpace
    sim.reset(producers + consumers, emitters=[])
    return sim


def get_sim_state(simulator, includeImageData=False, getRawState=False):
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
    if getRawState:
        return gridspacesInformation
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
        creature_data["emitters"].append({"range":emitter.emit_range, "strength":int(emitter.emit_val)})

    return jsonify(creature_data)

# Place a wall in the simulation at the specified location
def user_place_wall(sim, position):
    user_erase_space(sim, position)
    sim.layer_system.wall_add(position)

# Place a LightSource in the simulation at the specified location.
# If there is a wall there, no emitter will be placed
# Currently a preset for the strength/range of the emitter
def user_place_lightsource(sim, position, emit_range=20, emit_strength=100):
    if not sim.layer_system.has_wall(position):
        LightSource(sim, position, emit_range, emit_strength)
        # sim.reset(sim.creatures, new_emitter_list)
        # sim.add_emitter(new_light_source)
        user_place_emitter_visual_helper(sim)
        

# Place a HeatSource in the simulation at the specified location.
# If there is a wall there, no emitter will be placed
# Currently a preset for the strength/range of the emitter
def user_place_heatsource(sim, position, emit_range=20, emit_strength=100):
    if not sim.layer_system.has_wall(position):
        HeatSource(sim, position, emit_range, emit_strength)
        # sim.reset(sim.creatures, new_emitter_list)
        # sim.add_emitter(new_heat_source)
        user_place_emitter_visual_helper(sim)

def user_place_emitter_visual_helper(sim):
    sim.layer_system.step(decayPheromones=False)
    for emitter in sim.emitters:
        emitter.step()

# Place a Consumer in the simulation at the specified location.
# If there is a wall there, no consumer will be placed
# Currently the genome is random
def user_place_consumer(sim, position, presetID=None):
    if not sim.layer_system.has_wall(position):
        Consumer(sim, spawn_pos=position, genome=preset.load_consumer_preset(presetID))


# Place a Prodcuer in the simulation at the specified location.
# If there is a wall there, no producer will be placed
# Currently the genome is random
def user_place_producer(sim, position, presetID=None):
    if not sim.layer_system.has_wall(position):
        Producer(sim, spawn_pos=position, genome=preset.load_producer_preset(presetID))


# Erase EVERYTHING (Creatures, Wall, Emitters) at the specified location.
def user_erase_space(sim, position):
    sim.layer_system.wall_remove(position)

    removed_creatures = sim.layer_system.get_creatures(position)
    removed_emitters = sim.layer_system.get_emitters(position)

    # remove everything at the GridSpace object
    sim.layer_system.empty_space(position)

    # Remove the creatures and emitters from the lists in simspace
    for creature in removed_creatures:
        sim.remove_creature(creature)

    for emitter in removed_emitters:
        sim.remove_emitter(emitter)
  
    # Clear all emitter values in Simulation
    sim.layer_system.clear_emitter_values()
    for emitter in sim.emitters:
        emitter.step()

# EXPERIMENTAL
# Erase EVERYTHING in the simulation at ALL POSITIONS.
def user_clear_simulation(sim):
    for x in range(sim.layer_system.get_dimensions()[0]):
        for y in range(sim.layer_system.get_dimensions()[1]):
            user_erase_space(sim, [x, y])
