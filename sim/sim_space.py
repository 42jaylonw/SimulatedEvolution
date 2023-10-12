import time

import toml
import cv2
import numpy as np

CONFIG = toml.load("./config/simulation.toml")


class SimSpace:
    def __init__(self):
        self.creatures = None
        self.ground_size = np.array(CONFIG['SimSpace']['ground_size'])
        self.ground = np.ones((*self.ground_size, 3))
        self.ground_rgb = np.ones((*self.ground_size, 3))

    def reset(self, creatures):
        self.creatures = creatures

    def step(self):
        assert self.creatures is not None, "Reset first!"
        for creature in self.creatures:
            creature.step()

    def render(self):
        render_img = np.copy(self.ground_rgb)
        for creature in self.creatures:
            render_img[self.pos_to_pixel(creature.position)] = creature.rgb
        cv2.imshow(str(self.__class__.__name__),
                   cv2.cvtColor(np.uint8(cv2.resize(render_img, CONFIG['SimSpace']['visual_size'],
                                                    interpolation=cv2.INTER_NEAREST) * 255),
                                cv2.COLOR_RGB2BGR))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit()
        time.sleep(CONFIG['SimSpace']['time_step'])

    # utils
    def pos_to_pixel(self, pos):
        assert np.all(0 <= pos) and np.all(pos < self.ground_size)
        return int(pos[1]), int(self.ground_size[1] - pos[0] - 1)
