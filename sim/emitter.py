import numpy as np

# "Abstract" class
class Emitter():
    position: np.ndarray

    def __init__(self, sim):
        self.sim = sim
        self.position = np.random.randint(sim.grid_size)

    def step(self):
        pass

    @property
    def grid_pos(self):
        assert np.all(0 <= self.position) and np.all(self.position < self.sim.grid_size)
        return int(self.sim.grid_size[1] - self.position[1] - 1), int(self.position[0])

# Light Layer (layer 5)
class LightSource(Emitter):
    light_range: int

    def __init__(self, sim):
        super().__init(sim)

# Temperature Layer (layer 6)
class HeatSource(Emitter):
    heat_range: int

    def __init__(self):
        super().__init__(sim)