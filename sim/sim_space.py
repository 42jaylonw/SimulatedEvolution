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
        self.predation_table = self.generate_predation_table(0)

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
            if not hasattr(creature, 'appearance'):
                render_img[creature.grid_pos] = creature.rgb
        render_img = self.get_render_image(render_img)
        cv2.imshow(str(self.name),
                   cv2.cvtColor(render_img, cv2.COLOR_RGB2BGR))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit()
        time.sleep(self._cfg['time_step'])

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

    # generate_predation_table generates the dictionary of which creatures can consume which
    # modes: 0 for only plant eaters, 1 for only meat eaters, 2 for omnivores
    def generate_predation_table(self, mode):
        num_consumers = self.cfg['Consumer']['num_species']
        num_producers = self.cfg['Producer']['num_species']
        
        predation_table = {}
        if (mode == 0):
            for i in range(num_consumers):
                producer_range = list(range(num_producers))
                num_edible_species = np.random.choice(len(producer_range), 1, replace=False)
                # guarantee at least 1 edible species
                num_edible_species = max(num_edible_species, 1)
                edible_species = np.random.choice(producer_range, num_edible_species, replace=False)
                predation_table[i] = [[], edible_species]
        if (mode == 1):
            for i in range(num_consumers):
                consumer_range = list(range(num_consumers))
                consumer_range.remove(i)
                num_edible_species = np.random.choice(consumer_range, 1, replace=False)
                # guarantee at least 1 edible species
                num_edible_species = max(num_edible_species, 1)
                edible_species = np.random.choice(consumer_range, num_edible_species, replace=False)
                predation_table[i] = [edible_species, []]
        if (mode == 2):
            for i in range(num_consumers):
                producer_range = list(range(num_producers))
                num_edible_producers = np.random.choice(producer_range, 1, replace=False)
                edible_producers = np.random.choice(producer_range, num_edible_producers, replace=False)
                consumer_range = list(range(num_producers))
                consumer_range.remove(i)
                num_edible_consumers = np.random.choice(len(consumer_range), 1, replace=False)
                edible_consumers = np.random.choice(consumer_range, num_edible_consumers, replace=False)
                predation_table[i] = [edible_consumers, edible_producers]
        return predation_table
        

    def get_render_image(self, img):
        scale = int(self._cfg['visual_size'][0] / img.shape[0])
        img = np.uint8(cv2.resize(
            np.transpose(img, (1, 0, 2)), self._cfg['visual_size'], interpolation=cv2.INTER_NEAREST) * 255)

        for creature in self.creatures:
            if hasattr(creature, 'appearance'):
                top_half = int(scale / 2)
                bot_half = scale - int(scale / 2)
                x, y = creature.grid_pos
                scaled_x = x * scale + int(scale / 2)
                scaled_y = y * scale + int(scale / 2)
                grid_background = img[scaled_x - top_half:scaled_x + bot_half, scaled_y - top_half: scaled_y + bot_half]
                mask = cv2.resize(creature.appearance_mask, (scale, scale), interpolation=cv2.INTER_NEAREST)
                mask = mask.reshape(scale, scale, 1)
                masked_grid_background = (1 - mask) * grid_background
                appearance = cv2.resize(creature.appearance, (scale, scale), interpolation=cv2.INTER_NEAREST)
                normalized_appearance = np.float32(appearance) / 255. - 0.5
                appearance = np.uint8(255 * (creature.rgb + 0.05 * normalized_appearance))
                img[scaled_x - top_half:scaled_x + bot_half,
                scaled_y - top_half: scaled_y + bot_half] = mask * appearance + masked_grid_background

        return img
