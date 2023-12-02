import toml
import numpy as np
from sim.sim_space import SimSpace
from sim.creatures.comsumer import Consumer
from sim.creatures.producer import Producer
from sim.emitter import LightSource, HeatSource

GRIDSIZE = 50
def step(sim):
    assert sim.creatures is not None, "Reset first!"
    print("i am running")
    # Refresh emitter layer values
    sim.layer_system.step()

    #grid_space
    """
    -len(Wall) = 0?
    -Emitters[]
    """
    positionData = []
    for emitter in sim.emitters:
        emitter.step()

    # make a priority
    for creature in sim.creatures:
        oldPos = creature.grid_pos
        creature.step()
        newPos = creature.grid_pos
        #positionData.append((oldPos, newPos, creature.rgb))
        positionData.append((oldPos, newPos))
    idk = []
    for i in range(GRIDSIZE):
        for j in range(GRIDSIZE):
           # (position, layerinformation)
           idk.append(([i,j], sim.layers[:, i, j].tolist()))
    # Return updated creature movement and updated layer information
    # return [positionData, idk]
    return positionData

# Create a simulation space with a specified number of consumers and producers
def generate_sim(num_producers=0, num_consumers=1):
    # create list of producers and consumers
    config = toml.load("games/sprint_0_random/config.toml")
    sim = SimSpace(config)
    producers = [Producer(sim) for _ in range(num_producers)]

    consumers = [Consumer(sim) for _ in range(num_consumers)]
    emitters = []

    # Adding walls using the new LayerSystem
    for i in range(sim.grid_size[0]):
        sim.layer_system.wall_add([i, sim.grid_size[0] // 2])

    emitters = [HeatSource(sim, [sim.grid_size[0] // 3, 1 * sim.grid_size[1] // 4], 25, 75),
                HeatSource(sim, [(sim.grid_size[0] // 3), (sim.grid_size[1] // 4)], 5, 25),
                LightSource(sim, [(sim.grid_size[0] // 3), (sim.grid_size[1] // 4)], 50, 100)]

    # add organisms to simulation space
    sim.reset(producers + consumers, emitters)
    return sim

# Get the initial positions of all active creatures in a specified sim space
def get_initial_positions(sim):
    return sim.get_creature_positions()


# Allow all creatures to move, then return their new positions
def get_updated_positions(sim):
    # return sim.update_simulator()
    return step(sim)


class RandMoveConsumer(Consumer):
    def step(self):
        self.action_move(np.random.randint(0, 4))


def run_random_moving():
    num_producers = 500
    num_consumers = 2
    # create simulation space
    config = toml.load("games/sprint_2_survival/config.toml")
    sim = SimSpace(config)
    # create list of producers and consumers
    producers = [Producer(sim) for _ in range(num_producers)]
    # consumers = [RandMoveConsumer(sim) for _ in range(num_consumers)]
    consumers = [Consumer(sim) for _ in range(num_consumers)]
    print(consumers)
    # add organisms to simulation space
    # sim.reset(producers + consumers)

    for i in range(sim.grid_size[0]):
        sim.layer_system.wall_add([i, sim.grid_size[0] // 2])

    emitters = [HeatSource(sim, [sim.grid_size[0] // 3, 1 * sim.grid_size[1] // 4], 20, 10)]#,
    #            HeatSource(sim, [(sim.grid_size[0] // 3), (sim.grid_size[1] // 4)], 8, -5)]
    # add organisms + emitters to simulation space
    sim.reset(producers + consumers, emitters)

    for _ in range(1000):
        # render the simulation image
        sim.render()
        sim.step()
        #sim.render()
        #info = sim.get_near_info(consumers[0].grid_pos, 2)
        #grid_info = info[0]  # the grid layer info 0 means empty, 1 means grid board or obstacles
        #producers_info = info[1]  # the dimension 2: the producer layer info 0 means empty, 1 means a producer
        #consumers_info = info[2]  # the dimension 3: the consumer layer info 0 means empty, 1 means a consumer
        # print("grid_info: \n", grid_info)
        # print("producers_info: \n", producers_info)
        # print("consumers_info: \n", consumers_info)

def get_location_info(sim):
    return sim.layers
if __name__ == '__main__':
    run_random_moving()
