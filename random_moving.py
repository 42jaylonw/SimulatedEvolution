from sim.sim_space import SimSpace
from sim.creature import Producer, Consumer


def run_random_moving():
    num_producers = 1000
    num_consumers = 1
    sim = SimSpace()
    producers = [Producer(sim) for _ in range(num_producers)]
    consumers = [Consumer(sim) for _ in range(num_consumers)]
    sim.reset(producers + consumers)

    for _ in range(1000):
        # render the simulation image
        sim.step()
        sim.render()
        info = sim.get_near_info(consumers[0].grid_pos, 2)
        grid_info = info[0]  # the grid layer info 0 means empty, 1 means grid board or obstacles
        producers_info = info[1]  # the dimension 2: the producer layer info 0 means empty, 1 means a producer
        consumers_info = info[2]  # the dimension 3: the consumer layer info 0 means empty, 1 means a consumer
        print("grid_info: \n", grid_info)
        print("producers_info: \n", producers_info)
        print("consumers_info: \n", consumers_info)


if __name__ == '__main__':
    run_random_moving()
