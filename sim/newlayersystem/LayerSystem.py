import numpy as np
import math

from sim import GridUtils
from sim.pheremone import Pheremone
from sim.creatures.comsumer import Consumer
from sim.creatures.producer import Producer

# Global LayerSystem Constants
MIN_BRIGHTNESS = 0
MAX_BRIGHTNESS = 100

MIN_TEMPERATURE = 0
MAX_TEMPERATURE = 100

MIN_ELEVATION = -100
MAX_ELEVATION = 100

MIN_PHEREMONE_STRENGTH = 0
MAX_PHEREMONE_STRENGTH = 100
PHEREMONE_DECAY = 0.5

# Component Used by SimSpace to keep track of layers and data at all positions in the SimSpace
class LayerSystem():
    def __init__(self, sim_dim):
        self.dimensions = sim_dim
        self.grid_spaces = [[GridSpace(self, [x, y]) for y in range(sim_dim[0])] for x in range(sim_dim[1])]

    # step() function gets called every SimSpace step
    def step(self, decayPheromones=True):
        # Clear/update layer values
        self.clear_emitter_values()
        if decayPheromones:
            self.decay_pheromones()

    # Called every step() to refresh / update temperature and light values, decay pheremone values
    def clear_emitter_values(self):
        for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1]):
                self.grid_spaces[x][y].set_light_level(0)
                self.grid_spaces[x][y].set_temperature(0)
    
    def decay_pheromones(self):
          for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1]):
                self.grid_spaces[x][y].decay_pheremones()

    def add_pheremone(self, pos, pheremone):
        assert not self.out_of_bounds(pos)
        self.get_gridspace(pos).add_pheremone(pheremone)

    # Gets rid of every wall in the SimSpace
    def clear_walls(self):
        for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1]):
                self.grid_spaces[x][y].wall_remove()

    # Returns the GridSpace object at the specified position
    # Output type: GridSpace
    def get_gridspace(self, pos):
        assert not self.out_of_bounds(pos)
        return self.grid_spaces[pos[0]][pos[1]]
    
    # Returns the dimensions of the SimSpace
    def get_dimensions(self):
        return self.dimensions

    # Returns the light value at the specified position
    # Output type: float
    def get_light_level(self, pos):
        assert not self.out_of_bounds(pos)
        return self.get_gridspace(pos).get_light_level()

    # Returns the temperature value at the specified position
    # Output type: float
    def get_temperature(self, pos):
        assert not self.out_of_bounds(pos)
        return self.get_gridspace(pos).get_temperature()

    # Returns the elevation value at the specified position
    # Output type: float
    def get_elevation(self, pos):
        assert not self.out_of_bounds(pos)
        return self.get_gridspace(pos).get_elevation()

    # Returns the total number of creatures (consumers + producers) at the specified position
    # Output type: int
    def get_num_creatures(self, pos):
        assert not self.out_of_bounds(pos)
        return self.get_gridspace(pos).get_num_creatures()

    # Returns the total number of consumers at the specified position
    # Output type: int
    def get_num_consumers(self, pos):
        assert not self.out_of_bounds(pos)
        return self.get_gridspace(pos).get_num_consumers()

    # Returns the total number of producers at the specified position
    # Output type: int
    def get_num_producers(self, pos):
        assert not self.out_of_bounds(pos)
        return self.get_gridspace(pos).get_num_producers()

    # Returns a list of all creatures (consumers + producers) at the specified position
    # Output type: List [] of Creature objects
    def get_creatures(self, pos):
        assert not self.out_of_bounds(pos)
        return self.get_gridspace(pos).get_creatures()

    # Returns a list of all consumers at the specified position
    # Output type: List [] of Consumer objects
    def get_consumers(self, pos):
        assert not self.out_of_bounds(pos)
        return self.get_gridspace(pos).get_consumers()

    # Returns a list of all producers at the specified position
    # Output type: List [] of Producer objects
    def get_producers(self, pos):
        assert not self.out_of_bounds(pos)
        return self.get_gridspace(pos).get_producers()

    # Returns whether there is a wall at the specified position (True if there is a wall, False if no wall)
    # Output type: bool
    def has_wall(self, pos):
        assert not self.out_of_bounds(pos)
        return self.get_gridspace(pos).has_wall()

    # Returns a list of all emitters at the specified position
    # Output type: List [] of Emitter objects
    def get_emitters(self, pos):
        assert not self.out_of_bounds(pos)
        return self.get_gridspace(pos).get_emitters()

    # Returns a list of all pheremones present at the specified position
    # Output type: List [] of Pheremone objects
    def get_pheremones(self, pos):
        assert not self.out_of_bounds(pos)
        return self.get_gridspace(pos).get_pheremones()

    # Sets the light value at the specified position
    # Input parameter val should be type float
    def set_light_level(self, pos, val):
        assert not self.out_of_bounds(pos)
        return self.get_gridspace(pos).set_light_level(val)

    # Sets the temperature value at the specified position
    # Input parameter val should be type float
    def set_temperature(self, pos, val):
        assert not self.out_of_bounds(pos)
        return self.get_gridspace(pos).set_temperature(val)

    # Sets the elevation value at the specified position
    # Input parameter val should be type float
    def set_elevation(self, pos, val):
        assert not self.out_of_bounds(pos)
        return self.get_gridspace(pos).set_elevation(val)

    # Increments the light value at the specified position
    # Input parameter val should be type float
    def increment_light_level(self, pos, val):
        assert not self.out_of_bounds(pos)
        return self.get_gridspace(pos).increment_light_level(val)

    # Increments the temperature value at the specified position
    # Input parameter val should be type float
    def increment_temperature(self, pos, val):
        assert not self.out_of_bounds(pos)
        return self.get_gridspace(pos).increment_temperature(val)

    # Increments the elevation value at the specified position
    # Input parameter val should be type float
    def increment_elevation(self, pos, val):
        assert not self.out_of_bounds(pos)
        return self.get_gridspace(pos).increment_elevation(val)

    # Appends creature to the GridSpace creatures list at the specified position
    # This function should be called by the Creature when it is spawned
    def creature_enter(self, pos, creature):
        # print("CREATURE ENTER: ", pos)
        assert not self.out_of_bounds(pos)
        self.get_gridspace(pos).creature_enter(creature)

    # Removes creature from the GridSpace creatures list at the specified position
    # This function should be called by the Creature when it gets removed from the SimSpace
    def creature_exit(self, pos, creature):
        assert not self.out_of_bounds(pos)
        self.get_gridspace(pos).creature_exit(creature)

    # Removes creature from GridSpace at pos1 and Appends it to the GridSpace at pos2
    # This function should be called by the Creature whenever it updates its position
    # Handles the event of a Creature moving from position "pos1" to position "pos2"
    def creature_move(self, pos1, pos2, creature):
        assert not self.out_of_bounds(pos1) and not self.out_of_bounds(pos2)
        self.creature_exit(pos1, creature)
        self.creature_enter(pos2, creature)

    # Adds a wall to the specified position
    def wall_add(self, pos):
        assert not self.out_of_bounds(pos)
        self.get_gridspace(pos).wall_add()

    # Removes the wall from the specified position
    def wall_remove(self, pos):
        assert not self.out_of_bounds(pos)
        self.get_gridspace(pos).wall_remove()

    # Appends the Emitter to the GridSpace emitters list at the specified position
    # This function should be called by the Emitter when it is spawned
    def emitter_enter(self, pos, emitter):
        assert not self.out_of_bounds(pos)
        self.get_gridspace(pos).creature_enter(emitter)

    # Removes emitter from the GridSpace emitters list at the specified position
    # This function should be called by the Emitter when it gets removed from the SimSpace
    def emitter_exit(self, pos, emitter):
        assert not self.out_of_bounds(pos)
        self.get_gridspace(pos).emitter_exit(emitter)

    # Removes emitter from GridSpace at pos1 and Appends it to the GridSpace at pos2
    # This function should be called by the Emitter whenever it updates its position
    # Handles the event of an Emitter moving from position "pos1" to position "pos2"
    def emitter_move(self, pos1, pos2, emitter):
        assert not self.out_of_bounds(pos1) and not self.out_of_bounds(pos2)
        self.emitter_exit(pos1, emitter)
        self.emitter_enter(pos2, emitter)
    
    def empty_space(self, pos):
        self.get_gridspace(pos).empty_space()

    # Checks whether the position is out of bounds or not (True if out of bounds, False if within bounds)
    # Output: bool
    def out_of_bounds(self, pos):
        """
            :param:
                pos: [x, y] position that is checked to see if outside of bounds
            :return:
                True: pos is outside of bounds of sim space
                False: pos is within bounds of sim space
        """
        return GridUtils.out_of_bounds(self.dimensions, pos)
    
    # Debug function to print properties of every GridSpace in the LayerSystem
    def print(self):
        for i in range(len(self.grid_spaces)):
            for j in range(len(self.grid_spaces[i])):
                grid_space = self.get_gridspace([i, j])
                print(grid_space.get_properties())
  

