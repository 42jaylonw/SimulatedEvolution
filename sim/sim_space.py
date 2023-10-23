import time

import toml
import cv2
import numpy as np

from sim.creature import Producer, Consumer

CONFIG = toml.load("./config/simulation.toml")

LAYER_DICT = {
    # grid : 0
    Producer: 1,
    Consumer: 2
}
NUM_LAYERS = len(LAYER_DICT) + 1


class SimSpace:
    layers: np.ndarray
    grid: np.ndarray

    def __init__(self):
        self.creatures = None
        self.grid_size = np.array(CONFIG['SimSpace']['grid_size'])
        self.grid_rgb = np.ones((*self.grid_size, 3))


    def reset(self, creatures):
        self.creatures = creatures
        self.layers = np.zeros((NUM_LAYERS, *self.grid_size), dtype=np.int64)

    def step(self):
        assert self.creatures is not None, "Reset first!"
        # make a priority
        for creature in self.creatures:
            creature.step()
        self.refresh_state()

    def refresh_state(self):
        for creature in self.creatures:
            # if isinstance(creature, Producer):
            creature_pos = creature.grid_pos
            self.layers[LAYER_DICT[type(creature)], creature_pos[0], creature_pos[1]] = 1.

    def render(self):
        render_img = np.copy(self.grid_rgb)
        for creature in self.creatures:
            render_img[creature.grid_pos] = creature.rgb
        
        cv2.imshow(str(self.__class__.__name__),
                   cv2.cvtColor(np.uint8(cv2.resize(render_img, CONFIG['SimSpace']['visual_size'],
                                                    interpolation=cv2.INTER_NEAREST) * 255),
                                cv2.COLOR_RGB2BGR))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit()
        time.sleep(CONFIG['SimSpace']['time_step'])
    
    # return the starting position of all organism
    def get_creature_positions(self):
        return [(creature.grid_pos, creature.rgb) for creature in self.creatures]   
    
    # Update the state of the simulation grid  
    def update_simulator(self):
        # gather the data of all organisms
        positionData = []
        for creature in self.creatures:
            # current position of organism
            oldPos = creature.grid_pos
            # update movement
            creature.step()
            # new position of organism
            newPos = creature.grid_pos
            self.layers[LAYER_DICT[type(creature)], newPos[0], newPos[1]] = 1.
            positionData.append((oldPos, newPos, creature.rgb))
        return positionData


    def get_near_info(self, center, length):
        """
        :param:
            length: how far from the center
            example:
                near_info = sim.get_near_info(center=(0, 0), length=2)
                near_info.shape: (3, 3, 3)
        :return:
                the dimension 1: the grid layer info 0 means empty, 1 means grid board or obstacles
                the dimension 2: the producer layer info 0 means empty, 1 means a producer
                the dimension 3: the consumer layer info 0 means empty, 1 means a consumer
        """
        x, y = center
        rows, cols = self.grid_size
        output_size = (length * 2 - 1, length * 2 - 1)

        # Calculate the boundaries for slicing the grid_map
        x_start = max(0, x - length + 1)
        x_end = min(rows, x + length)
        y_start = max(0, y - length + 1)
        y_end = min(cols, y + length)

        # Calculate the boundaries for placing the slice into the output array
        out_x_start = length - 1 - (x - x_start)
        out_x_end = length - 1 + (x_end - x)
        out_y_start = length - 1 - (y - y_start)
        out_y_end = length - 1 + (y_end - y)

        # Place the slice into the output array
        # todo: make it not reverse
        output = np.ones((NUM_LAYERS, *output_size)) * np.array([1, 0, 0]).reshape(3, 1, 1)
        for layer_id in range(NUM_LAYERS):
            layer_info = self.layers[layer_id]
            output[layer_id, out_x_start:out_x_end, out_y_start:out_y_end
            ] = layer_info[x_start:x_end, y_start:y_end]
        return output
