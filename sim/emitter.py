import numpy as np
import math

from sim.newlayersystem.LayerSystem import MIN_BRIGHTNESS, MAX_BRIGHTNESS, MIN_TEMPERATURE, MAX_TEMPERATURE, MIN_ELEVATION, MAX_ELEVATION

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
        emit_position_pairs = []
        emit_positions = []
        for angle in range(0, 360, 1):
            for r in range(0, self.emit_range, 1):
                x = int(round(r * math.sin(math.radians(angle)) + self.position[0]))
                y = int(round(r * math.cos(math.radians(angle)) + self.position[1]))
                emit_pos = [x, y]
                pos_dist_pair = (emit_pos, r)
                if self.layer_system.out_of_bounds(emit_pos) or self.layer_system.has_wall(emit_pos):
                    break
                if emit_pos not in emit_positions:
                    emit_positions.append(emit_pos)
                    emit_position_pairs.append(pos_dist_pair)
        return emit_position_pairs

    def step(self):
        pass

# Light Level
class LightSource(Emitter):
    brightness: int

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
            # TODO: make a gradual fading out of values towards 0
            self.layer_system.increment_light_level(emit_pos, cur_val)

# Temperature
class HeatSource(Emitter):
    max_heat: int

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
            cur_val = self.emit_val * ((self.emit_range - dist) / self.emit_range)
            self.layer_system.increment_temperature(emit_pos, cur_val)


# Elevation Layer (Experimental)
# "Mountains" / "Hills" / "Valleys" (negative e_vals)
# TODO: redesign how elevation gets set - emitters might not be a good fit behavior-wise
class HillEmitter(Emitter):
    max_elevation: int

    def __init__(self, sim, pos, e_range, e_val):
        super().__init__(sim, pos, e_range, e_val)
        self.layer = "Elevation"
        self.min_val = MIN_ELEVATION
        self.max_val = MAX_ELEVATION
        self.emit_val = np.clip(e_val, self.min_val, self.max_val) # WIP: will support negative values
