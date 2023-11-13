import random
import numpy as np

"""""
*first byte*
sensory inputs
01 - blocked forward    02 - blocked back   03 - blocked left   04 - blocked right  05 - population density
06 - last movement was x    07 - last movement was y    08 - border distance north  09 - border distance east
0A - border distance south  0B - border distance west   0C - nearest border distance    0D - current loc. north
0E - current loc. east  0F - current loc. south     10 - current loc. west

internal neurons
11 - n_1    12 - n_2    13 - n_3

first byte of genome ranges from 01 to 13 (mod 19 + 1)

reserve 00 for detects food, which will have special connections to move towards the food.

*second byte*
internal neurons
01 - n_1    02 - n_2    03 - n_3    

action outputs
04 - move forward   05 - move random     06 - move backwards    07 - move left
08 - move right     09 - move north     0A - move east      0b - move south     0C - move west

second byte ranges from 01 to 0C (mod 12 + 1)

reserve 00 for move to food, which is reserved for special sensory input


*third byte*
this will determine the strength of connection, ranging from -4.0 to 4.0
00 will represent the extreme of -4.000
AA will represent the extreme of 4.000

*fourth byte*
currently unused, will keep open for potential down the road since there is no 24-bit integers
"""""


# worker functions
# byte_to_float is used for byte 3 to convert to a float
# int_to_hex_string is used for random genome generation and ensures that the output is of desired length
# extract_hex_sub is used to get the bytes from the hex string
def byte_to_float(byte):
    # Convert the input byte (hex string) to an integer
    value = int(byte, 16)

    # Calculate the float value within the range -4.0 to 4.0
    min_range = -4.0
    max_range = 4.0
    float_value = min_range + (max_range - min_range) * (value / 255.0)

    return float_value


def int_to_hex(number):
    # Convert the integer to a hexadecimal string with '0x' prefix, and remove the prefix
    hex_string = hex(number)[2:]
    # Ensure the string is exactly two characters long by padding with '0' if needed
    hex_string = hex_string.zfill(2)
    return hex_string


def hex_to_int(hex_str):
    try:
        return int(hex_str, 16)
    except ValueError:
        return None


def extract_hex_sub(input_string, start_index, end_index):
    if start_index < 0 or end_index > len(input_string):
        return "Invalid indices"

    substring = input_string[start_index:end_index]
    return substring


def generate_genome():
    # change numbers as program expands
    num_inputs = 16
    num_outputs = 9
    num_int_neurons = 3

    genome = ""
    # first byte
    genome += int_to_hex(
        random.randint(1, num_inputs + num_int_neurons))  # random number, then convert to 2 char hex string
    # second byte
    genome += int_to_hex(random.randint(1, num_outputs + num_int_neurons))  # same as before
    # third byte
    # as of right now, we are going to weight connections positively, since we would like to see action
    # may need to revert later
    genome += int_to_hex(random.randint(55, 255))
    # fourth byte
    genome += int_to_hex(random.randint(0, 255))
    return genome


def sensor_switch_handler(properties, sensor):
    match sensor:
        # blocked forwards
        case 1:
            return properties[3] * .5
        # blocked backwards
        case 2:
            return properties[4] * .5
        # blocked left
        case 3:
            return properties[5] * .5
        # blocked right
        case 4:
            return properties[6] * .5
        # population density
        case 5:
            return properties[7] * .16
        # last movement was in x dir
        case 6:
            if properties[2] == 1 or properties[2] == 3:
                return 1.0
            return 0.0
        # last movement was in y dir
        case 7:
            if properties[2] == 0 or properties[2] == 2:
                return 1.0
            return 0.0
        # border distance north
        # formula is (dist from north border / grid height)^2
        case 8:
            grid_height = 50
            dist_north = properties[1]
            return (dist_north / grid_height) * (dist_north / grid_height)
        # border distance east
        case 9:
            grid_height = 50
            dist_east = grid_height - properties[0]
            return (dist_east / grid_height) * (dist_east / grid_height)
        # border distance south
        case 10:
            grid_height = 50
            dist_south = grid_height - properties[1]
            return (dist_south / grid_height) * (dist_south / grid_height)
        # border distance west
        case 11:
            grid_height = 50
            dist_west = properties[0]
            return (dist_west / grid_height) * (dist_west / grid_height)
        # nearest border distance
        case 12:
            grid_height = 50
            nearest_border = max(properties[0], properties[1], grid_height - properties[1],
                                 grid_height - properties[0])
            return (nearest_border / grid_height) * .8  # arbitrary value to prevent overpowering
        # current location north
        # formula is (dist from south border / grid height)^2
        case 13:
            grid_height = 50
            dist_south = grid_height - properties[1]
            return (dist_south / grid_height) * (dist_south / grid_height)
        # current location east
        case 14:
            grid_height = 50
            dist_west = properties[0]
            return (dist_west / grid_height) * (dist_west / grid_height)
        # border distance south
        case 15:
            grid_height = 50
            dist_north = properties[1]
            return (dist_north / grid_height) * (dist_north / grid_height)
        # border distance west
        case 16:
            grid_height = 50
            dist_west = grid_height - properties[0]
            return (dist_west / grid_height) * (dist_west / grid_height)
        case _:
            print("sensor_switch_handler defaulting")


