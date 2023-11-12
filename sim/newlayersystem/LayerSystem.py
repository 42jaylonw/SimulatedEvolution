import numpy as np

from sim.creatures.comsumer import Consumer
from sim.creatures.producer import Producer

MIN_BRIGHTNESS = 0
MAX_BRIGHTNESS = 100

MIN_TEMPERATURE = -100
MAX_TEMPERATURE = 100

MIN_ELEVATION = -100
MAX_ELEVATION = 100
class LayerSystem():
    def __init__(self, sim_dim):
        self.dimensions = sim_dim
        # TODO: check if x and y need to be swapped
        self.grid_spaces = [[GridSpace(self, [x, y]) for y in range(sim_dim[0])] for x in range(sim_dim[1])]

    def step(self):
        # Clear emitters
        self.clear_emitter_values()

    def clear_emitter_values(self):
        for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1]):
                self.grid_spaces[x][y].set_light_level(0)
                self.grid_spaces[x][y].set_temperature(0)

    #Gets rid of every wall in the SimSpace
    def clear_walls(self):
        for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1]):
                self.grid_spaces[x][y].wall_remove()

    def get_gridspace(self, pos):
        assert not self.out_of_bounds(pos)
        return self.grid_spaces[pos[0]][pos[1]]

    def get_light_level(self, pos):
        assert not self.out_of_bounds(pos)
        return self.grid_spaces[pos[0]][pos[1]].get_light_level()

    def get_temperature(self, pos):
        assert not self.out_of_bounds(pos)
        return self.grid_spaces[pos[0]][pos[1]].get_temperature()

    def get_elevation(self, pos):
        assert not self.out_of_bounds(pos)
        return self.grid_spaces[pos[0]][pos[1]].get_elevation()

    def get_num_creatures(self, pos):
        assert not self.out_of_bounds(pos)
        return self.grid_spaces[pos[0]][pos[1]].get_num_creatures()

    def get_num_consumers(self, pos):
        assert not self.out_of_bounds(pos)
        return self.grid_spaces[pos[0]][pos[1]].get_num_consumers()

    def get_num_producers(self, pos):
        assert not self.out_of_bounds(pos)
        return self.grid_spaces[pos[0]][pos[1]].get_num_producers()

    def get_creatures(self, pos):
        assert not self.out_of_bounds(pos)
        return self.grid_spaces[pos[0]][pos[1]].get_creatures()

    def has_wall(self, pos):
        assert not self.out_of_bounds(pos)
        return self.grid_spaces[pos[0]][pos[1]].has_wall()

    def get_emitters(self, pos):
        assert not self.out_of_bounds(pos)
        return self.grid_spaces[pos[0]][pos[1]].get_emitters()

    def set_light_level(self, pos, val):
        assert not self.out_of_bounds(pos)
        return self.grid_spaces[pos[0]][pos[1]].set_light_level(val)
    def set_temperature(self, pos, val):
        assert not self.out_of_bounds(pos)
        return self.grid_spaces[pos[0]][pos[1]].set_temperature(val)
    def set_elevation(self, pos, val):
        assert not self.out_of_bounds(pos)
        return self.grid_spaces[pos[0]][pos[1]].set_elevation(val)
    def increment_light_level(self, pos, val):
        assert not self.out_of_bounds(pos)
        return self.grid_spaces[pos[0]][pos[1]].increment_light_level(val)
    def increment_temperature(self, pos, val):
        assert not self.out_of_bounds(pos)
        return self.grid_spaces[pos[0]][pos[1]].increment_temperature(val)
    def increment_elevation(self, pos, val):
        assert not self.out_of_bounds(pos)
        return self.grid_spaces[pos[0]][pos[1]].increment_elevation(val)

    def creature_enter(self, pos, creature):
        print("CREATURE ENTER: ", pos)
        assert not self.out_of_bounds(pos)
        self.grid_spaces[pos[0]][pos[1]].creature_enter(creature)

    def creature_exit(self, pos, creature):
        assert not self.out_of_bounds(pos)
        self.grid_spaces[pos[0]][pos[1]].creature_exit(creature)

    # move from pos1 to pos2
    def creature_move(self, pos1, pos2, creature):
        assert not self.out_of_bounds(pos1) and not self.out_of_bounds(pos2)
        print("MOVE FROM ", pos1, " TO: ", pos2)
        self.creature_exit(pos1, creature)
        self.creature_enter(pos2, creature)
        print("END MOVE!")

    def wall_add(self, pos):
        assert not self.out_of_bounds(pos)
        self.grid_spaces[pos[0]][pos[1]].wall_add()
    def wall_remove(self, pos):
        assert not self.out_of_bounds(pos)
        self.grid_spaces[pos[0]][pos[1]].wall_remove()
    def emitter_enter(self, pos, emitter):
        assert not self.out_of_bounds(pos)
        self.grid_spaces[pos[0]][pos[1]].creature_enter(emitter)
    def emitter_exit(self, pos, emitter):
        assert not self.out_of_bounds(pos)
        self.grid_spaces[pos[0]][pos[1]].emitter_exit(emitter)
    def emitter_move(self, pos1, pos2, emitter):
        assert not self.out_of_bounds(pos1) and not self.out_of_bounds(pos2)
        self.emitter_exit(pos1, emitter)
        self.emitter_enter(pos2, emitter)

    def out_of_bounds(self, pos):
        """
            :param:
                pos: [x, y] position that is checked to see if outside of bounds
            :return:
                True: pos is outside of bounds of sim space
                False: pos is within bounds of sim space
        """
        return pos[0] < 0 or pos[0] > self.dimensions[0] - 1 or pos[1] < 0 or pos[1] > self.dimensions[1] - 1
    
    
    def print(self):
        for grid_space in self.grid_spaces:
            print(grid_space.get_properties())
  


