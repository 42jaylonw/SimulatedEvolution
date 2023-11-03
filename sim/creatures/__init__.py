import toml
import numpy as np
from algorithm.genetic_algorithm import GeneticAlgorithm


class Creature:
    name: str
    # core
    cfg: dict
    _cfg: dict
    position: np.ndarray
    behavior_system: GeneticAlgorithm

    # properties
    energy: float
    size: float
    metabolism: float

    def __init__(self, sim, genome=None):
        self.cfg = sim.cfg
        self._cfg = sim.cfg[self.name]
        self.sim = sim

        self.behavior_system = GeneticAlgorithm(
            num_observations=self._cfg['num_observations'],
            num_actions=self._cfg['num_actions'],
            genome=genome,
            num_neurons=self._cfg['num_neurons'],
            reproduce_mode=self._cfg['reproduce_mode'],
            mutation_rate=self._cfg['mutation_rate'])

        self._init_properties()

    def _init_properties(self):
        self.rgb = self._cfg['rgb']
        self.position = np.random.randint(self.sim.grid_size)
        self.sim.increment_pos_layer(self.name, self.position, 1)
        self.energy = 0.

    def reset(self):
        self._init_properties()

    def step(self):
        pass

    @property
    def grid_pos(self):
        assert np.all(0 <= self.position) and np.all(self.position < self.sim.grid_size)
        # return int(self.sim.grid_size[1] - self.position[1] - 1), int(self.position[0])
        return int(self.position[0]), int(self.position[1])


class Corpse:
    pass
