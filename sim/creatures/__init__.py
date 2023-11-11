import toml
import hashlib
import numpy as np
from algorithm.genetic_algorithm import GeneticAlgorithm
from sim.energy import EnergyBar


class Creature:
    name: str
    # core
    cfg: dict
    _cfg: dict
    position: np.ndarray
    behavior_system: GeneticAlgorithm
    energy_bar: EnergyBar

    # properties
    energy: float
    size: float

    def __init__(self, sim, genome=None):
        self.cfg = sim.cfg
        self._cfg = sim.cfg[self.name]
        self.sim = sim
        self.layer_system = sim.layer_system #EXPERIMENTAL


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

        #EXPERIMENTAL
        self.layer_system.creature_enter(self.position, self)


        # Compute a unique hash based on the 4th byte of creature's genome
        hasher = hashlib.sha256()
        hasher.update(self.behavior_system.genome[3].encode())
        hash = hasher.hexdigest()
        # Assign size and energy properties based on the hash
        self.size = int(hash[:32], 16) % 101 + 0.1
        self.energy = int(hash[32:], 16) % 101 + 1
        self.energy_bar = EnergyBar(initial_energy=self.energy, max_energy=101.0, satiation_level=85.0, size=self.size)
        # self.energy_bar = EnergyBar(initial_energy=10, max_energy=101.0, satiation_level=85.0, size=self.size)

    def reset(self):
        self._init_properties()

    def step(self):
        pass

    def die(self):
        """
        Handles death. A creature that dies should remove itself from sim.creatures
        and update the layer's grid position value.
        """
        pass

    @property
    def grid_pos(self):
        assert np.all(0 <= self.position) and np.all(self.position < self.sim.grid_size)
        # return int(self.sim.grid_size[1] - self.position[1] - 1), int(self.position[0])
        return int(self.position[0]), int(self.position[1])


class Corpse:
    pass
