import toml
import numpy as np
from algorithm.genetic_algorithm import GeneticAlgorithm


class Creature:
    # core
    cfg: dict
    position: np.ndarray
    behavior_system: GeneticAlgorithm

    # properties
    energy: float
    size: float
    metabolism: float

    def __init__(self, sim):
        self.cfg = sim.cfg[self.__class__.__name__]
        self.sim = sim

        self.behavior_system = GeneticAlgorithm(
            num_observations=self.cfg['num_observations'],
            num_actions=self.cfg['num_actions'],
            genome=self.cfg['genome'],
            num_neurons=self.cfg['num_neurons'],
            reproduce_mode=self.cfg['reproduce_mode'],
            mutation_rate=self.cfg['mutation_rate'])

        self._init_properties()

    def _init_properties(self):
        self.rgb = self.cfg['rgb']
        self.sim.increment_pos_layer(self.__class__.__name__, self.position, 1)
        self.position = np.random.randint(self.sim.grid_size)
        self.energy = 0.

    def step(self):
        pass

    @property
    def grid_pos(self):
        assert np.all(0 <= self.position) and np.all(self.position < self.sim.grid_size)
        return int(self.sim.grid_size[1] - self.position[1] - 1), int(self.position[0])


class Corpse:
    pass
