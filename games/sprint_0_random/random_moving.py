import toml
from sim.sim_space import SimSpace
from sim.creature import Producer, Consumer
from sim.wall import Wall
from sim.emitter import LightSource, HeatSource

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


def run_random_moving():
    num_producers = 200
    num_consumers = 3
    # create simulation space
    config = toml.load("games/sprint_0_random/config.toml")
    sim = SimSpace(config)
    # create list of producers and consumers
    producers = [Producer(sim) for _ in range(num_producers)]
    consumers = [Consumer(sim) for _ in range(num_consumers)]
    walls = None
    walls = [Wall(sim, [i,i]) for i in range(sim.grid_size[0])]
    walls += [Wall(sim, [i, sim.grid_size[0] // 2]) for i in range(sim.grid_size[0])]
    emitters = [HeatSource(sim, [sim.grid_size[0] // 3, 1 * sim.grid_size[1] // 4], 10, 2), LightSource(sim, [(sim.grid_size[0] // 2) - 5, (sim.grid_size[1] // 2) + 5], 25, 1)]
    # add organisms, walls, emitters to simulation space
    sim.reset(producers + consumers, walls, emitters)

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
        sim.show_layer(5)
        #sim.print_layer(5)



if __name__ == '__main__':
    run_random_moving()
