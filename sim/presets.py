PRODUCER_PRESETS = dict()

# WE can format the dictionaries to include species id like {"1" : [<species>, <genome>]}
CONSUMER_PRESET = {"1": ["07034df2","0109d0e6","120c92ee","110ae8ef"]}



def load_consumer_preset(PresetID):
    if PresetID not in CONSUMER_PRESET:
        return None
    return CONSUMER_PRESET[PresetID]

def load_conusmer_preset(PresetID):
    if PresetID not in PRODUCER_PRESETS:
        return None
    return PRODUCER_PRESETS