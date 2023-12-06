PRODUCER_PRESETS = dict()

# WE can format the dictionaries to include species id like {"1" : [<species>, <genome>]}
CONSUMER_PRESET = {"1": ["01054df2","0d0bd0e6","120492ee","0601e8ef"]}

SIM_PRESET = {"followers_and_leaders": [], "cat_and_mouse": [], "secret_room": [], "half-and-half": []}

def load_consumer_preset(PresetID):
    if PresetID not in CONSUMER_PRESET:
        return None
    return CONSUMER_PRESET[PresetID]

def load_producer_preset(PresetID):
    if PresetID not in PRODUCER_PRESETS:
        return None
    return PRODUCER_PRESETS