# Represents a single coordinate in the SimSpace.
# Contains all data at the position, including environmental values and all Creatures, Emitters that occupy its space
# Note: The descriptions of most these getter/setter functions are documented above in LayerSystem's functions
#       GridSpace can be called and then these functions can be accessed, but it is better to call them through LayerSystem
#       since it is funtionally the same and has additional helper functions
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
        self.pheremones = []

    def empty_space(self):
        self.wall_remove()
        self.empty_all_creatures()
        self.empty_all_emitters()

    def empty_all_creatures(self):
        self.creatures = []
        self.consumers = []
        self.producers = []
    
    def empty_all_emitters(self):
        self.emitters = []

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
    
    def get_pheremones(self):
        return self.pheremones

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
        if creature is None:
            return

        # Handles the specific type (Consumer/Producer) internally
        self.creatures.append(creature)
        if type(creature) == Consumer:
            self.consumers.append(creature)
        elif type(creature) == Producer:
            self.producers.append(creature)

    def creature_exit(self, creature):
        # If the creature has not yet been assigned to a position, do not perform exit
        # Note: this may cause issues if the creature position is not perfectly mapped to the layer system (which should not happen)
        if creature is None:
            return

        if creature.position is None:
            return
        if creature not in self.creatures:
            return
        # Handles the specific type (Consumer/Producer) internally
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

    def add_pheremone(self, pheremone):
        affected_pheremone = None
        for p in self.pheremones:
            if p.source.species_id == pheremone.source.species_id:
                affected_pheremone = p
        
        if affected_pheremone is None:
            self.pheremones.append(pheremone)
        else:
            affected_pheremone.strength += pheremone.strength
    
    def decay_pheremones(self):
        for p in self.pheremones:
            p.strength = math.floor(p.strength * PHEREMONE_DECAY) # WIP - this might need to be changed to linear decay
            # Remove pheremones if their strength is 0
            if p.strength == 0:
                self.pheremones.remove(p)

    # Returns a dictionary of the properties (WIP - this does not return all properties yet) at this GridSpace
    def get_properties(self, includeImages=False):
        if includeImages:
             return  {"position": self.position,
                "consumerCount": self.get_num_consumers(),
                "producerCount": self.get_num_producers(),
                "isWall": self.has_a_wall,
                "temperature": np.int16(self.temperature_val).item(),
                "light": np.int16(self.light_val).item(),
                "creatureImages": [(x.ref_id, x.image_data.tolist())  for x in self.get_consumers()]}
        return  {"position": self.position,
                "consumerCount": self.get_num_consumers(),
                "producerCount": self.get_num_producers(),
                "isWall": self.has_a_wall,
                "temperature": np.int16(self.temperature_val).item(),
                "light": np.int16(self.light_val).item(),
                "creatureImages": [x.ref_id  for x in self.get_consumers()]}
                # "creatureImages": [x.image_data.tolist()  for x in self.get_consumers()]}