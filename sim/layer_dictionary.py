LAYER_DICT = {
    # grid : 0
    "Producer": 1,
    "Consumer": 2,
    "Wall": 3,
    "Elevation": 4,
    "Light": 5,
    "Temperature": 6
}
NUM_LAYERS = len(LAYER_DICT) + 1

MIN_BRIGHTNESS = 0
MAX_BRIGHTNESS = 100

MIN_TEMPERATURE = -100
MAX_TEMPERATURE = 100

MIN_ELEVATION = -100
MAX_ELEVATION = 100