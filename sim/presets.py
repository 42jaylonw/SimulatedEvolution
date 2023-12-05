import pickle
from sim.creatures.comsumer import Consumer
from sim.creatures.producer import Producer
from sim.emitter import LightSource, HeatSource

PRESET_DIRECTORY_PATH = 'sim/preset_folder/'
PRODUCER_PRESETS = dict()

# WE can format the dictionaries to include species id like {"1" : [<species>, <genome>]}
CONSUMER_PRESET = {"1": ["07034df2","0109d0e6","120c92ee","110ae8ef"]}

SIM_PRESET = {"followers_and_leaders": [], "cat_and_mouse": [], "secret_room": [], "half-and-half": []}

def load_consumer_preset(PresetID):
    if PresetID not in CONSUMER_PRESET:
        return None
    return CONSUMER_PRESET[PresetID]

def load_producer_preset(PresetID):
    if PresetID not in PRODUCER_PRESETS:
        return None
    return PRODUCER_PRESETS


def save_simspace_to_file(sim, file_name):
    width = sim.grid_size[0]
    walls = []
    for i in range(width):
        for j in range(width):
           # access and append each gridspaces' properties
           if sim.layer_system.get_gridspace([i,j]).has_wall():
               walls.append([i,j])

    #walls = [grid_space.position for grid_space in sim.layer_system.grid_spaces if grid_space.has_wall()]
    emitters = sim.emitters

    emitter_data = [[type(emitter), emitter.position, emitter.emit_range, emitter.emit_val] for emitter in emitters]


    creatures = sim.creatures
    creature_data = [[type(creature), creature.position, creature.genome] for creature in creatures]

    
    sim_dictionary = {"walls": walls, "emitters": emitter_data, "creatures": creature_data}
    with open(PRESET_DIRECTORY_PATH + file_name + '.pkl', 'wb') as f:
        print("saving ", sim_dictionary)
        pickle.dump(sim_dictionary, f)
        f.close()
    # with open(PRESET_DIRECTORY_PATH + 'test_run.pkl', 'rb') as f:
    #     new_data = pickle.load(f)
    #     print(new_data)

def loadSimSpaceFromFile(simulation, filename):
    # open file
    with open(filename, 'rb') as f:
        preset_data = pickle.load(f)
        print("Loading preset: ", preset_data)
        # update simulation with preset data
        # replace walls 
        simulation.layer_system.clear_walls()
        for wall_position in preset_data["walls"]:
            simulation.layer_system.wall_add(wall_position)
        # Add creatures and emitters
        
        for creature in simulation.creatures:
            creature.remove()
        for emitter in simulation.emitters:
            emitter.remove()
        
        #simulation.reset([], ())
        for creature in preset_data["creatures"]:
            new_creature = None
            if creature[0] == 'Consumer':
                new_creature = Consumer(simulation, creature[1], creature[2])
            else:
                print(type(creature[1]), creature[2])
                new_creature = Producer(simulation, creature[1], creature[2])

        for emitter in preset_data["emitters"]:
            new_emitter = None
            if emitter[0] == 'LightSource':
                new_emitter = LightSource(simulation, emitter[1], emitter[2], emitter[3])
            else:
                new_emitter = HeatSource(simulation, emitter[1], emitter[2], emitter[3])
        

    return simulation




if __name__ == '__main__':

    with open(PRESET_DIRECTORY_PATH + 'test_run.pkl', 'rb') as f:
        new_data = pickle.load(f)
        print(new_data)
    #consumer_file = open(r'SimulatedEvolution\sim\preset_folder\testDump.pkl', 'wb')
    #merged_dictionary = CONSUMER_PRESET | SIM_PRESET
    #pickle.dump(merged_dictionary, consumer_file)
    #pickle.dump("hi", consumer_file)
    #consumer_file.close()

    