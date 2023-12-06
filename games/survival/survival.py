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

    def termination(self):
        if self.curr_generation >= self.max_generations:
            return True
        return False

    def end_generation(self):
        self.curr_generation += 1
        # log data
        if len(self.creatures) == 0:
            pass_rate = 0
        else:
            pass_rate = len(self.get_survivors()) / self.population_consumers
        self.pass_rate_list.append(pass_rate)

        print(f"Generation: {self.curr_generation}: Survival Rate {pass_rate}")
        # reproduce and reset
        survivors = self.get_survivors()
        offsprings = self.generate_offsprings(survivors)
        producers = [Producer(self) for _ in range(self.population_producers)]
        creatures = offsprings + producers
        self.reset(creatures, self.emitters)

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


def run_example_evolution_train(num_generation=5):
    # create simulation space
    config = toml.load("games/survival/config.toml")
    sim = SurvivalSim(config)
    consumers = [Consumer(sim) for _ in range(sim.population_consumers)]
    producers = [Producer(sim) for _ in range(sim.population_producers)]
    emitters = [HeatSource(sim, np.array([0, 0]), 20, 100),
                LightSource(sim, np.array([0, 0]), 20, 100)]
    sim.reset(consumers + producers, emitters)
    sim.train(num_generation)
    # show result
    image_array = []
    for _ in range(50):
        sim.step()
        render_img = sim.render()
        image_array.append(render_img)
    create_gif(image_array, f"survival_generation_{num_generation}.gif", duration=5.)


if __name__ == '__main__':
    run_example_evolution_train()
