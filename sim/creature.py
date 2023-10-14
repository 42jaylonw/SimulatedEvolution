import toml
import numpy as np
from sim.sim_space import SimSpace

CONFIG = toml.load("./config/simulation.toml")


# todo： [
#  abstract position,
#  vision
#  ]

class Creature:
    def __init__(self, sim: SimSpace):
        self.sim = sim
        self.position = np.random.randint(sim.ground_size - 1)

    def step(self):
        pass


class Producer(Creature):
    rgb = CONFIG['Producer']['rgb']

    def step(self):
        pass


class Consumer(Creature):
    rgb = CONFIG['Consumer']['rgb']

    def __init__(self, sim: SimSpace):
        super().__init__(sim)
        self.speed = CONFIG['Consumer']['init_speed']

    def step(self):
        other_creatures = self.sim.creatures
        d_x = np.random.choice([-self.speed, self.speed], p=[0.5, 0.5])
        d_y = np.random.choice([-self.speed, self.speed], p=[0.5, 0.5])
        self.position[0] = np.clip(self.position[0] + d_x, 0, self.sim.ground_size[0] - 1)
        self.position[1] = np.clip(self.position[1] + d_y, 0, self.sim.ground_size[1] - 1)
