import numpy as np
import random
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

    def __init__(self, sim, genome=None, spawn_pos=None):
        super().__init__(sim, genome, spawn_pos)

        if (self.genome == None):
            self.genome = self.generate_genome()

        hash = self.generate_hash(self.genome)

        self.ideal_temp = int(hash[:32], 16) % 25 + 15
        self.light_req = int(hash[32:], 16) % 20 + 20

        # growth rate determines how fast the creature grows
        # given ideal conditions
        self.growth_rate = .05

        # current_size is similar to a tracker for age
        # a creature grows to it's .size when current_size = 1.0
        self.current_size = 0.01

        self.fruit_bearer = False


    def generate_producer_genome(self):
        # get random genome
        genome = random.randint(0, 4294967295)
        # convert to hex and remove '0x' prefix
        genome = hex(genome)[2:]
        return genome

    def mutate_producer_genome(self):
        to_mut = self.genome
        # gene mutates
        if random.randint(0, 100) / 100.0 <= self.mutation_rate:
            mutate_index = random.randint(0, len(to_mut) - 1)
            mutate_char = hex(random.randint(0, 15))[2:]
            temp = list(to_mut)
            temp[mutate_index] = mutate_char
            to_mut = "".join(temp)
        return to_mut

    
    # use when calculating light absorption
    # for raw light levels, use will's refactored function
    def get_light_level(self, pos):
        if (self.sim.layer_system.out_of_bounds(pos)):
            return -1
        # get list of producers at space in pool
        producer_list = self.sim.layer_system.get_producers(pos)
        if len(producer_list) == 0:
            return self.sim.layer_system.get_light_level(pos)
        # get their sizes and add them up
        size_total = 0
        for producer in producer_list:
            size_total += producer.size

        if size_total == 0:
            print("help")
            print(pos)
            print(producer_list)
        # light level for the creature is (their size / size total) * light lvl
        ret = ((self.size) / size_total) * self.sim.layer_system.get_light_level(pos)
        return ret

    def get_temp(self, pos):
        if (self.sim.layer_system.out_of_bounds(pos)):
            return -1
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

    def producer_metabolize(self):
        pos = self.position
        light = self.light_req - self.get_light_level(pos)
        light = max(0, light)

        size_penalty = .1
        light_penalty = .02
        self.energy -= (self.current_size * size_penalty) + (light * light_penalty)

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

    # expansion_assess is used to assess what neighboring tile would be best
    # returns an array with [(score of space), x, y]
    def expansion_assess(self):

        possible_expansion = []
        pos = self.position

        target_pos = pos
        target_pos[0] -= 1
        if self.expansion_possible(target_pos):
            exp_tile = [self.assess_tile(target_pos)]
            possible_expansion += exp_tile

        target_pos = pos
        target_pos[0] += 1
        if self.expansion_possible(target_pos):
            exp_tile = [self.assess_tile(target_pos)]
            possible_expansion += exp_tile     

        target_pos = pos
        target_pos[1] -= 1
        if self.expansion_possible(target_pos):
            exp_tile = [self.assess_tile(target_pos)]
            possible_expansion += exp_tile

        target_pos = pos
        target_pos[1] += 1
        if self.expansion_possible(target_pos):
            exp_tile = [self.assess_tile(target_pos)]
            possible_expansion += exp_tile
                
        return possible_expansion

    def assess_tile(self, pos):
        ret = [0, pos[0], pos[1]]
        # tile_score is our running score for the tile
        # as a candidate for growth
        tile_score = 0.0

        # add based on light and heat values
        if (self.sim.layer_system.out_of_bounds(pos)):
            print("error assess tile")

        tile_score += self.get_temp(pos)
        tile_score = tile_score * self.get_light_level(pos)

        tile_score -= random.randint(1, int(tile_score))

        ret[0] = int(tile_score)

        return ret

    # producer_expand handles whether the producer expands to a neighboring tile or not
    # expansions is the list of possible expansions, we select the most fit
    def producer_expand(self, expansions):
        if (len(expansions) == 0):
            return
        # expansion is where the plant chooses to expand by the max of the scoring function
        expansion = max(expansions, key=lambda x: x[0])
        # TODO: handle creation of new plant at expansion tile
        new_genome = self.mutate_producer_genome()
        new_plant = self.__class__(self.sim, new_genome)
        new_plant.species_id = self.species_id
        new_plant.set_position(expansion[1:3])
        self.sim.layer_system.creature_enter(expansion[1:3], new_plant)
        self.sim.creatures.append(new_plant)

        # reset plant so it doesn't proliferate
        self.current_size = 0.02
        return


    def die(self):
        if self in self.sim.creatures:
            self.sim.creatures.remove(self)

        self.sim.layer_system.creature_exit(self.position, self)

    # expansion_possible checks if the producer can expand into that tile
    def expansion_possible(self, pos):
        if (self.sim.layer_system.out_of_bounds(pos)):
            return 0
        # ensure plant of same species is not already on tile
        for producer in self.sim.layer_system.get_producers(pos):
            if producer.species_id == self.species_id or producer.genome == self.genome:
                return 0
        return not self.sim.layer_system.has_wall(pos)


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
                    expansions = self.expansion_assess()

                    self.producer_expand(expansions)
                    
        
        self.producer_metabolize()

        # check if dead
        if self.energy <= 0.0:
            self.die()

                    
