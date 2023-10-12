from sim.sim_space import SimSpace
from sim.creature import Producer, Consumer


def run_random_moving():
    num_producers = 1000
    num_consumers = 50
    sim = SimSpace()
    producers = [Producer(sim) for _ in range(num_producers)]
    consumers = [Consumer(sim) for _ in range(num_consumers)]
    sim.reset(producers + consumers)

    for _ in range(1000):
        # render the simulation image
        sim.render()
        sim.step()


if __name__ == '__main__':
    run_random_moving()
