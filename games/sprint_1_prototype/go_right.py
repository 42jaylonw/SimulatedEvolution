import toml
import cv2
import time
import numpy as np

from sim.sim_space import SimSpace
from sim.creature import Creature, Producer, Consumer

SAVE_ZONE_RGB = [0.5647, 0.9333, 0.5647]
PASS_CONDITION = 0.5


class GoRightSim(SimSpace):
    def __init__(self, cfg):
        super().__init__(cfg)

        # set save zone to green
        self.grid_rgb[:, int(self.grid_size[0] * PASS_CONDITION):, :] = SAVE_ZONE_RGB

    def get_survivors(self):
        survivors = []
        for creatures in self.creatures:
            if creatures.position[0] >= int(self.grid_size[0] * PASS_CONDITION):
                survivors.append(creatures)
        return survivors

    def render(self):
        render_img = np.copy(self.grid_rgb)
        for creature in self.creatures:
            render_img[creature.grid_pos] = creature.rgb

        render_img = cv2.resize(render_img, self.cfg['SimSpace']['visual_size'], interpolation=cv2.INTER_NEAREST)
        # put text
        visual_size = self.cfg['SimSpace']['visual_size']
        pass_rate = np.round((len(self.get_survivors()) / len(self.creatures)) * 100, 2)
        render_text = f'Pass Rate: {pass_rate: .2f} %'
        cv2.putText(render_img, render_text, (int(visual_size[0] / 9), int(visual_size[0] / 8)),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 5)

        cv2.imshow(str(self.__class__.__name__),
                   cv2.cvtColor(np.uint8(render_img * 255), cv2.COLOR_RGB2BGR))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit()
        time.sleep(self.cfg['SimSpace']['time_step'])


def run_random_moving():
    num_consumers = 3
    config = toml.load("games/sprint_1_prototype/config.toml")
    sim = GoRightSim(config)
    consumers = [Consumer(sim) for _ in range(num_consumers)]
    sim.reset(consumers)

    for _ in range(1000):
        # render the simulation image
        sim.render()
        sim.step()
        # info = sim.get_near_info(consumers[0].grid_pos, 2)
        # grid_info = info[0]  # the grid layer info 0 means empty, 1 means grid board or obstacles
        # producers_info = info[1]  # the dimension 2: the producer layer info 0 means empty, 1 means a producer
        # consumers_info = info[2]  # the dimension 3: the consumer layer info 0 means empty, 1 means a consumer
        # print("grid_info: \n", grid_info)
        # print("producers_info: \n", producers_info)
        # print("consumers_info: \n", consumers_info)
        survivors = sim.get_survivors()
        print(f'pass rate: {len(survivors) / len(sim.creatures)}')
        sim.show_layer(2)


if __name__ == '__main__':
    run_random_moving()
