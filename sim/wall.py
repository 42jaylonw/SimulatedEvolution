import numpy as np

class Wall():
    position: np.ndarray

    def __init__(self, sim, pos):
        self.sim = sim
        self.rgb = (0, 0, 0)#sim.cfg[self.__class__.__name__]['rgb']
        self.position = np.random.randint(sim.grid_size)
        self.position[0] = np.clip(pos[0], 0, self.sim.grid_size[0] - 1)
        self.position[1] = np.clip(pos[1], 0, self.sim.grid_size[1] - 1)

        self.sim.increment_pos_layer(self.__class__.__name__, self.position, 1)

    @property
    def grid_pos(self):
        assert np.all(0 <= self.position) and np.all(self.position < self.sim.grid_size)
        return int(self.sim.grid_size[1] - self.position[1] - 1), int(self.position[0])