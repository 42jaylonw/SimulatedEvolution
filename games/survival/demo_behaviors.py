import time

import toml
import numpy as np
from sim.sim_space import SimSpace
from sim.creatures.comsumer import Consumer
from sim.creatures.producer import Producer
from sim.emitter import LightSource, HeatSource
from sim.visualization.recorder import create_gif


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
        self.num_species_consumers = self.cfg['Consumer']['num_species']
        self.population_consumers = self._cfg['population_consumers']
        self.population_producers = self._cfg['population_producers']
        self.min_survival_rate = self._cfg['min_survival_rate']
        self.curr_generation = 0
        self.pass_rate_list = []

    def train(self, num_generations):
        while True:
            if self.curr_generation >= num_generations:
                break
            self.step()

    def end_generation(self):
        # log data
        if len(self.creatures) == 0:
            pass_rate = 0
        else:
            pass_rate = len(self.get_survivors()) / self.population_consumers
        self.pass_rate_list.append(pass_rate)

        print(f"Generation: {self.curr_generation}: Survival Rate {pass_rate}")
        # reproduce and reset
        survivors = self.get_survivors()
        for creature in self.creatures:
            creature.remove()
        offsprings = self.generate_offsprings(survivors)
        # producers = [Producer(self) for _ in range(self.population_producers)]
        for pos in [
            (0, 0), (0, 1), (0, 2), (0, 5),
            (1, 0), (1, 2), (0, 4), (0, 5),
            (2, 0), (2, 1), (0, 3), (2, 4), (2, 5),
            (4, 0), (3, 1), (3, 3), (4, 4), (4, 5), (4, 8),
            (5, 0), (5, 1), (5, 3), (5, 5), (4, 6), (4, 7),
            (6, 0), (6, 1), (6, 3), (6, 5),
            (7, 0), (7, 1), (7, 3), (7, 5), (7, 6), (7, 8),
            (8, 0), (8, 1), (8, 3), (8, 4), (8, 6), (8, 7),
        ]:
            producers = [Producer(self, spawn_pos=np.int64(pos)) for _ in range(2)]
        self.time_steps = 0
        self.curr_generation += 1

    def get_survivors(self):
        survivors = []
        for creatures in self.creatures:
            if isinstance(creatures, Consumer):
                # if creatures.position[0] >= int(self.grid_size[0] * (1. - PASS_CONDITION)):
                survivors.append(creatures)
        return survivors

    def generate_offsprings(self, parent_pool):
        min_num_parents = int(self.population_consumers * self.min_survival_rate)
        if len(parent_pool) < min_num_parents:
            new_creatures = [Consumer(self) for _ in range(min_num_parents - len(parent_pool))]
            parent_pool = parent_pool + new_creatures
        offsprings = []
        parent_pool_species = []
        parent_ratios_species = []
        for spices_id in range(self.num_species_consumers):
            species_parents = []
            for p in parent_pool:
                if p.species_id == spices_id:
                    species_parents.append(p)
            if len(species_parents) >= 2:
                parent_pool_species.append(species_parents)
                parent_ratios_species.append(len(species_parents) / len(parent_pool))

        for group_id in range(len(parent_pool_species)):
            species_parent_pool = parent_pool_species[group_id]
            species_ratio = parent_ratios_species[group_id]
            for i in range(int(self.population_consumers * species_ratio)):
                p0_id = np.random.randint(len(species_parent_pool))
                p1_id = np.random.choice([p_id for p_id in range(len(species_parent_pool))
                                          if p_id != p0_id])
                p0 = species_parent_pool[p0_id]
                p1 = species_parent_pool[p1_id]
                child_genome = p0.behavior_system.reproduce_genome(p1.behavior_system)
                offspring = Consumer(self, child_genome, species_id=p0.species_id)
                offsprings.append(offspring)
        return offsprings


def run_eat_producer():
    # create simulation space
    config = toml.load("games/survival/config.toml")
    config['SimSpace']['grid_size'] = [5, 5]
    config['SimSpace']['population_consumers'] = 1
    config['SimSpace']['population_producers'] = 10
    config['Consumer']['size_consumption_rate'] = 0.5
    sim = SurvivalSim(config)
    sim.time_steps = 0
    consumers = [Consumer(sim) for _ in range(sim.population_consumers)]
    producers = [Producer(sim) for _ in range(sim.population_producers)]
    emitters = [HeatSource(sim, np.array([0, 0]), 20, 100),
                LightSource(sim, np.array([0, 0]), 20, 100)]
    # sim.reset(consumers + producers, emitters)
    # sim.train(num_generation)
    # show result
    image_array = []
    for i in range(15):
        sim.step()
        render_img = sim.render()
        if i > 0:
            image_array.append(render_img)
    create_gif(image_array, f"survival_eat_producer.gif", duration=3.)


def run_eat_other():
    # create simulation space
    config = toml.load("games/survival/config.toml")
    config['SimSpace']['grid_size'] = [5, 5]
    config['SimSpace']['population_consumers'] = 3
    config['SimSpace']['population_producers'] = 0
    config['Producer']['num_species'] = 2
    config['Consumer']['size_consumption_rate'] = 0.1
    sim = SurvivalSim(config)
    sim.time_steps = 0
    consumers = [Consumer(sim) for _ in range(sim.population_consumers)]
    producers = [Producer(sim) for _ in range(sim.population_producers)]
    emitters = [HeatSource(sim, np.array([0, 0]), 20, 100),
                LightSource(sim, np.array([0, 0]), 20, 100)]
    # sim.reset(consumers + producers, emitters)
    # sim.train(num_generation)
    # show result
    image_array = []
    for i in range(15):
        sim.step()
        render_img = sim.render()
        image_array.append(render_img)
    create_gif(image_array, f"survival_eat_other.gif", duration=3.)


