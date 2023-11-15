import numpy as np
from . import Creature
class Producer(Creature):
    name = 'Producer'

    def step(self):
        pass

class new_Producer(Creature):
    name = 'new_Producer'

    def __init__(self, sim, genome):
        super().__init__(sim, genome)

        # TODO: hash values from genome
        self.ideal_temp = 60.0
        self.light_req = 0.25

        # growth rate determines how fast the creature grows
        # given ideal conditions
        self.growth_rate = .1

        # current_size is similar to a tracker for age
        # a creature grows to it's .size when current_size = 1.0
        self.current_size = 0.01

        self.fruit_bearer = False

    
    # use when calculating light absorption
    # for raw light levels, use will's refactored function
    def get_light_level(self, pos):
        # get list of producers at space in pool
        producer_list = self.sim.get_producers(pos)
        # get their sizes and add them up
        size_total = 0
        for (producer in producer_list):
            size_total += (producer.size * producer.current_size)
        # light level for the creature is (their size / size total) * light lvl
        ret = ((self.size * self.current_size) / size_total) * self.sim.get_light_level(pos)
        return ret

    def get_temp(self, pos):
        return self.sim.get_temperature(pos)

    # returns true on energy gain,false on no gained energy
    # values calculated before metabolizing
    def check_suff_energy(self):
        curr_temp = self.get_temp(self.position)
        curr_light = self.get_light_level(self.position)

        heat_diff = (curr_temp - self.ideal_temp)
        light_diff = (curr_light - self.light_req)
        
        if (heat_diff > 0.0) and (light_diff > 0.0):
            return 1

        # heat or light was insufficient, return false
        return 0

    # NOTE: copied from consumer metabolize, fix in accordance
    def producer_metabolize(self, climate=0.0):
        self.energy -= (self.current_size * 0.1) + (climate * 0.5)

    # producer_growth handles growth of a plant that is not max size
    def producer_growth(self):
        # stage 1: sprouting
        if (self.current_size < .51):
            self.current_size += (self.growth_rate * 3)
        # stage 2: budding
        elif (self.current_size < .91):
            self.current_size += (self.growth_rate * 2)
        # stage 3: flowering
        else:
            self.current_size += (self.growth_rate)

        # ensure current_size does not pass 1.0
        self.current_size = min(1.0, self.current_size)

    # producer_expansion is used to assess what neighboring tile would be best
    # returns an array with [(score of space), x, y]
    def producer_expansion(self, x, y):
        ret = [0, x, y]

        # tile_score is our running score for the tile
        # as a candidate for growth
        tile_score = 0.0

        # add based on light and heat values
        tile_score += self.get_temp(x, y)
        tile_score = tile_score * self.get_light_level(x, y) * 100

        ret[0] = int(tile_score)

        return ret

    def step(self):
        # not sure what this line does ???
        if self.sim.is_pos_layer_empty("Producer", self.position):
            self.sim.increment_pos_layer("Producer", self.position, 1)

        # check if light and temp are sufficient for growth
        if (self.check_suff_energy()):
            # if current size is not 1.0, grow in size
            # grow differently based on size percentage
            # 0-50, 51-90, 91-100, each with different rate
            if (self.current_size < 1.0):
                self.producer_growth()

            # elif current size is 1.0, reproduce
            # if fruit bearer, grow fruit on curr space
            # if not, grow plant in most optimal neighbor
            elif (self.current_size == 1.0):
                # fruit bearer
                if (self.fruit_bearer):
                    # create food object at position
                    # note multiple food objects can occupy this position
                    # food object needs to have species ID so they can be eaten

                    # reset size 
                    # this prevents plant from producing a fruit every turn
                    # this can be changed to reduce energy 
                    self.current_size = 0.01

                else:
                    possible_expansion = []

                    for i in range(4):
                        target_pos = self.position

                        if (i < 2):
                            target_pos[0] = target_pos[0] + (pow(-1, i))
                            if not self.sim.is_pos_out_of_bounds(target_pos) and self.sim.is_pos_layer_empty("Wall", target_pos):
                                exp_tile = self.producer_expansion(target_pos[0], target_pos[1])
                                possible_expansion += exp_tile
                        elif (i >= 2):
                            target_pos[1] = target_pos[1] + (pow(-1, i))
                            if not self.sim.is_pos_out_of_bounds(target_pos) and self.sim.is_pos_layer_empty("Wall", target_pos):
                                exp_tile = self.producer_expansion(target_pos[0], target_pos[1])
                                possible_expansion += exp_tile

                    expansion = max(possible_expansion, key=lambda x: x[0])
                    # TODO: handle creation of new plant at expansion tile
                    
