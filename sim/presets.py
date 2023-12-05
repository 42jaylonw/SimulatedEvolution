import pickle

PRESET_DIRECTORY_PATH = '/SimulatedEvolution/sim/simPresetFiles'

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


def saveSimSpaceToFile(sim, file_name):
    walls = [grid_space.position for grid_space in sim.layer_system.grid_spaces if grid_space.has_wall()]
    emitters = sim.emitters
    creatures = sim.creatures
    
    
    sim_dictionary = {"walls": walls, "emitters": emitters, "creatures": creatures}
    #pickle.dump(sim_dictionary, file_name)





if __name__ == '__main__':
    consumer_file = open(PRESET_DIRECTORY_PATH + 'testDump.pkl', 'wb')
    #merged_dictionary = CONSUMER_PRESET | SIM_PRESET
    #pickle.dump(merged_dictionary, consumer_file)
    pickle.dump("hi", consumer_file)
    consumer_file.close()

    open_test_file = open(PRESET_DIRECTORY_PATH + 'testDump.pkl', 'rb')
    new_data = pickle.load(open_test_file)
    print(new_data)