def if_neuron_triggers(properties, input_sensors):
    num_inputs = 16
    # make array to be returned
    ret = [0.0] * (num_inputs + 1)

    for sensor in input_sensors:
        ret[sensor] = sensor_switch_handler(properties, sensor)

    return ret


# create_active_map takes in a creature's genome and active sensors to create an adjacency map of network
# the key is the input sensor and the value is a list of pairs, with format (output index, connection strength)
def create_active_map(genome):

    # create dict to be returned
    ret = {}

    # populate adjacency map with network
    for k in genome:
        # define genome connection in adjacency map
        input_node = hex_to_int(extract_hex_sub(k, 0, 2))
        conn_str = byte_to_float(extract_hex_sub(k, 4, 6))
        if input_node not in ret:
            ret[input_node] = []
        # to_add is pair with format (output index, connection strength)
        to_add = [hex_to_int(extract_hex_sub(k, 2, 4)), conn_str]
        ret[input_node].append(to_add)

    # filter internal connections with no output
    # TODO: create function to filter internal connections with no meaningful output

    return ret


def movement_output(output_sensors, properties):
    output_index = np.array(output_sensors).argmax()
    output_array = [0, 0, 0, 0]
    match output_index:
        # move forward
        case 1:
            output_array[properties[2]] = 1
            return output_array
        # move random
        case 2:
            random_index = random.randint(0, 3)
            output_array[random_index] = 1
            return output_array
        # move backwards
        case 3:
            output_array[(properties[2] + 2) % 4] = 1
            return output_array
        # move left
        case 4:
            output_array[(properties[2] + 3) % 4] = 1
            return output_array
        # move right
        case 5:
            output_array[(properties[2] + 1) % 4] = 1
            return output_array
        # move north
        case 6:
            output_array[0] = 1
            return output_array
        # move east
        case 7:
            output_array[1] = 1
            return output_array
        # move south
        case 8:
            output_array[2] = 1
            return output_array
        # move west
        case 9:
            output_array[3] = 1
            return output_array
        # default case (move forward)
        case _:
            output_array[properties[2]] = 1
            return output_array


def clean_genome(genome):
    # change numbers as program expands
    num_inputs = 16
    num_outputs = 9
    num_internal_neurons = 3

    ret = []
    for gene in genome:
        new_gene = ""
        # first byte (input)
        to_add = extract_hex_sub(gene, 0, 2)
        to_add = hex_to_int(to_add) % (num_inputs + num_internal_neurons)
        # this is a temporary fix, since 00 is reserved for food detected
        if to_add == 0:
            to_add = 1
        new_gene += int_to_hex(to_add)
        # second byte
        to_add = extract_hex_sub(gene, 2, 4)
        to_add = hex_to_int(to_add) % (num_outputs + num_internal_neurons)
        # this is a temporary fix, since 00 is reserved for move to food
        if to_add == 0:
            to_add = 1
        new_gene += int_to_hex(to_add)
        # third and fourth byte (these values are converted and do not need to be modulo'd)
        new_gene += extract_hex_sub(gene, 4, 8)
        ret.append(new_gene)

    return ret


# mutate_genome takes in a genome string and a float mutation probability
# if the probability succeeds, that particular string in the genome will mutate a random bit
def mutate_genome(genome, mutation_chance):
    for g in range(len(genome)):
        # gene mutates
        if random.randint(0, 100) / 100.0 <= mutation_chance:
            # this code mutates the entire genome
            # mutate_index = random.randint(0, len(genome[g]) - 1)
            # this code mutates only the weights
            mutate_index = random.randint(0, len(genome[g]) - 1)
            mutate_char = int_to_hex(random.randint(0, 15))
            temp = list(genome[g])
            temp[mutate_index] = mutate_char
            genome[g] = "".join(temp)
    return genome


