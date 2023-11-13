import numpy as np
from . import Creature

MOVE_DICT = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]


class Consumer(Creature):
    name = 'Consumer'

    def __init__(self, sim, genome=None):
        super().__init__(sim, genome)
        self.speed = sim.cfg['Consumer']['init_speed']
        self.sensory_range = sim.cfg['Consumer']['sensory_range']
        self.curr_action = [0, 0]
        self.last_action = [0, 0]
        self.move_cost = 0.0

    def step(self):
        obs = self.get_observation()
        action = np.argmax(self.behavior_system.predict(obs))
        self.action_move(action)
        self.energy_bar.consume_energy(self.move_cost)
        self.energy_bar.age_tick()
        if self.energy_bar.is_empty():
            self.die()

    def die(self):
        # self.sim.creatures -= this
        if self in self.sim.creatures:
            self.sim.creatures.remove(self)
        self.sim.increment_pos_layer("Consumer", self.position, -1)

    def get_observation(self):

        observation = np.zeros(self._cfg['num_observations'])
        # block here
        observation[0] = self.blockedFwd()
        observation[1] = self.blockedBack()
        observation[2] = self.blockedLeft()
        observation[3] = self.blockedRight()
        observation[4] = self.sensePopulation()
        observation[5:7] = self.last_action
        # border distance north: formula is (dist from north border / grid height)^2
        observation[7] = self.distBorderNorth()
        # border distance east
        observation[8] = self.distBorderEast()
        # border distance south
        observation[9] = self.distBorderSouth()
        # border distance west
        observation[10] = self.distBorderWest()
        # nearest border distance
        observation[11] = self.nearestBorderDist()
        # current location north: formula is (dist from south border / grid height)^2
        observation[12] = self.currLocNorth()
        # current location east
        observation[13] = self.currLocEast()
        # current location south
        observation[14] = self.currLocSouth()
        # current location west
        observation[15] = self.currLocWest()

        return observation

    def distBorderNorth(self):
        curr_pos = self.position
        grid_y = self.sim.grid_size[1]
        return pow((curr_pos[1] / grid_y), 2)

    def distBorderSouth(self):
        curr_pos = self.position
        grid_y = self.sim.grid_size[1]
        return pow(((grid_y - curr_pos[1]) / grid_y), 2)

    def distBorderEast(self):
        curr_pos = self.position
        grid_x = self.sim.grid_size[0]
        return pow(((grid_x - curr_pos[0]) / grid_x), 2)

    def distBorderWest(self):
        curr_pos = self.position
        grid_x = self.sim.grid_size[0]
        return pow((curr_pos[0] / grid_x), 2)

    def nearestBorderDist(self):
        curr_pos = self.position
        grid_x = self.sim.grid_size[0]
        grid_y = self.sim.grid_size[1]
        return max(curr_pos[1], grid_y - curr_pos[1], curr_pos[0], grid_x - curr_pos[0])

    def currLocNorth(self):
        curr_pos = self.position
        grid_y = self.sim.grid_size[1]
        return pow(((grid_y - curr_pos[1]) / grid_y), 2)

    def currLocSouth(self):
        curr_pos = self.position
        grid_y = self.sim.grid_size[1]
        return pow((curr_pos[1] / grid_y), 2)

    def currLocEast(self):
        curr_pos = self.position
        grid_x = self.sim.grid_size[0]
        return pow((curr_pos[0] / grid_x), 2)

    def currLocWest(self):
        curr_pos = self.position
        grid_x = self.sim.grid_size[0]
        return pow((curr_pos[0] / grid_x), 2)

    def sensePopulation(self):
        """ Obtains population count (of consumers) within sensory range. """

        # Obtains nearby information from function centered on the creature
        near_info = self.sim.get_near_info(self.position, self.sensory_range)

        # sums number of 1s in consumer layer of the array (if this is how the array works)
        num_consumers = np.sum(near_info[2])

        return num_consumers

    def senseNearest(self):
        move_dir = np.random.randint(0, 4)
        self.action_move(move_dir)
        # d_x = np.random.choice([-self.speed, self.speed], p=[0.5, 0.5])
        # d_y = np.random.choice([-self.speed, self.speed], p=[0.5, 0.5])
        # self.position[0] = np.clip(self.position[0] + d_x, 0, self.sim.grid_size[0] - 1)
        # self.position[1] = np.clip(self.position[1] + d_y, 0, self.sim.grid_size[1] - 1)

    def action_move(self, action: int):
        """
            :Desc: Moves the creature by 1 space in the direction specified by the direction parameter.
                   Checks for collisions/out-of-bounds before moving and updates layer pos on the sim space grid
            :param:
                direction: list of 4 bools - each one corresponds to a direction. NOTE: Only one value can be set to 1!
        """
        direction = MOVE_DICT[action]
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
        
        self.move_cost = 0.0
        # TO-DO -- grab elevation from sim space on layer
        current_elevation = 0.0
        target_elevation = 0.0
        self.move_cost = self.energy_bar.movement_cost(current_elevation, target_elevation, 1.0)

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

    def blockedFwd(self):
        """
        Returns 1 if the creature's forward direction is blocked by any creature or a wall or is out of bounds. Returns 0 if free.
        Orientation based on last moved direction.
        """
        last_act = self.last_action
        target_pos = self.position
        target_pos[0] += last_act[0]
        target_pos[1] += last_act[1]
        return self.check_empty(target_pos)

    def blockedBack(self):
        """
        Returns if the creature's backward direction is blocked by any creature of a wall or is out of bounds. Returns 0 if free.
        Orientation based on last moved direction.
        """
        last_act = self.last_action
        target_pos = self.position
        target_pos[0] -= last_act[0]
        target_pos[1] -= last_act[1]
        return self.check_empty(target_pos)

    def blockedLeft(self):
        """
        Returns if the creature's relative left direction is blocked by any creature or a wall or is out of bounds. Returns 0 if free.
        Orientation based on last moved direction.
        """
        last_act = self.last_action
        target_pos = self.position
        target_pos[0] -= last_act[1]
        target_pos[1] += last_act[0]
        return self.check_empty(target_pos)

    def blockedRight(self):
        """
        Returns if the creature's relative right direction is blocked by any creature or a wall or is out of bounds. Returns 0 if free.
        Orientation based on last moved direction.
        """

        last_act = self.last_action
        target_pos = self.position
        target_pos[0] += last_act[1]
        target_pos[1] -= last_act[0]
        return self.check_empty(target_pos)

    def check_empty(self, target_pos):
        return int(not all([self.sim.is_pos_layer_empty(layer, target_pos)
                            for layer in ["Wall", "Producer", "Consumer"]]))
    
    def metabolize(self, activity=0.0, climate=0.0):
        """
        Subtract Consumer's energy by the sum of activity, climate, and 10% of its size\n
        params:
            activity = added energy cost associated with movement

            climate = added energy cost based on the climate layer that the creature resides in
        """
        self.energy -= (self.size * 0.1) + activity + (climate * 0.5)

    def consume(self, energy=0):
        """
        Increment a Creature's energy by a specified amount\n
        param:
            energy = energy to add to Creature's current energy level 
        Notes:
            Only accepts positive energy values
        """
        if energy < 0: 
            raise Exception(f"Cannot Consume {energy} energy")
        self.energy += energy
