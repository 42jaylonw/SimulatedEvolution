import numpy as np
from . import Creature
from sim import GridUtils
from sim.pheremone import Pheremone

PHEREMONE_EMIT_RANGE = 8 # WIP - arbitrary constant for now -
PHEREMONE_EMIT_STRENGTH = 80 # WIP - arbitrary constant for now -

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
        self.edible_consumers = sim.predation_table[self.species_id][0]
        self.edible_producers = sim.predation_table[self.species_id][1]

    def step(self):
        obs = self.get_observation()
        # if energy is sufficient to reproduce
        action = self.reproduction_protocol()
        # if reproduction protocol not active
        if action == -1:
            action = np.argmax(self.behavior_system.predict(obs))
        # self.die()
        self.action_hunt(action)
        self.energy_bar.consume_energy(self.move_cost)
        self.energy_bar.age_tick()
        if self.energy_bar.is_empty():
            # print(f"A creature of {self.species_id} has died")
            self.die()

    
    def reproduction_protocol(self):
        reproduce_thresh = 40
        if (self.energy_bar.current_energy >= reproduce_thresh):
            # if another creature on current space that is compatible
            for creature in self.sim.layer_system.get_consumers(self.position):
                if creature == self:
                    continue
                if creature.species_id == self.species_id and creature != self:
                    if creature.energy_bar.current_energy >= reproduce_thresh:
                        # reproduce
                        # TODO: make actual reproduction function
                        pass
            # else check for compatible creatures in sensory range
            potential_partners = self.sensePartners()
            if (len(potential_partners) == 0):
                # emit pheromone and predict regularly
                self.emit_pheremones()
                return -1
            else:
                for consumer in potential_partners:
                    if consumer.energy_bar.current_energy >= reproduce_thresh:
                        # move towards partner
                        action = np.argmax(self.move_towards(self.position, consumer.position))
                        return action
        return -1

    # move_towards takes in a starting point and ending point
    # returns the direction needed to move closest to target
    def move_towards(self, start, end):
        temp = start
        temp_n = [temp[0] - 1, temp[1]]
        move_n = [[1, 0, 0, 0], temp_n]
        temp_e = [temp[0], temp[1] + 1]
        move_e = [[0, 1, 0, 0], temp_e]
        temp_s = [temp[0] + 1, temp[1]]
        move_s = [[0, 0, 1, 0], temp_s]
        temp_w = [temp[0], temp[1] - 1]
        move_w = [[0, 0, 0, 1], temp_w]

        moves = [move_n, move_e, move_s, move_w]
        min_dist = 999
        min_dir = [0, 0, 0, 0]
        for move in moves:
            dist = np.linalg.norm(end - move[1])
            if dist < min_dist:
                min_dir = move[0]
                min_dist = dist

        return min_dir


    def die(self):
        # self.sim.creatures -= this
        if self in self.sim.creatures:
            self.sim.creatures.remove(self)

        self.layer_system.creature_exit(self.position, self)

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
        #near_info = self.sim.get_near_info(self.position, self.sensory_range)

        # sums number of 1s in consumer layer of the array (if this is how the array works)
        #num_consumers = np.sum(near_info[2])

        # EXPERIMENTAL - original code commented out above, the implementation below
        # should do the same job of counting the nearby consumers
        num_consumers = 0
        center = self.position
        length = self.sensory_range
        start_x = np.clip(center[0] - length, 0, self.sim.grid_size[0])
        end_x = np.clip(center[0] + length, 0, self.sim.grid_size[0])
        start_y = np.clip(center[1] - length, 0, self.sim.grid_size[1])
        end_y = np.clip(center[1] + length, 0, self.sim.grid_size[1])

        for x_pos in range(start_x, end_x):
            for y_pos in range(start_y, end_y):
                num_consumers += self.layer_system.get_num_consumers([x_pos, y_pos])
        # ---------

        return num_consumers

    def sensePartners(self):
        """ Obtains population count (of potential mates) within sensory range. """

        center = self.position
        length = self.sensory_range
        species = self.species_id
        start_x = np.clip(center[0] - length, 0, self.sim.grid_size[0])
        end_x = np.clip(center[0] + length, 0, self.sim.grid_size[0])
        start_y = np.clip(center[1] - length, 0, self.sim.grid_size[1])
        end_y = np.clip(center[1] + length, 0, self.sim.grid_size[1])

        # potential_mates stores a list of creatures that share a species ID
        # format is [creature, dist]
        potential_mates = []

        for x_pos in range(start_x, end_x):
            for y_pos in range(start_y, end_y):
                consumers = self.layer_system.get_consumers([x_pos, y_pos])
                for consumer in consumers:
                    if consumer == self:
                        continue
                    if consumer.species_id == species and consumer != self:
                        potential_mates = potential_mates + [consumer]
        return potential_mates
        # ---------

    def senseNearest(self):
        """
        Senses the location of the nearest of a specified object using 
        square "rings". Returns None if there are no creatures 
        within the sensory range, and returns the location of the 
        nearest creature(s) otherwise.
        """
        # TODO: NOTE: Right now, this only checks for the nearest producer. Need to implement functionality
        # where it can instead specify the type of creature or object it wants to find, esp. with regards to which species are edible to it.
        closest_locations = []

        # Check first if there is a producer on same square
        if self.layer_system.get_num_producers(self.position) > 0:
            return self.position

        for radius in range(1, self.sensory_range + 1):
            for dx in range(-radius, radius + 1):
                for dy in [-radius, radius]:
                    checked_pos = self.position
                    checked_pos[0] = checked_pos[0] + dx
                    checked_pos[1] = checked_pos[1] + dy
                    if not self.layer_system.out_of_bounds(checked_pos):
                        if self.layer_system.get_num_producers(checked_pos) > 0:
                            if len(closest_locations) == 0:
                                closest_locations.append(checked_pos)
                            elif np.linalg.norm(np.array(self.position) - np.array(checked_pos)) < np.linalg.norm(np.array(self.position) - np.array(closest_locations[0])):
                                closest_locations = [checked_pos]
                            elif np.linalg.norm(np.array(self.position) - np.array(checked_pos)) == np.linalg.norm(np.array(self.position) - np.array(closest_locations[0])):
                                closest_locations.append(checked_pos)
                                
            for dy in range(-radius + 1, radius):
                for dx in [-radius, radius]:
                    checked_pos = self.position
                    checked_pos[0] = checked_pos[0] + dx
                    checked_pos[1] = checked_pos[1] + dy
                    if not self.layer_system.out_of_bounds(checked_pos):
                        if self.layer_system.get_num_producers(checked_pos) > 0:
                            if len(closest_locations) == 0:
                                closest_locations.append(checked_pos)
                            elif np.linalg.norm(np.array(self.position) - np.array(checked_pos)) < np.linalg.norm(np.array(self.position) - np.array(closest_locations[0])):
                                closest_locations = [checked_pos]
                            elif np.linalg.norm(np.array(self.position) - np.array(checked_pos)) == np.linalg.norm(np.array(self.position) - np.array(closest_locations[0])):
                                closest_locations.append(checked_pos)

            if len(closest_locations) > 0:
                # return np.random.choice(closest_locations)
                # random.choice is not used to provide for more "consistent"
                # behavior when it comes to the nearest object.
                # This results in "preferred" directions when there is a tie
                # in distance
                print(f"closest location to {self.species_id} at {self.position} is {closest_locations[0]}")
                return closest_locations[0]

            if len(closest_locations) > 0:
                return np.random.choice(closest_locations)
        return None

    def senseWithinRange(self):
        positions_to_check = GridUtils.get_circle_coord_dist_pairs(self.layer_system, self.position, self.sensory_range)
        producer_positions = []
        for pos in positions_to_check:
            if self.layer_system.get_num_producers(pos[0]) > 0:
                producer_positions.append(pos)
        if len(producer_positions) <= 0:
            return None
        closest_pos = min(producer_positions, key=lambda x: x[1])
        return closest_pos[0]

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

        if self.layer_system.out_of_bounds(target_pos) or self.layer_system.has_wall(target_pos):
            # Space is blocked: no change in position can be made in this direction
            d_x, d_y = 0, 0
            target_pos = self.position
        
        current_elevation = self.layer_system.get_elevation(self.position)
        target_elevation = self.layer_system.get_elevation(target_pos)
        self.move_cost = self.energy_bar.movement_cost(current_elevation, target_elevation, 1.0)

        self.set_position(target_pos)

        # Update the Layer System
        #self.layer_system.creature_move(self.position, target_pos, self) # WIP
        # Update the creature's position to the target position
        #self.position = target_pos #WIP

    # TODO: finalize + test this implementation
    # WIP - consumer acts like an emitter onto the pheremone layer
    # Emit range + strength are defined by arbitrary constants for now
    def emit_pheremones(self):
        pheremone = Pheremone(PHEREMONE_EMIT_STRENGTH, self)
        emit_positions = GridUtils.get_circle_coord_dist_pairs(self.layer_system, self.position, PHEREMONE_EMIT_RANGE)
        for emit_pos in emit_positions:
            self.layer_system.add_pheremone(emit_pos[0], pheremone)

    def blockedFwd(self):
        """
        Returns 1 if the creature's forward direction is blocked by a wall or is out of bounds. Returns 0 if free.
        Orientation based on last moved direction.
        """
        last_act = self.last_action
        target_pos = self.position
        target_pos[0] += last_act[0]
        target_pos[1] += last_act[1]
        if not self.layer_system.out_of_bounds(target_pos):
            if self.layer_system.has_wall(target_pos):
                return 1
            else:
                return 0
        else:
            return 1

    def blockedBack(self):
        """
        Returns if the creature's backward direction is blocked by a wall or is out of bounds. Returns 0 if free.
        Orientation based on last moved direction.
        """
        last_act = self.last_action
        target_pos = self.position
        target_pos[0] -= last_act[0]
        target_pos[1] -= last_act[1]
        if not self.layer_system.out_of_bounds(target_pos):
            if self.layer_system.has_wall(target_pos):
                return 1
            else:
                return 0
        else:
            return 1

    def blockedLeft(self):
        """
        Returns if the creature's relative left direction is blocked by a wall or is out of bounds. Returns 0 if free.
        Orientation based on last moved direction.
        """
        last_act = self.last_action
        target_pos = self.position
        target_pos[0] -= last_act[1]
        target_pos[1] += last_act[0]
        if not self.layer_system.out_of_bounds(target_pos):
            if self.layer_system.has_wall(target_pos):
                return 1
            else:
                return 0
        else:
            return 1

    def blockedRight(self):
        last_act = self.last_action
        target_pos = self.position
        target_pos[0] += last_act[1]
        target_pos[1] -= last_act[0]
        if not self.layer_system.out_of_bounds(target_pos):
            if self.layer_system.has_wall(target_pos):
                return 1
            else:
                return 0
        else:
            return 1
    
    def metabolize(self, activity=0.0, climate=0.0):
        """
        Subtract Consumer's energy by the sum of activity, climate, and 10% of its size\n
        params:
            activity = added energy cost associated with movement

            climate = added energy cost based on the climate layer that the creature resides in
        """
        self.energy -= (self.size * 0.1) + activity + (climate * 0.5)
        # NOTE: Functionality already in self.energy_bar.consume_energy(act)

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
        # 
    
    def is_edible(self, creature):
        """
        Checks to see if a creature underneath is edible. (exists within edible tags)
        """
        # TODO: Need to check how to access
        return True

    
    # NOTE: temporarily adding the "otherwise" param to do a regular action-move if a creature is not detected
    def action_hunt(self, otherwise):
        """
        Hunts a creature down. Follows manhattan distance if a creature
        is detected. Follows nearest pheromone if pheromone is present 
        and no creature is detected, or if walls are detected.

        While hunting, if it moves onto the square of a creature it may eat
        it gains energy and the creature on that square dies.
        """
        # TODO: NOTE: Because senseNearest only returns the location of the nearest
        # producer, the action_hunt behavior does not currently include pheromone
        # tracking, as producers are completely stationary and do not use
        # pheromones.
        # senseLocation = self.senseNearest()
        senseLocation = self.senseWithinRange()
        if senseLocation is not None and not self.energy_bar.is_satiated():
            raw_x = senseLocation[0] - self.position[0]
            raw_y = senseLocation[1] - self.position[1]
            distToLoc_x = np.abs(raw_x)
            distToLoc_y = np.abs(raw_y)
            if distToLoc_x == 0 and distToLoc_y == 0:
                self.eat_on_square()
                print(f"a creature of {self.species_id} consumed food and its energy is now {self.energy_bar.current_energy}")
            elif distToLoc_x >= distToLoc_y:
                if raw_x > 0:
                    self.action_move(1)
                elif raw_x < 0:
                    self.action_move(3)
            elif distToLoc_x < distToLoc_y:
                if raw_y > 0:
                    self.action_move(0)
                elif raw_y < 0:
                    self.action_move(2)
        else:
            self.action_move(otherwise)
        # else:
            # get pheromones of tile above, below, to the right, and to the left (if not out of bounds)
            # go to tile with strongest pheromone from edible-tagged species
        
 
    def eat_on_square(self):
        """
        Eats a producer (should be expanded to all edible creatures)
        on the same square as the calling creature.
        If there is no creature to eat here, then does nothing.
        """
        # TODO: NOTE: I don't know anything about the "edible creatures" tag system
        # that's been floating around, so I'll hold off on implementing the 'eat edible creature'
        # check and make this function only consume a producer.
        yummy_produce = self.layer_system.get_producers(self.position)
        if len(yummy_produce) > 0:
            chosen_to_eat = np.random.choice(yummy_produce)
            print(f"{self.species_id} has chosen to eat {chosen_to_eat.species_id}, whose current energy is {chosen_to_eat.energy_bar.current_energy}")
            energy_gain_base = chosen_to_eat.energy_bar.current_energy * 0.10

            # a bonus to energy gain from consumption based on the size of the prey creature and the eating creature
            # this value is never greater than the eating creature's size
            energy_gain_sizeBonus = max((1.75 * chosen_to_eat.size), self.size)
            self.energy_bar.replenish_energy(energy_gain_base + energy_gain_sizeBonus)
            chosen_to_eat.die()
        else:
            print(f"a creature of (self.species_id) ate nothing")

    def reproduce(self, child_starting_energy=30):
        """
        Create a new creature at a space nearby.
        Also updates the parent's max energy. 
        """
        # senseLocation = self.senseNearest()
        # if senseLocation is not None:

