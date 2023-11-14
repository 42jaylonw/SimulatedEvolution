import time

import cv2
import numpy as np
from sim.creatures.comsumer import Consumer
from sim.creatures.producer import Producer
from sim.emitter import LightSource, HeatSource
from sim.newlayersystem import LayerSystem


class SimSpace:
    name = 'SimSpace'
    cfg: dict
    layer_system: LayerSystem
    grid: np.ndarray

    def __init__(self, cfg):
        self.cfg = cfg
        self._cfg = cfg[self.name]
        self.creatures = None
        self.emitters = None
        self.grid_size = np.array(self._cfg['grid_size'])
        self.grid_rgb = np.ones((*self.grid_size, 3))

        self.layer_system = LayerSystem.LayerSystem(self.grid_size)

        self.max_steps = self._cfg['max_steps']
        self.max_generations = self._cfg['max_generations']

    def reset(self, creatures, emitters=()):
        self.time_steps = 0
        self.creatures = creatures
        self.emitters = emitters

        for creature in self.creatures:
            creature.reset()

    def step(self):
        assert self.creatures is not None, "Reset first!"

        self.layer_system.step()

        for emitter in self.emitters:
            emitter.step()

        # make a priority
        for creature in self.creatures:
            creature.step()

        self.time_steps += 1

        if self.time_steps >= self.max_steps:
            self.end_generation()

    def end_generation(self):
        pass

    def termination(self):
        pass


    def render(self):
        render_img = np.copy(self.grid_rgb)
        for creature in self.creatures:
            render_img[creature.grid_pos] = creature.rgb

        render_img = self.get_render_image(render_img)
        cv2.imshow(str(self.name),
                   cv2.cvtColor(render_img, cv2.COLOR_RGB2BGR))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit()
        time.sleep(self._cfg['time_step'])

    # This function's computation has been moved to the Consumer class
    """
    def get_near_info(self, center, length):
        """
        #:param:
        #    length: how far from the center
        #    example:
        #        near_info = sim.get_near_info(center=(0, 0), length=2)
        #        near_info.shape: (3, 3, 3)
        #:return:
        #        the dimension 1: the grid layer info 0 means empty, 1 means grid board or obstacles
        #        the dimension 2: the producer layer info 0 means empty, 1 means a producer
        #        the dimension 3: the consumer layer info 0 means empty, 1 means a consumer
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
    """

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

    def get_render_image(self, img):
        img = np.uint8(cv2.resize(
            np.transpose(img, (1, 0, 2)), self._cfg['visual_size'], interpolation=cv2.INTER_NEAREST) * 255)
        return img