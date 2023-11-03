import toml
import numpy as np
from sim.sim_space import SimSpace
from sim.creatures.producer import Producer
from sim.creatures.comsumer import Consumer


# Create a simulation space with a specified number of consumers and producers
def generate_sim(num_producers=1, num_consumers=1):
    # create list of producers and consumers
    config = toml.load("games/sprint_0_random/config.toml")
    sim = SimSpace(config)
    producers = [Producer(sim) for _ in range(num_producers)]
    consumers = [Consumer(sim) for _ in range(num_consumers)]
    # add organisms to simulation space
    sim.reset(producers + consumers)
    return sim


# Get the initial positions of all active creatures in a specified sim space
def get_initial_positions(sim):
    return sim.get_creature_positions()


# Allow all creatures to move, then return their new positions
def get_updated_positions(sim):
    return sim.update_simulator()


class RandMoveConsumer(Consumer):
    def step(self):
        self.action_move(np.random.randint(0, 4))


def run_random_moving():
    num_producers = 100
    num_consumers = 3
    # create simulation space
    config = toml.load("games/sprint_0_random/config.toml")
    sim = SimSpace(config)
    # create list of producers and consumers
    producers = [Producer(sim) for _ in range(num_producers)]
    consumers = [RandMoveConsumer(sim) for _ in range(num_consumers)]
    # add organisms to simulation space
    sim.reset(producers + consumers)

    for _ in range(1000):
        # render the simulation image
        sim.step()
        sim.render()
        info = sim.get_near_info(consumers[0].grid_pos, 2)
        grid_info = info[0]  # the grid layer info 0 means empty, 1 means grid board or obstacles
        producers_info = info[1]  # the dimension 2: the producer layer info 0 means empty, 1 means a producer
        consumers_info = info[2]  # the dimension 3: the consumer layer info 0 means empty, 1 means a consumer
        # print("grid_info: \n", grid_info)
        # print("producers_info: \n", producers_info)
        # print("consumers_info: \n", consumers_info)
        # sim.show_layer(1)
        sim.show_layer(2)
        # sim.show_layer(3)
        # sim.print_layer("Consumer")


if __name__ == '__main__':
    run_random_moving()
