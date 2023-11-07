import numpy as np
import math

from sim.layer_dictionary import LAYER_DICT, NUM_LAYERS, MAX_BRIGHTNESS, MAX_TEMPERATURE, MAX_ELEVATION

# "Abstract" class
class Emitter():
    layer: int
    position: np.ndarray
    emit_range: int
    emit_val: int
    max_val: int

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
        self.position = pos
        self.position[0] = np.clip(pos[0], 0, self.sim.grid_size[0] - 1)
        self.position[1] = np.clip(pos[1], 0, self.sim.grid_size[1] - 1)
        #print(self.position)
        self.emit_range = e_range
        self.max_val = MAX_BRIGHTNESS # arbitrary value
        self.emit_val = e_val

    def move_to_pos(self, new_pos):
        self.position[0] = np.clip(new_pos[0], 0, self.sim.grid_size[0] - 1)
        self.position[1] = np.clip(new_pos[1], 0, self.sim.grid_size[1] - 1)

    """
    Update by radiating outwards in a circle from the center
    Note: Walls obstruct emitters
    """
    def step(self):
        for angle in range(0, 360, 1):
            cur_val = np.clip(self.emit_val, 0, MAX_BRIGHTNESS)

            for r in range(0, self.emit_range, 1):
                if r == 0:
                    self.sim.set_pos_layer(self.layer, self.position, max(self.emit_val, self.sim.get_pos_layer(self.layer, self.position)))
                    pass

                x = int(round(r * math.sin(math.radians(angle)) + self.position[0]))
                y = int(round(r * math.cos(math.radians(angle)) + self.position[1]))
                light_pos = [x ,y]

                #if not self.sim.is_pos_out_of_bounds([x, y]) and not self.sim.is_pos_layer_empty("Producer", [x, y]):
                #    break

                if self.sim.is_pos_out_of_bounds(light_pos) or not self.sim.is_pos_layer_empty("Wall", light_pos):
                    break
                else:
                    self.sim.set_pos_layer(self.layer, light_pos, max(cur_val, self.sim.get_pos_layer(self.layer, light_pos)))
        pass

    # @property
    # def grid_pos(self):
    #     assert np.all(0 <= self.position) and np.all(self.position < self.sim.grid_size)
    #     return int(self.sim.grid_size[1] - self.position[1] - 1), int(self.position[0])

# Light Layer
class LightSource(Emitter):
    brightness: int

    def __init__(self, sim, pos, e_range, e_val):
        super().__init__(sim, pos, e_range, e_val)
        self.layer = "Light"
        self.max_val = MAX_BRIGHTNESS
        self.emit_val = np.clip(e_val, 0, self.max_val)

# Temperature Layer
class HeatSource(Emitter):
    max_heat: int

    def __init__(self, sim, pos, e_range, e_val):
        super().__init__(sim, pos, e_range, e_val)
        self.layer = "Temperature"
        self.max_val = MAX_TEMPERATURE
        self.emit_val = np.clip(e_val, 0, self.max_val)

# Elevation Layer (Experimental)
# "Mountains" / "Hills" / "Valleys" (negative e_vals)
class HillEmitter(Emitter):
    max_elevation: int

    def __init__(self, sim, pos, e_range, e_val):
        super().__init__(sim, pos, e_range, e_val)
        self.layer = "Elevation"
        self.max_val = MAX_ELEVATION
        self.emit_val = np.clip(e_val, -self.max_val, self.max_val) # WIP: will support negative values
