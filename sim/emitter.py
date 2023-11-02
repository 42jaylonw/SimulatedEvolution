import numpy as np
import math

from sim.layer_dictionary import LAYER_DICT, NUM_LAYERS

# "Abstract" class
class Emitter():
    layer: int
    position: np.ndarray
    emit_range: int
    emit_val: float

    """
    params:
        sim = the SimSpace object the Emitter is a part of
        pos = where the emitter is in grid space
        e_range = how far out will the emitter reach?
        e_val = how much should each space within e_range be incremented by?
    """
    def __init__(self, sim, pos, e_range, e_val):
        self.layer = None
        self.sim = sim
        self.position = np.random.randint(sim.grid_size)
        self.position[0] = np.clip(pos[0], 0, self.sim.grid_size[0] - 1)
        self.position[1] = np.clip(pos[1], 0, self.sim.grid_size[1] - 1)
        self.emit_range = e_range
        self.emit_val = e_val

    def move_to_pos(self, new_pos):
        self.position[0] = np.clip(new_pos[0], 0, self.sim.grid_size[0] - 1)
        self.position[1] = np.clip(new_pos[1], 0, self.sim.grid_size[1] - 1)

    """
    Update by radiating outwards in a circle from the center
    Note: Walls obstruct emitters
    """
    def step(self):
        for angle in range(0, 360, 5):
            for r in range(0, self.emit_range, 1):
                x = int(round(r * math.sin(math.radians(angle)) + self.position[0]))
                y = int(round(r * math.cos(math.radians(angle)) + self.position[1]))
                if self.sim.is_pos_out_of_bounds([x, y]) or not self.sim.is_pos_layer_empty("Wall", [x, y]):
                    break
                else:
                    self.sim.increment_pos_layer(self.layer, [x, y], self.emit_val)
        pass

    @property
    def grid_pos(self):
        assert np.all(0 <= self.position) and np.all(self.position < self.sim.grid_size)
        return int(self.sim.grid_size[1] - self.position[1] - 1), int(self.position[0])

# Light Layer (layer 5)
class LightSource(Emitter):
    brightness: float # unused for now

    def __init__(self, sim, pos, e_range, e_val):
        super().__init__(sim, pos, e_range, e_val)
        self.layer = "Light"

# Temperature Layer (layer 6)
class HeatSource(Emitter):
    max_heat: float # unused for now

    def __init__(self, sim, pos, e_range, e_val):
        super().__init__(sim, pos, e_range, e_val)
        self.layer = "Temperature"