# reproduce_genome takes in two genome strings and an integer to declare which mode we are using
# 0 is full string genome, 1 is segmented genome, 2 is random genome
# the function returns a new genome that is a descendant of the two given as parameters
def reproduce_genome(parent1, parent2, mode):
    assert len(parent1) == len(parent2)
    new_gen = []
    if mode == 0:  # full string genome
        for gene in range(len(parent1)):
            # parent 1
            if gene % 2 == 0:
                new_gen.append(parent1[gene])
            # parent 2
            else:
                new_gen.append(parent2[gene])
        return new_gen
    elif mode == 1:  # segmented string genome
        parent_ind = 0;  # parent_ind keeps track of which parent the segment is being taken from
        parent_list = [parent1, parent2]
        for gene in range(len(parent1)):  # for each gene in the genome
            to_add = ""
            start_ind = 0;
            end_ind = 2;
            for seg in range(4):  # for each segment in the gene
                to_add += (extract_hex_sub(parent_list[parent_ind][gene], start_ind, end_ind))
                # increment vars
                parent_ind = (parent_ind + 1) % 2
                start_ind += 2
                end_ind += 2
            new_gen.append(to_add)
        return new_gen
    elif mode == 2:  # random string genome
        for gene in range(len(parent1)):
            to_add = ""
            for char in range(len(parent1[0])):
                parent_index = random.randint(1, 8) % 2
                if parent_index == 0:
                    to_add += (extract_hex_sub(parent1[gene], char, char + 1))
                elif parent_index == 1:
                    to_add += (extract_hex_sub(parent2[gene], char, char + 1))
            new_gen.append(to_add)
        return new_gen


class GeneticAlgorithm:
    genome: list

    def __init__(self,
                 num_observations,
                 num_actions,
                 genome=None,
                 num_genomes=4,
                 num_neurons=4,
                 reproduce_mode=1,
                 mutation_rate=0.2):
        self.num_observations = num_observations
        self.num_actions = num_actions
        self.num_genomes = num_genomes
        self.num_neurons = num_neurons
        self.reproduce_mode = reproduce_mode
        self.mutation_rate = mutation_rate

        self.neurons = np.zeros(self.num_neurons + 1)
        if genome is None:
            self.genome = [generate_genome() for _ in range(self.num_genomes)]
        else:
            self.genome = genome

    def predict(self, obs):
        active_sensors = []
        # this loop lists all sensory signals
        for g in self.genome:
            # get input sensor from genome
            temp = hex_to_int(extract_hex_sub(g, 0, 2))
            if temp <= self.num_observations:  # if temp is sensory
                # sensory neuron can trigger a connection, add to list
                active_sensors.append(temp)

        input_sensors = if_neuron_triggers(obs, active_sensors)
        active_map = create_active_map(self.genome)
        active_map = sorted(active_map.items())

        # sort so internal neurons are processed last

        # use active_map and input_sensors to calculate sensory input in neural network
        out_vec = np.zeros(self.num_actions + 1)
        for input_index, output_list in active_map:
            for key, conn_str in output_list:  # for each output attached to the input
                # split based on internal or output
                if key <= self.num_neurons:  # output is internal
                    if input_index < self.num_observations:
                        self.neurons[key - 1] += (input_sensors[input_index] * conn_str)  # add signal to internal
                    else:
                        self.neurons[key - 1] += (self.neurons[input_index - self.num_observations - 1] * conn_str)
                else:  # output is action
                    if input_index < self.num_observations:
                        out_vec[key - self.num_neurons] += (input_sensors[input_index] * conn_str)
                    else:
                        out_vec[key - self.num_neurons] += (
                                self.neurons[input_index - self.num_observations] * conn_str)

        out_vec = np.tanh(out_vec)
        action = np.array(movement_output(out_vec, np.int64(obs)))
        return action

    def reproduce_genome(self, other):
        assert isinstance(other, self.__class__)
        assert len(self.genome) == len(other.genome), "parents must have the same length of genome"
        child_genome = reproduce_genome(self.genome, other.genome, self.reproduce_mode)
        child_genome = clean_genome(mutate_genome(child_genome, self.mutation_rate))
        return child_genome


if __name__ == '__main__':
    state = [22, 24, 2, 0, 1, 0, 1, 1]
    gen = GeneticAlgorithm(num_observations=16,
                           num_actions=9,
                           num_neurons=3)

    for _ in range(100):
        obs = np.random.rand(16)
        gen.update_state(state)
        act = gen.predict(obs)
        print(act)
