import numpy as np
import math

from sim.layer_dictionary import LAYER_DICT, NUM_LAYERS, MAX_BRIGHTNESS, MAX_TEMPERATURE, MAX_ELEVATION
from sim.newlayersystem.LayerSystem import LayerSystem


# "Abstract" class
# TODO: get rid of "max/min value" parameters - this gets handled in LayerSystem now
class Emitter():
    layer: int
    layer_system: LayerSystem #EXPERIMENTAL
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

        self.layer_system = sim.layer_system #EXPERIMENTAL

        self.position = pos
        self.position[0] = np.clip(pos[0], 0, self.sim.grid_size[0] - 1)
        self.position[1] = np.clip(pos[1], 0, self.sim.grid_size[1] - 1)
        #print(self.position)
        self.emit_range = e_range
        self.min_val = -MAX_BRIGHTNESS
        self.max_val = MAX_BRIGHTNESS # arbitrary value
        self.emit_val = e_val

        #EXPERIMENTAL
        self.layer_system.emitter_enter(self.position, self)

    def move_to_pos(self, new_pos):
        self.layer_system.emitter_move(self.position, new_pos, self)
        self.position[0] = np.clip(new_pos[0], 0, self.sim.grid_size[0] - 1)
        self.position[1] = np.clip(new_pos[1], 0, self.sim.grid_size[1] - 1)


    def remove(self):
        if self in self.sim.emitters:
            self.sim.emitters.remove(self)
        self.layer_system.emitter_exit(self.position, self) #EXPERIMENTAL
    """
    Update by radiating outwards in a circle from the center
    Note: Walls obstruct emitters
    """
    def step(self):
        for angle in range(0, 360, 1):
            cur_val = np.clip(self.emit_val, self.min_val, self.max_val)
            for r in range(0, self.emit_range, 1):

                x = int(round(r * math.sin(math.radians(angle)) + self.position[0]))
                y = int(round(r * math.cos(math.radians(angle)) + self.position[1]))
                emit_pos = [x, y]

                #EXPERIMENTAL
                if self.layer_system.out_of_bounds(emit_pos) or self.layer_system.has_wall(emit_pos):
                    break
                else:
                    match self.layer:
                        case "Light":
                            self.layer_system.increment_light_level(emit_pos, cur_val)
                            continue
                        case "Temperature":
                            self.layer_system.increment_temperature(emit_pos, cur_val)
                            continue
                        case _:
                            continue

                #EXPERIMENTAL

                #if self.sim.is_pos_out_of_bounds(emit_pos) or not self.sim.is_pos_layer_empty("Wall", emit_pos):
                #    break
                #else:
                #    cur_total_val = 0.99 * (cur_val + self.sim.get_pos_layer(self.layer, emit_pos))
                #    self.sim.set_pos_layer(self.layer, emit_pos, np.clip(cur_total_val, self.min_val, self.max_val))

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
        self.min_val = 0
        self.max_val = MAX_BRIGHTNESS
        self.emit_val = np.clip(e_val, self.min_val, self.max_val)

# Temperature Layer
class HeatSource(Emitter):
    max_heat: int

    def __init__(self, sim, pos, e_range, e_val):
        super().__init__(sim, pos, e_range, e_val)
        self.layer = "Temperature"
        self.max_val = MAX_TEMPERATURE
        self.min_val = -self.max_val
        self.emit_val = np.clip(e_val, self.min_val, self.max_val)

# Elevation Layer (Experimental)
# "Mountains" / "Hills" / "Valleys" (negative e_vals)
# TODO: redesign how elevation gets set - emitters might not be a good fit behavior-wise
class HillEmitter(Emitter):
    max_elevation: int

    def __init__(self, sim, pos, e_range, e_val):
        super().__init__(sim, pos, e_range, e_val)
        self.layer = "Elevation"
        self.max_val = MAX_ELEVATION
        self.min_val = -self.max_val
        self.emit_val = np.clip(e_val, self.min_val, self.max_val) # WIP: will support negative values
