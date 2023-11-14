import toml
from sim.sim_space import SimSpace
from sim.creatures.comsumer import Consumer
from sim.creatures.producer import Producer

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
    with open("games/sprint_0_random/config.toml", 'r') as f:
        config = toml.load(f)
    config['SimSpace']['grid_size'] = [width, width]
    with open('games/sprint_0_random/config.toml', 'w') as f:
        toml.dump(config, f)
    # Create SimSpace
    sim = SimSpace(config)
    # Instantiate Organisms
    producers = [Producer(sim) for _ in range(num_producers)]
    consumers = [Consumer(sim) for _ in range(num_consumers)]

    # Add Wall
    for i in range(sim.grid_size[0]):
        sim.layer_system.wall_add([i, sim.grid_size[0] // 2])
        
    # Instantiate emitters
    emitters = [HeatSource(sim, [sim.grid_size[0] // 3, 1 * sim.grid_size[1] // 4], 20, 10),
                HeatSource(sim, [(sim.grid_size[0] // 3), (sim.grid_size[1] // 4)], 8, -5)]
    
    # add all instantiated objects to SimSpace
    sim.reset(producers + consumers, emitters)
    return sim


def get_sim_state(simulator):
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
           gridspacesInformation.append(simulator.layer_system.get_gridspace([i,j]).get_properties())
    # return information of all gridspaces
    return jsonify(gridspacesInformation)
