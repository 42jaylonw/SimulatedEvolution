import toml
import numpy as np


# todo： [
#  abstract position,
#  vision
#  ]

class Creature:
    def __init__(self, sim):
        self.sim = sim
        self.rgb = sim.cfg[self.__class__.__name__]['rgb']
        self.position = np.random.randint(sim.grid_size)

    def step(self):
        pass

    @property
    def grid_pos(self):
        assert np.all(0 <= self.position) and np.all(self.position < self.sim.grid_size)
        return int(self.position[1]), int(self.sim.grid_size[1] - self.position[0] - 1)


class Producer(Creature):

    def step(self):
        pass


class Consumer(Creature):

    def __init__(self, sim):
        super().__init__(sim)
        self.speed = sim.cfg['Consumer']['init_speed']

    def step(self):
        other_creatures = self.sim.creatures
        d_x = np.random.choice([-self.speed, self.speed], p=[0.5, 0.5])
        d_y = np.random.choice([-self.speed, self.speed], p=[0.5, 0.5])
        self.position[0] = np.clip(self.position[0] + d_x, 0, self.sim.grid_size[0] - 1)
        self.position[1] = np.clip(self.position[1] + d_y, 0, self.sim.grid_size[1] - 1)
