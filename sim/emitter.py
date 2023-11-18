import numpy as np
import math

from sim import GridUtils
from sim.newlayersystem.LayerSystem import MIN_BRIGHTNESS, MAX_BRIGHTNESS, MIN_TEMPERATURE, MAX_TEMPERATURE
from sim.newlayersystem.LayerSystem import MIN_ELEVATION, MAX_ELEVATION, MIN_PHEREMONE_STRENGTH, MAX_PHEREMONE_STRENGTH

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

        self.layer_system = sim.layer_system

        self.position = pos
        self.position[0] = np.clip(pos[0], 0, self.sim.grid_size[0] - 1)
        self.position[1] = np.clip(pos[1], 0, self.sim.grid_size[1] - 1)

        self.emit_range = e_range
        self.min_val = 0 # arbitrary value
        self.max_val = 0 # arbitrary value
        self.emit_val = e_val

        # Update the Layer System
        self.layer_system.emitter_enter(self.position, self)

    def move_to_pos(self, new_pos):
        # Update the Layer System
        self.layer_system.emitter_move(self.position, new_pos, self)
        # Move emitter pos
        self.position[0] = np.clip(new_pos[0], 0, self.sim.grid_size[0] - 1)
        self.position[1] = np.clip(new_pos[1], 0, self.sim.grid_size[1] - 1)


    def remove(self):
        # Remove reference from SimSpace emitters list
        if self in self.sim.emitters:
            self.sim.emitters.remove(self)
        # Update the Layer System
        self.layer_system.emitter_exit(self.position, self)
    """
    Update by radiating outwards in a circle from the center
    Note: Walls obstruct emitters
    """
    def get_emit_position_pairs(self):
        return GridUtils.get_circle_coord_dist_pairs(self.layer_system, self.position, self.emit_range, True)

    def step(self):
        pass

# Light Level
class LightSource(Emitter):
    def __init__(self, sim, pos, e_range, e_val):
        super().__init__(sim, pos, e_range, e_val)
        self.layer = "Light"
        self.min_val = MIN_BRIGHTNESS
        self.max_val = MAX_BRIGHTNESS
        self.emit_val = np.clip(e_val, self.min_val, self.max_val)

    def step(self):
        emit_pos_pairs = self.get_emit_position_pairs()
        cur_val = self.emit_val
        for emit_pos, dist in emit_pos_pairs:
            # TODO: make a universal decay coefficient rather than depend on individual emit strength + range
            cur_val = self.emit_val * ((self.emit_range - dist) / self.emit_range)
            self.layer_system.increment_light_level(emit_pos, cur_val)

# Temperature
class HeatSource(Emitter):
    def __init__(self, sim, pos, e_range, e_val):
        super().__init__(sim, pos, e_range, e_val)
        self.layer = "Temperature"
        self.min_val = MIN_TEMPERATURE
        self.max_val = MAX_TEMPERATURE
        self.emit_val = np.clip(e_val, self.min_val, self.max_val)

    def step(self):
        emit_pos_pairs = self.get_emit_position_pairs()
        cur_val = self.emit_val
        for emit_pos, dist in emit_pos_pairs:
            if dist == 0:
                cur_val = self.emit_val
            cur_val = self.emit_val * ((self.emit_range - dist) / self.emit_range)
            self.layer_system.increment_temperature(emit_pos, cur_val)