import toml
import cv2
import time
import numpy as np

from sim.sim_space import SimSpace
from sim.creatures.comsumer import Consumer

SAVE_ZONE_RGB = [0.5647, 0.9333, 0.5647]
PASS_CONDITION = 0.3


class GoRightSim(SimSpace):
    def __init__(self, cfg):
        super().__init__(cfg)
        # set save zone to green
        self.grid_rgb[int(self.grid_size[0] * (1. - PASS_CONDITION)):, :, :] = SAVE_ZONE_RGB
        self.population = self._cfg['population']
        self.min_survival_rate = self._cfg['min_survival_rate']
        self.reset([Consumer(self) for _ in range(self.population)])
        self.curr_generation = 0
        self.pass_rate_list = []

    def termination(self):
        if self.curr_generation >= self.max_generations:
            return True
        return False

    def end_generation(self):
        self.curr_generation += 1
        # log data
        pass_rate = len(self.get_survivors()) / len(self.creatures)
        self.pass_rate_list.append(pass_rate)

        print(f"Generation: {self.curr_generation}: Pass Rate {pass_rate}")
        # reproduce and reset
        survivors = self.get_survivors()
        offsprings = self.generate_offsprings(survivors)
        self.reset(offsprings)

    def get_survivors(self):
        survivors = []
        for creatures in self.creatures:
            if creatures.position[0] >= int(self.grid_size[0] * (1. - PASS_CONDITION)):
                survivors.append(creatures)
        return survivors

    def generate_offsprings(self, parent_pool):
        min_num_parents = int(self.population * self.min_survival_rate)
        if len(parent_pool) < min_num_parents:
            new_creatures = [Consumer(self) for _ in range(min_num_parents - len(parent_pool))]
            parent_pool = parent_pool + new_creatures
        offsprings = []
        for i in range(self.population):
            p0_id = np.random.randint(len(parent_pool))
            p1_id = np.random.choice([p_id for p_id in range(len(parent_pool))
                                      if p_id != p0_id])
            p0 = parent_pool[p0_id]
            p1 = parent_pool[p1_id]
            child_genome = p0.behavior_system.reproduce_genome(p1.behavior_system)
            offsprings.append(Consumer(self, child_genome))
        return offsprings

    def render(self):
        render_img = np.copy(self.grid_rgb)
        for creature in self.creatures:
            render_img[creature.grid_pos] = creature.rgb

        render_img = self.get_render_image(render_img)
        # put text
        visual_size = self.cfg['SimSpace']['visual_size']
        pass_rate = np.round((len(self.get_survivors()) / len(self.creatures)) * 100, 2)
        render_text0 = f'Generation: {self.curr_generation}'
        render_text1 = f'Pass Rate: {pass_rate: .2f} %'
        cv2.putText(render_img, render_text0, (int(visual_size[0] / 6), int(visual_size[1] / 12)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 4)
        cv2.putText(render_img, render_text1, (int((visual_size[0]) / 6), int((visual_size[1]) / 12) + 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 4)

        cv2.imshow(str(self.name), cv2.cvtColor(render_img, cv2.COLOR_RGB2BGR))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit()
        time.sleep(self._cfg['time_step'])


def run_game(is_render=False):
    import matplotlib.pyplot as plt
    config = toml.load("games/sprint_1_prototype/config.toml")
    sim = GoRightSim(config)
    while not sim.termination():
        if is_render:
            sim.render()
        sim.step()
    plt.ylabel('Survival Rate')
    plt.xlabel('Generations')
    plt.grid()
    plt.plot(sim.pass_rate_list)
    plt.show()
    sim.cfg['SimSpace']['time_step'] = 0.03
    for _ in range(150):
        sim.render()
        sim.step()


def get_args():
    import argparse
    parser = argparse.ArgumentParser("Evolution Simulator Sprint 1")
    parser.add_argument("--verbose",
                        '-v',
                        type=int,
                        default=0,
                        choices=[0, 1],
                        help="run with rendering or not")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    run_game(get_args().verbose)
