import toml
import numpy as np
from sim.sim_space import SimSpace
from sim.creatures.comsumer import Consumer
from sim.creatures.producer import Producer
from sim.emitter import LightSource, HeatSource


def get_map(sim: SimSpace, getter_func):
    a_map = np.zeros(sim.grid_size)
    for x in range(sim.grid_size[0]):
        for y in range(sim.grid_size[1]):
            a_map[x, y] = getter_func(np.array([x, y]))
    return a_map


class SurvivalSim(SimSpace):
    def __init__(self, cfg):
        super().__init__(cfg)
        # set save zone to green
        self.population_consumers = self._cfg['population_consumers']
        self.population_producers = self._cfg['population_producers']
        self.min_survival_rate = self._cfg['min_survival_rate']
        consumers = [Consumer(self) for _ in range(self.population_consumers)]
        producers = [Producer(self) for _ in range(self.population_producers)]
        self.heat_source = HeatSource(self, np.array([0, 0]), 20, 100)
        self.light_source = LightSource(self, np.array([0, 0]), 20, 100)
        emitters = [self.light_source, self.heat_source]
        # todo: add walls
        # self.layer_system.wall_add()
        self.reset(consumers + producers, emitters)
        # show maps
        light_map = get_map(self, self.layer_system.get_light_level)
        heat_map = get_map(self, self.layer_system.get_elevation)
        self.curr_generation = 0
        self.pass_rate_list = []

    def termination(self):
        if self.curr_generation >= self.max_generations:
            return True
        return False

    def end_generation(self):
        self.curr_generation += 1
        # log data
        pass_rate = len(self.get_survivors()) / len(self.creatures)
        self.pass_rate_list.append(pass_rate)

        print(f"Generation: {self.curr_generation}: Pass Rate {pass_rate}")
        # reproduce and reset
        survivors = self.get_survivors()
        offsprings = self.generate_offsprings(survivors)
        self.reset(offsprings)

    def get_survivors(self):
        survivors = []
        for creatures in self.creatures:
            # if creatures.position[0] >= int(self.grid_size[0] * (1. - PASS_CONDITION)):
            survivors.append(creatures)
        return survivors

    def generate_offsprings(self, parent_pool):
        min_num_parents = int(self.population * self.min_survival_rate)
        if len(parent_pool) < min_num_parents:
            new_creatures = [Consumer(self) for _ in range(min_num_parents - len(parent_pool))]
            parent_pool = parent_pool + new_creatures
        offsprings = []
        for i in range(self.population):
            p0_id = np.random.randint(len(parent_pool))
            p1_id = np.random.choice([p_id for p_id in range(len(parent_pool))
                                      if p_id != p0_id])
            p0 = parent_pool[p0_id]
            p1 = parent_pool[p1_id]
            child_genome = p0.behavior_system.reproduce_genome(p1.behavior_system)
            offsprings.append(Consumer(self, child_genome))
        return offsprings


def run_random_moving():
    # create simulation space
    config = toml.load("games/sprint_2_survival/config.toml")
    sim = SurvivalSim(config)
    for _ in range(1000):
        sim.render()
        sim.step()


if __name__ == '__main__':
    run_random_moving()
