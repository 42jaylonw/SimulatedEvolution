import numpy as np
from . import Creature


class Consumer(Creature):

    def __init__(self, sim):
        super().__init__(sim)
        self.speed = sim.cfg['Consumer']['init_speed']
        self.curr_action = [0, 0]
        self.last_action = [0, 0]

    def step(self):
        other_creatures = self.sim.creatures
        move_dir = np.random.randint(0, 4)
        move_dirs = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        self.action_move(move_dirs[move_dir])

    def get_observation(self):
        observation = np.zeros(self.cfg['num_observations'])
        # block here
        observation[0] = ...
        observation[1] = ...
        observation[2] = ...
        observation[3] = ...
        observation[4] = self.sensePopulation()
        observation[5:7] = self.last_action
        # border distance north: formula is (dist from north border / grid height)^2
        observation[7] = ...
        # border distance east
        observation[8] = ...
        # border distance south
        observation[9] = ...
        # border distance west
        observation[10] = ...
        # nearest border distance
        observation[11] = ...
        # current location north: formula is (dist from south border / grid height)^2
        observation[12] = ...
        # current location east
        observation[13] = ...
        # current location south
        observation[14] = ...
        # current location west
        observation[15] = ...

    def sensePopulation(self):
        """ Obtains population count (of consumers) within sensory range. """

        # Obtains nearby information from function centered on the creature
        near_info = self.sim.get_near_info(self.position, self.sensory_range)

        # sums number of 1s in consumer layer of the array (if this is how the array works)
        num_consumers = np.sum(near_info[2])

        return num_consumers

    def senseNearest(self):
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
        self.last_action = self.curr_action
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
        self.curr_action = [d_x, d_y]

        if self.sim.is_pos_out_of_bounds(target_pos) or not self.sim.is_pos_layer_empty("Producer", target_pos):
            # Space is occupied: no change in position can be made in this direction
            if not self.sim.is_pos_out_of_bounds(target_pos) and not self.sim.is_pos_layer_empty("Wall", target_pos):
                print("PRODUCER blocking movement")
            d_x, d_y = 0, 0
            target_pos = self.position

        self.sim.increment_pos_layer("Consumer", self.position,
                                     -1)  # WIP - DELETE THIS IF REFRESH IN SIMSPACE USED INSTEAD

        # Update the creature's position to the target position
        # The clipping shouldn't be necessary, but just in case - clip the new position to be within bounds of sim space
        self.position[0] = np.clip(target_pos[0], 0, self.sim.grid_size[0] - 1)
        self.position[1] = np.clip(target_pos[1], 0, self.sim.grid_size[1] - 1)

        self.sim.increment_pos_layer("Consumer", self.position,
                                     1)  # WIP DELETE THIS IF REFRESH IN SIMSPACE USED INSTEAD

    # def blockedFwd(self, layer, prev_move):
    #     """
    #     Returns 1 if the creature's forward direction is blocked. Returns 0 if free.
    #     Orientation based on last moved direction.
    #
    #     Checks on the layer specified.
    #     """
    #     curr_pos = self.grid_pos
    #
    #     if prev_move[0]:
    #         next_move[0] = curr_pos[0]
    #         next_move[1] = curr_pos[1] + 1
    #     elif prev_move[1]:
    #         next_move[0] = curr_pos[0] + 1
    #         next_move[1] = curr_pos[1]
    #
    #     elif prev_move[2]:
    #         next_move[0] = curr_pos[0]
    #         next_move[1] = curr_pos[1] - 1
    #
    #     elif prev_move[3]:
    #         next_move[0] = curr_pos[0] - 1
    #         next_move[1] = curr_pos[1]
    #     if self.sim.is_pos_layer_empty(layer, next_move):
    #         return False
    #     return True
    #
    # def blockedBack(self, layer, prev_move):
    #     """
    #     Returns if the creature's backward direction is blocked. Returns 0 if free.
    #     Orientation based on last moved direction.
    #
    #     Checks on the layer specified.
    #     """
    #     curr_pos = self.grid_pos
    #
    #     if prev_move[0]:
    #         next_move[0] = curr_pos[0]
    #         next_move[0] = curr_pos[1] - 1
    #     elif prev_move[1]:
    #         next_move[0] = curr_pos[0] - 1
    #         next_move[1] = curr_pos[1]
    #     elif prev_move[2]:
    #         next_move[0] = curr_pos[0]
    #         next_move[1] = curr_pos[1] + 1
    #     elif prev_move[3]:
    #         next_move[0] = curr_pos[0] + 1
    #         next_move[1] = curr_pos[1]
    #     if self.sim.is_pos_layer_empty(layer, next_move):
    #         return False
    #     return True
    #
    # def blockedLeft(self, layer, prev_move):
    #     """
    #     Returns if the creature's relative left direction is blocked. Returns 0 if free.
    #     Orientation based on last moved direction.
    #
    #     Checks on the layer specified.
    #     """
    #
    #     curr_pos = self.grid_pos
    #
    #     if prev_move[0]:
    #         next_move[0] = curr_pos[0] - 1
    #         next_move[0] = curr_pos[1]
    #     elif prev_move[1]:
    #         next_move[0] = curr_pos[0]
    #         next_move[1] = curr_pos[1] + 1
    #     elif prev_move[2]:
    #         next_move[0] = curr_pos[0] + 1
    #         next_move[1] = curr_pos[1]
    #     elif prev_move[3]:
    #         next_move[0] = curr_pos[0]
    #         next_move[1] = curr_pos[1] - 1
    #     if self.sim.is_pos_layer_empty(layer, next_move):
    #         return False
    #     return True
    #
    # def blockedRight(self, prev_move):
    #     """
    #     Returns if the creature's relative right direction is blocked. Returns 0 if free.
    #     Orientation based on last moved direction.
    #
    #     Checks on the layer specified.
    #     """
    #
    #     curr_pos = self.grid_pos
    #
    #     if prev_move[0]:
    #         next_move[0] = curr_pos[0] + 1
    #         next_move[1] = curr_pos[1]
    #     elif prev_move[1]:
    #         next_move[0] = curr_pos[0]
    #         next_move[1] = curr_pos[1] - 1
    #     elif prev_move[2]:
    #         next_move[0] = curr_pos[0] - 1
    #         next_move[1] = curr_pos[1]
    #     elif prev_move[3]:
    #         next_move[0] = curr_pos[0]
    #         next_move[1] = curr_pos[1] + 1
    #     if self.sim.is_pos_layer_empty(layer, next_move):
    #         return False
    #     return True
