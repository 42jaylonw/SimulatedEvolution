import toml
import hashlib
import numpy as np
from algorithm.genetic_algorithm import GeneticAlgorithm
from sim.energy import EnergyBar
from sim.visualization.appearance import rgb_mutation
from sim.visualization.random_ship_generator import InvaderCreator


class Creature:
    name: str
    # core
    cfg: dict
    _cfg: dict
    position: np.ndarray
    behavior_system: GeneticAlgorithm
    energy_bar: EnergyBar

    # properties
    species_id: int
    energy: float
    size: float

    def __init__(self, sim, genome=None, spawn_pos=None):
        self.cfg = sim.cfg
        self._cfg = sim.cfg[self.name]
        self.sim = sim
        self.layer_system = sim.layer_system  # EXPERIMENTAL
        #self.position = None
        self.position = spawn_pos
        if self.position is not None:
            self.layer_system.creature_enter(self.position, self)

        if self.name == 'Consumer':
            self.behavior_system = GeneticAlgorithm(
                num_observations=self._cfg['num_observations'],
                num_actions=self._cfg['num_actions'],
                genome=genome,
                num_neurons=self._cfg['num_neurons'],
                reproduce_mode=self._cfg['reproduce_mode'],
                mutation_rate=self._cfg['mutation_rate'],
                creature=self)
            self.genome = self.behavior_system.genome
        elif self.name == 'Producer':
            self.genome = self.generate_producer_genome()
            self.mutation_rate=self._cfg['mutation_rate']
        self._init_properties()

    def _init_properties(self):
        self.image_data = None
        self.ref_id = str(self)
        if 'num_species' in self._cfg:
            self.species_id = np.random.randint(self._cfg['num_species'])
        else:
            self.species_id = 0
        self.rgb = rgb_mutation(self._cfg['rgb'], self.species_id, self._cfg['num_species'])
        if self.name == 'Consumer':
            self.appearance = InvaderCreator(img_size=5).get_an_invader(5)
            self.appearance_mask = (self.appearance.sum(2) != 0).astype(np.uint8)
            # consolidate appearance and mask data into single representation
            mask = np.expand_dims(self.appearance_mask, axis=2)
            self.image_data = np.concatenate((self.appearance, mask), axis=2)

        if self.position is None:
            self.position = np.random.randint(self.sim.grid_size)
            self.layer_system.creature_enter(self.position, self)

        # self.sim.increment_pos_layer(self.name, self.position, 1)

        # Compute a unique hash based on the 4th byte of creature's genome
        if self.name == 'Consumer':
            hash = self.generate_hash(self.genome[3])
        else:
            hash = self.generate_hash(self.genome)
        # Assign size and energy properties based on the hash
        self.size = int(hash[:32], 16) % 101 + 0.1
        self.energy = int(hash[32:], 16) % 101 + 1
        self.energy_bar = EnergyBar(initial_energy=self.energy, max_energy=101.0, satiation_level=85.0, size=self.size, age_rate=0.02)
        # self.energy_bar = EnergyBar(initial_energy=10, max_energy=101.0, satiation_level=85.0, size=self.size)

    def reset(self):
        self._init_properties()

    def step(self):
        pass

    def remove(self):
        """
        Removes the creature from the SimSpace. Removes itself from sim.creatures
        and updates the list stored at that position in the layer system.
        Different from die() in that no additional simulation logic is attached.
        """
        if self in self.sim.creatures:
            self.sim.creatures.remove(self)

        self.layer_system.creature_exit(self.position, self)
        pass

    def die(self):
        """
        Handles death. A creature that dies should remove itself from sim.creatures
        and update the layer's grid position value.
        """
        if self in self.sim.creatures:
            self.sim.creatures.remove(self)

        self.layer_system.creature_exit(self.position, self)
        pass

    # NOTE: This assumes that the creature has already been spawned.
    def set_position(self, target_pos):
        assert self.position is not None
        target_pos[0] = np.clip(target_pos[0], 0, self.sim.grid_size[0] - 1)
        target_pos[1] = np.clip(target_pos[1], 0, self.sim.grid_size[1] - 1)
        # Update the Layer System
        self.layer_system.creature_move(self.position, target_pos, self)
        # Update the creature's position to the target position
        self.position = target_pos

    def generate_hash(self, to_hash):
        hasher = hashlib.sha256()
        hasher.update(to_hash.encode())
        hash = hasher.hexdigest()
        return hash

    @property
    def grid_pos(self):
        assert np.all(0 <= self.position) and np.all(self.position < self.sim.grid_size)
        # return int(self.sim.grid_size[1] - self.position[1] - 1), int(self.position[0])
        return int(self.position[0]), int(self.position[1])

    @property
    def creature_info(self):
        print(self.energy_bar)
        if self.image_data is not None:
            return {"genome": self.genome,
                    "size": self.size,
                    "energy": self.energy_bar.current_energy,
                    "refId" : str(self),
                    "image_data": self.image_data.tolist()}
        return {"genome": self.genome,
                "size": self.size,
                "energy": self.energy_bar.current_energy}


class Corpse:
    pass
