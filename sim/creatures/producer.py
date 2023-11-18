import numpy as np
from . import Creature

class Food():
    name = 'Food'

    def __init__(self, sim, genome=None):
        # TODO: hash from genome 
        self.saturation = 0.5
        self.seed_bearer = False
        self.genome = genome


class Producer(Creature):
    name = 'Producer'

    def __init__(self, sim, genome=None):
        super().__init__(sim, genome)

        if (self.genome == None):
            self.genome = self.GeneticAlgorithm.generate_prod_genome()

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
        producer_list = self.sim.layer_system.get_producers(pos)
        if len(producer_list) == 0:
            return self.sim.layer_system.get_light_level(pos)
        # get their sizes and add them up
        size_total = 0
        for producer in producer_list:
            size_total += (producer.size * producer.current_size)

        if size_total == 0:
            print("help")
            print(pos)
            print(producer_list)
        # light level for the creature is (their size / size total) * light lvl
        ret = ((self.size * self.current_size) / size_total) * self.sim.layer_system.get_light_level(pos)
        return ret

    def get_temp(self, pos):
        return self.sim.layer_system.get_temperature(pos)

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
    def producer_expansion(self, pos):
        ret = [0, pos[0], pos[1]]

        # tile_score is our running score for the tile
        # as a candidate for growth
        tile_score = 0.0

        # add based on light and heat values
        tile_score += self.get_temp(pos)
        tile_score = tile_score * self.get_light_level(pos) * 100

        ret[0] = int(tile_score)

        return ret


    def die(self):
        if self in self.sim.creatures:
            self.sim.creatures.remove(self)

        self.sim.layer_system.creature_exit(self.position, self)

    def step(self):
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
                # TODO: for fruit bearers, remember to kill fruits if plant dies
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
                            if not self.sim.layer_system.out_of_bounds(target_pos) and not self.sim.layer_system.has_wall(target_pos):
                                exp_tile = [self.producer_expansion(target_pos)]
                                possible_expansion += exp_tile
                        elif (i >= 2):
                            target_pos[1] = target_pos[1] + (pow(-1, i))
                            if not self.sim.layer_system.out_of_bounds(target_pos) and not self.sim.layer_system.has_wall(target_pos):
                                exp_tile = [self.producer_expansion(target_pos)]
                                possible_expansion += exp_tile

                    expansion = max(possible_expansion, key=lambda x: x[0])
                    # TODO: handle creation of new plant at expansion tile
                    new_genome = self.behavior_system.mutate_genome()
                    new_plant = self.__class__(self.sim, new_genome)
                    new_plant.set_position(expansion[1:3])
                    self.sim.layer_system.creature_enter(expansion[1:3], new_plant)
                    self.sim.creatures.append(new_plant)

                    # reset plant so it doesn't proliferate
                    self.current_size = 0.02
                    
        
        self.producer_metabolize()

        # check if dead
        if self.energy == 0.0:
            self.die()

                    