def run_reproduce():
    # create simulation space
    config = toml.load("games/survival/config.toml")
    config['SimSpace']['grid_size'] = [5, 5]
    config['SimSpace']['population_consumers'] = 2
    config['SimSpace']['population_producers'] = 50
    config['Consumer']['num_species'] = 1
    config['Consumer']['size_consumption_rate'] = 0.2
    sim = SurvivalSim(config)
    sim.time_steps = 0
    # consumers = [ for _ in range(sim.population_consumers)]
    a0 = Consumer(sim, spawn_pos=np.int64([2, 2]))
    a1 = Consumer(sim, spawn_pos=np.int64([4, 3]))
    producers = [Producer(sim) for _ in range(sim.population_producers)]
    emitters = [HeatSource(sim, np.array([0, 0]), 20, 100),
                LightSource(sim, np.array([0, 0]), 20, 100)]
    # sim.reset(consumers + producers, emitters)
    # sim.train(num_generation)
    # show result
    [sim.step() for _ in range(10)]
    image_array = []
    for i in range(15):
        sim.step()
        if i == 0:
            a0.position = np.int64([2, 1])
            a1.position = np.int64([4, 4])
        if i == 1:
            a0.position = np.int64([2, 2])
            a1.position = np.int64([4, 3])
        if i == 2:
            a0.position = np.int64([2, 3])
            a1.position = np.int64([3, 3])
        if i == 3:
            a0.position = np.int64([2, 3])
            a1.position = np.int64([2, 3])
        if i == 4:
            a0.position = np.int64([1, 3])
            a1.position = np.int64([2, 4])
        if i == 5:
            a0.position = np.int64([1, 2])
            a1.position = np.int64([3, 3])
        render_img = sim.render()
        image_array.append(render_img)
    create_gif(image_array, f"survival_reproduce.gif", duration=3.)


def dance_around():
    # create simulation space
    config = toml.load("games/survival/config.toml")
    config['SimSpace']['max_steps'] = 50
    config['SimSpace']['grid_size'] = [20, 20]
    config['SimSpace']['population_consumers'] = 20
    config['SimSpace']['population_producers'] = 40
    config['Consumer']['num_species'] = 4
    config['Consumer']['size_consumption_rate'] = 0.2
    sim = SurvivalSim(config)
    sim.time_steps = 0
    consumers = [Consumer(sim) for _ in range(sim.population_consumers)]
    producers = [Producer(sim) for _ in range(sim.population_producers)]
    emitters = [HeatSource(sim, np.array([0, 0]), 20, 100),
                LightSource(sim, np.array([0, 0]), 20, 100)]
    # sim.reset(consumers + producers, emitters)
    sim.train(5)
    # show result
    image_array = []
    sim.time_steps = 0
    for i in range(49):
        sim.step()
        render_img = sim.render()
        if i > 0:
            image_array.append(render_img)
    create_gif(image_array, f"survival_dance.gif", duration=3.)


def demo_train():
    # create simulation space
    config = toml.load("games/survival/config.toml")
    config['SimSpace']['max_steps'] = 50
    config['SimSpace']['grid_size'] = [20, 20]
    config['SimSpace']['max_steps'] = 50
    config['SimSpace']['population_consumers'] = 40
    config['SimSpace']['population_producers'] = 20
    config['Consumer']['num_species'] = 1
    config['Consumer']['size_consumption_rate'] = 0.25
    sim = SurvivalSim(config)
    sim.time_steps = 0
    consumers = [Consumer(sim) for _ in range(sim.population_consumers)]
    emitters = [HeatSource(sim, np.array([0, 0]), 20, 100),
                LightSource(sim, np.array([0, 0]), 20, 100)]
    for pos in [
        (8, 0), (8, 1), (8, 4), (8, 6), (8, 8),
        (0, 8), (1, 8), (4, 8), (6, 8)
    ]:
        sim.layer_system.wall_add(np.int64(pos))

    for pos in [
        (0, 0), (0, 1), (0, 2), (0, 5),
        (1, 0), (1, 2), (0, 4), (0, 5),
        (2, 0), (2, 1), (0, 3), (2, 4), (2, 5),
        (4, 0), (3, 1), (3, 3), (4, 4), (4, 5), (4, 8),
        (5, 0), (5, 1), (5, 3), (5, 5),  (4, 6), (4, 7),
        (6, 0), (6, 1), (6, 3), (6, 5),
        (7, 0), (7, 1), (7, 3), (7, 5),  (7, 6), (7, 8),
        (8, 0), (8, 1), (8, 3), (8, 4),  (8, 6), (8, 7),
    ]:
        producers = [Producer(sim, spawn_pos=np.int64(pos)) for _ in range(2)]
    [Producer(sim) for _ in range(10)]
    # sim.reset(consumers + producers, emitters)
    # sim.train(5)
    # show result
    saving_gen = [0, 2, 5]
    for num_gen in range(6):
        if num_gen in saving_gen:
            image_array = []
            for i in range(sim.max_steps):
                sim.step()
                render_img = sim.render()
                image_array.append(render_img)
            curr_survival_rate = sim.pass_rate_list[num_gen]
            create_gif(image_array, f"train_Gen{num_gen}_SurvivalRate{curr_survival_rate}.gif", duration=3.)
        else:
            for i in range(sim.max_steps):
                sim.step()


if __name__ == '__main__':
    # run_eat_producer()
    # run_eat_other()
    # run_reproduce()
    # dance_around()
    demo_train()
