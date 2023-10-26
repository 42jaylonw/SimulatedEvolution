import toml
import numpy as np

CONFIG = toml.load("./config/simulation.toml")


# todo： [
#  abstract position,
#  vision
#  ]

class Creature:
    def __init__(self, sim):
        self.sim = sim
        self.position = np.random.randint(sim.grid_size)

    def step(self):
        pass

    @property
    def grid_pos(self):
        assert np.all(0 <= self.position) and np.all(self.position < self.sim.grid_size)
        return int(self.position[1]), int(self.sim.grid_size[1] - self.position[0] - 1)


class Producer(Creature):
    rgb = CONFIG['Producer']['rgb']

    def step(self):
        pass

    def sense


class Consumer(Creature):
    rgb = CONFIG['Consumer']['rgb']

    def __init__(self, sim):
        super().__init__(sim)
        self.speed = CONFIG['Consumer']['init_speed']
        self.sensory_range = CONFIG['Consumer']['sensory_range']

    def step(self):
        other_creatures = self.sim.creatures
        d_x = np.random.choice([-self.speed, self.speed], p=[0.5, 0.5])
        d_y = np.random.choice([-self.speed, self.speed], p=[0.5, 0.5])
        self.position[0] = np.clip(self.position[0] + d_x, 0, self.sim.grid_size[0] - 1)
        self.position[1] = np.clip(self.position[1] + d_y, 0, self.sim.grid_size[1] - 1)

    def sensePopulation(self):
        """ Obtains population count (of consumers) within sensory range. """

        # Obtains nearby information from function centered on the creature
        near_info = self.sim.get_near_info(self.position, self.sensory_range)

        # sums number of 1s in consumer layer of the array (if this is how the array works)
        num_consumers = np.sum(near_info[2])

        return num_consumers

    def blockedFwd(self, layer, prev_move):
        """ 
        Returns 1 if the creature's forward direction is blocked. Returns 0 if free.
        Orientation based on last moved direction. 

        Checks on the layer specified.
        """
        curr_pos = self.grid_pos

        if prev_move[0]:
			next_move[0] = curr_pos[0]
            next_move[1] = curr_pos[1] + 1
        elif prev_move[1]:
            next_move[0] = curr_pos[0] + 1
            next_move[1] = curr_pos[1]
        elif prev_move[2]:
            next_move[0] = curr_pos[0]
            next_move[1] = curr_pos[1] - 1
        elif prev_move[3]:
            next_move[0] = curr_pos[0] - 1
            next_move[1] = curr_pos[1]
        if self.sim.is_pos_layer_empty(layer, next_move):
            return False
        return True

    
    def blockedBack(self, layer, prev_move):
        """ 
        Returns if the creature's backward direction is blocked. Returns 0 if free.
        Orientation based on last moved direction. 

        Checks on the layer specified.
        """
        curr_pos = self.grid_pos

        if prev_move[0]:
            next_move[0] = curr_pos[0]
            next_move[0] = curr_pos[1] - 1
        elif prev_move[1]:
            next_move[0] = curr_pos[0] - 1
            next_move[1] = curr_pos[1]
        elif prev_move[2]:
            next_move[0] = curr_pos[0]
            next_move[1] = curr_pos[1] + 1
        elif prev_move[3]:
            next_move[0] = curr_pos[0] + 1
            next_move[1] = curr_pos[1]
        if self.sim.is_pos_layer_empty(layer, next_move):
            return False
        return True

    def blockedLeft(self, layer, prev_move):
        """ 
        Returns if the creature's relative left direction is blocked. Returns 0 if free.
        Orientation based on last moved direction. 

        Checks on the layer specified.
        """

        curr_pos = self.grid_pos

        if prev_move[0]:
            next_move[0] = curr_pos[0] - 1
            next_move[0] = curr_pos[1]
        elif prev_move[1]:
            next_move[0] = curr_pos[0]
            next_move[1] = curr_pos[1] + 1
        elif prev_move[2]:
            next_move[0] = curr_pos[0] + 1
            next_move[1] = curr_pos[1]
        elif prev_move[3]:
            next_move[0] = curr_pos[0]
            next_move[1] = curr_pos[1] - 1
        if self.sim.is_pos_layer_empty(layer, next_move):
            return False
        return True

    def blockedRight(self, prev_move):
        """ 
        Returns if the creature's relative right direction is blocked. Returns 0 if free.
        Orientation based on last moved direction. 

        Checks on the layer specified.
        """
        
        curr_pos = self.grid_pos

        if prev_move[0]:
            next_move[0] = curr_pos[0] + 1
            next_move[1] = curr_pos[1]
        elif prev_move[1]:
            next_move[0] = curr_pos[0]
            next_move[1] = curr_pos[1] - 1
        elif prev_move[2]:
            next_move[0] = curr_pos[0] - 1
            next_move[1] = curr_pos[1]
        elif prev_move[3]:
            next_move[0] = curr_pos[0] 
            next_move[1] = curr_pos[1] + 1
        if self.sim.is_pos_layer_empty(layer, next_move):
            return False
        return True
    
    def senseNearest():

