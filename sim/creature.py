import toml
import numpy as np


# todo： [
#  abstract position,
#  vision
#  ]
class Coorps:
    pass


class Creature:
    position: np.ndarray
    energy: float
    mass: float
    metabolism: float

    def __init__(self, sim):
        self.sim = sim
        self.rgb = sim.cfg[self.__class__.__name__]['rgb']
        self.position = np.random.randint(sim.grid_size)
        self.energy = 0.

    def step(self):
        pass

    @property
    def grid_pos(self):
        assert np.all(0 <= self.position) and np.all(self.position < self.sim.grid_size)
        return int(self.sim.grid_size[1] - self.position[1]), int(self.position[0] - 1)


class Producer(Creature):

    def step(self):
        pass


class Consumer(Creature):

    def __init__(self, sim):
        super().__init__(sim)
        self.speed = sim.cfg['Consumer']['init_speed']

    def step(self):
        other_creatures = self.sim.creatures
        d_x = np.random.choice([-self.speed, self.speed], p=[0.5, 0.5])
        d_y = np.random.choice([-self.speed, self.speed], p=[0.5, 0.5])
        self.position[0] = np.clip(self.position[0] + d_x, 0, self.sim.grid_size[0] - 1)
        self.position[1] = np.clip(self.position[1] + d_y, 0, self.sim.grid_size[1] - 1)
        move_dir = np.random.randint(0, 4)
        move_dirs = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        self.action_move(move_dirs[move_dir])
        # d_x = np.random.choice([-self.speed, self.speed], p=[0.5, 0.5])
        # d_y = np.random.choice([-self.speed, self.speed], p=[0.5, 0.5])
        # self.position[0] = np.clip(self.position[0] + d_x, 0, self.sim.grid_size[0] - 1)
        # self.position[1] = np.clip(self.position[1] + d_y, 0, self.sim.grid_size[1] - 1)

    def action_move(self, direction):
        """
            :Desc: Moves the creature by 1 space in the direction specified by the direction parameter.
                   Checks for collisions/out-of-bounds before moving and updates layer pos on the sim space grid
            :param:
                direction: list of 4 bools - each one corresponds to a direction. NOTE: Only one value can be set to 1!
        """
        d_x, d_y = 0, 0
        if direction[0]:
            # Up
            d_y = 1
        elif direction[1]:
            # Right
            d_x = 1
        elif direction[2]:
            # Down
            d_y = -1
        elif direction[3]:
            # Left
            d_x = -1

        target_pos = self.position + (d_x, d_y)

        if self.sim.is_pos_out_of_bounds(target_pos) or not self.sim.is_pos_layer_empty(self, target_pos):
            # Space is occupied: no change in position can be made in this direction
            d_x, d_y = 0, 0
            target_pos = self.position

        # Update the creature's old position to be empty at this layer
        # (POTENTIAL FUTURE BUG - THIS MIGHT CAUSE ISSUES IF OTHER CREATURE MOVES IN IMMEDIATELY AFTER)
        self.sim.update_pos_layer(self, self.position, 0)

        # Update the creature's position to the target position
        # The clipping shouldn't be necessary, but just in case - clip the new position to be within bounds of sim space
        self.position[0] = np.clip(target_pos[0], 0, self.sim.grid_size[0] - 1)
        self.position[1] = np.clip(target_pos[1], 0, self.sim.grid_size[1] - 1)

        # Update the sim space's grid to be "occupied" at the layer/pos moved to by this creature
        self.sim.update_pos_layer(self, self.position, 1)
