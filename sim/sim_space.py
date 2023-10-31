import time

import cv2
import numpy as np

from sim.creature import Producer, Consumer

LAYER_DICT = {
    # grid : 0
    Producer: 1,
    Consumer: 2
}
NUM_LAYERS = len(LAYER_DICT) + 1


class SimSpace:
    cfg: dict
    layers: np.ndarray
    grid: np.ndarray

    def __init__(self, cfg):
        self.cfg = cfg
        self.creatures = None
        self.grid_size = np.array(self.cfg['SimSpace']['grid_size'])
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
        # print(self.layers)

    # NOTE TO OTHERS: I had to move the handling of the layer values to the creatures themselves as they move
    # Instead of calling this function, the creatures call update_pos_layer() instead on their position + layer
    def refresh_state(self):
        self.layers[:] = 0.
        for creature in self.creatures:
            # if isinstance(creature, Producer):
            # clear all
            creature_pos = creature.grid_pos
            self.layers[LAYER_DICT[type(creature)], creature_pos[0], creature_pos[1]] = 1.

    def render(self):
        render_img = np.copy(self.grid_rgb)
        for creature in self.creatures:
            render_img[creature.grid_pos] = creature.rgb

        cv2.imshow(str(self.__class__.__name__),
                   cv2.cvtColor(np.uint8(cv2.resize(render_img, self.cfg['SimSpace']['visual_size'],
                                                    interpolation=cv2.INTER_NEAREST) * 255),
                                cv2.COLOR_RGB2BGR))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit()
        time.sleep(self.cfg['SimSpace']['time_step'])

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
        output = np.ones((NUM_LAYERS, *output_size)) * np.array([1] + [0] * (NUM_LAYERS - 1)).reshape(NUM_LAYERS, 1, 1)
        for layer_id in range(NUM_LAYERS):
            layer_info = self.layers[layer_id]
            output[layer_id, out_x_start:out_x_end, out_y_start:out_y_end
            ] = layer_info[x_start:x_end, y_start:y_end]
        return output

    def is_pos_layer_empty(self, layer, pos):
        """
            :param:
                layer: which layer should be checked - specifically, the object type will be checked to determine the layer
                    example: if a Consumer object is passed in, check layer id (LAYER_DICT=Consumer)
                pos: (x, y) position on the grid to check if empty/occupied
            :return:
                    True: there is no object on specified layer at pos
                    False: there is an object on specified layer at pos
        """
        assert not self.is_pos_out_of_bounds(pos), "pos must be within bounds of sim space grid"

        # Debug: Print CONSUMER layer grid -----------------
        # np.set_printoptions(threshold=np.inf)
        # np.set_printoptions(linewidth=150)
        # print(self.layers[LAYER_DICT[type(layer)]])
        # print("Checking pos" + str(pos) + ": " + str(self.layers[LAYER_DICT[type(layer)], pos[0], pos[1]]))
        # --------------------------------------------------

        if self.layers[LAYER_DICT[type(layer)], pos[0], pos[1]] == 0:
            return True
        else:
            return False

    def update_pos_layer(self, layer, pos, val=0):
        """
            :param:
                layer: which layer should be updated
                pos: (x, y) position on the grid layer to update the value of
                val: value that the layer at pos is updated to. default value sets it to empty (0)
        """
        assert val == 0 or val == 1, "val must be 0 or 1!"
        if not self.is_pos_out_of_bounds(pos):
            self.layers[LAYER_DICT[type(layer)], pos[0], pos[1]] = val

    def is_pos_out_of_bounds(self, pos):
        """
            :param:
                pos: (x, y) position that is checked to see if outside of bounds
            :return:
                True: pos is outside of bounds of sim space
                False: pos is within bounds of sim space
        """
        return pos[0] < 0 or pos[0] > self.grid_size[0] - 1 or pos[1] < 0 or pos[1] > self.grid_size[1] - 1

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
            positionData.append((oldPos, newPos, creature.rgb))
        return positionData

    def show_layer(self, layer_id):
        cv2.imshow(str(f'Layer ID {layer_id}'),
                   cv2.cvtColor(np.uint8(cv2.resize(self.layers[layer_id].reshape(
                       *self.grid_size, 1) * np.array([1, 1, 1]).reshape(1, 1, 3),
                                                    self.cfg['SimSpace']['visual_size'],
                                                    interpolation=cv2.INTER_NEAREST) * 255),
                                cv2.COLOR_RGB2BGR))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit()