class GridSpace():
    layer_system: LayerSystem

    position: np.ndarray

    light_val: float
    temperature_val: float
    elevation_val: float
    has_a_wall: bool
    def __init__(self, layer_system, pos):
        self.layer_system = layer_system
        self.position = pos
        self.creatures = [] # consumers + producers
        self.consumers = [] # subset list of creatures
        self.producers = [] # subset list of creatures
        self.emitters = []
        self.light_val = 0
        self.temperature_val = 0
        self.elevation_val = 0
        self.has_a_wall = False


    def get_light_level(self):
        return self.light_val
    def get_temperature(self):
        return self.temperature_val
    def get_elevation(self):
        return self.elevation_val
    def get_num_creatures(self):
        return len(self.creatures)
    def get_num_consumers(self):
        return len(self.consumers)
    def get_num_producers(self):
        return len(self.producers)

    def get_creatures(self):
        return self.creatures

    def get_consumers(self):
        return self.consumers

    def get_producers(self):
        return self.producers

    def has_wall(self):
        return self.has_a_wall

    def get_emitters(self):
        return self.emitters

    def set_light_level(self, val):
        self.light_val = np.clip(val, MIN_BRIGHTNESS, MAX_BRIGHTNESS)

    def set_temperature(self, val):
        self.temperature_val = np.clip(val, MIN_TEMPERATURE, MAX_TEMPERATURE)

    def set_elevation(self, val):
        self.elevation_val = np.clip(val, MIN_ELEVATION, MAX_ELEVATION)

    def increment_light_level(self, inc):
        self.light_val = np.clip(self.light_val + inc, MIN_BRIGHTNESS, MAX_BRIGHTNESS)

    def increment_temperature(self, inc):
        self.temperature_val = np.clip(self.temperature_val + inc, MIN_TEMPERATURE, MAX_TEMPERATURE)

    def increment_elevation(self, inc):
        self.elevation_val = np.clip(self.elevation_val + inc, MIN_ELEVATION, MAX_ELEVATION)

    def creature_enter(self, creature):
        print("CREATURE ENTER")
        self.creatures.append(creature)
        if type(creature) == Consumer:
            self.consumers.append(creature)
        elif type(creature) == Producer:
            self.producers.append(creature)

    def creature_exit(self, creature):
        print("CREATURE EXIT at", self.position)
        self.creatures.remove(creature)
        if type(creature) == Consumer:
            self.consumers.remove(creature)
        elif type(creature) == Producer:
            self.producers.remove(creature)

    def wall_add(self):
        self.has_a_wall = True
    def wall_remove(self):
        self.has_a_wall = False
    def emitter_enter(self, emitter):
        self.emitters.append(emitter)
    def emitter_exit(self, emitter):
        self.emitters.remove(emitter)
    def get_properties(self):
        #"(position, numConsumer, numProduc, isWall, temperature)"
        return (self.position, self.get_num_consumers(), self.get_num_producers(), self.has_a_wall, np.int16(self.temperature_val).item())