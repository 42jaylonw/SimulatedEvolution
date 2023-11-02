from . import Creature


class Producer(Creature):

    def step(self):
        if self.sim.is_pos_layer_empty("Producer", self.position):
            self.sim.increment_pos_layer("Producer", self.position, 1)
