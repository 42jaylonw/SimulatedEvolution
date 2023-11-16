import numpy as np


def rgb_mutation(original_rgb, species_code, total_species, delta=0.5, sign=(-1.0, 1.0, -1.0)):
    normalized_scale = species_code / total_species - 0.5
    new_rgb = np.clip(np.float32(original_rgb) + delta * np.float32(sign) * normalized_scale, 0.0, 1.0)
    return new_rgb
