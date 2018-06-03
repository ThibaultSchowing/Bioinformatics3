import copy
import collections

class BooleanNetwork:
    def __init__(self, matrix):
        # Propagation Matrix
        self.matrix = matrix

        # Number of genes/nodes
        self.nb_bits = len(matrix)

        # Number of possible states (in our example 2**6 = 64)
        self.nb_states = int(2**self.nb_bits)

        # For each gene, we can set a threshold. Here we assume it's 0 for all of them
        self.threshold = [0] * self.nb_bits


    def int_to_binary(self, n):
        """
        Convert an integer to binary
        /!\ Uses the variable: SELF.NB_BITS !

        :Source: https://stackoverflow.com/questions/10411085/converting-integer-to-binary-in-python
        :param n: Integer
        :return: map object -> use list comprehension to print/loop in etc
        """
        ret = bin(n)[2:].zfill(self.nb_bits)
        return list(map(int, format(ret)))

    def binary_to_int(self, n):
        """
        Converts binary number (list) to Integer
        :param n: List of bits
        :return: the list converted to int
        """
        ret = ""
        for bit in n:
            ret += str(bit)
        ret_int = int(ret,2)
        return ret_int


    def get_states_sequence(self, start_state):
        """
        From a passed starting state (INT), calculates all the following states and stops when a loop is detected.
        :param start_state: INT - number of the starting state
        :return: The sequence of states,
        """

        binary_current_state = self.int_to_binary(start_state)

        binary_next_state = [0] * self.nb_bits
        states_sequence = [start_state]

        state_not_visited = True

        # While the state haven't already been visited...(while not orbit)
        while state_not_visited:

            for i in range(0, self.nb_bits):
                sum_next_state = 0
                for j in range(0, self.nb_bits):
                    # print("Fucking i: ", i, " and j: ", j)
                    # print(binary_current_state[j] * self.matrix[j][i])
                    sum_next_state += binary_current_state[j] * self.matrix[j][i]

                # Now we can set the next state for this gene
                if sum_next_state > self.threshold[i]:
                    binary_next_state[i] = 1
                else:
                    binary_next_state[i] = 0

            # If the next state doesn't already exist, we add it to the states list and continue
            # If not, we add it and end the while loop

            #print("CURRENT STATE: ", binary_next_state)
            if self.binary_to_int(binary_next_state) not in states_sequence:
                states_sequence.append(self.binary_to_int(binary_next_state))
            else:
                states_sequence.append(self.binary_to_int(binary_next_state))
                state_not_visited = False

            # The state now (starting state) is the next state

            binary_current_state = copy.copy(binary_next_state)

        return states_sequence

    def orbit(self, start_state):
        """
        Return many things, orbit is a random name here
        :param start_state:
        :return: see comments below
        """
        # Sequence from start state -> stabilization
        sequence = self.get_states_sequence(start_state)

        # At which state it closes its orbit
        closure = sequence[-1]

        # Basin = states leading to periodic orbits (cyclic attractor)
        partial_basin = sequence[0:sequence.index(closure)]

        # Periodic orbit (cyclic attractor) of the sequence
        periodic_orbit = sequence[sequence.index(closure):len(sequence) - 1]

        # Size of the orbit
        orbit_size = len(sequence) - sequence.index(closure) - 1

        return orbit_size, periodic_orbit, closure, partial_basin


    def count_attractors(self):
        """
        # Returns a counter containing the sets of attractors and their occurence
        # In our case:
        # Counter({frozenset({0}): 23,
        #          frozenset({1, 3, 7, 13, 55, 23, 63}): 21,
        #          frozenset({39, 19, 5, 31}): 11,
        #          frozenset({18, 26, 4, 36}): 9})
        #
        # Notice that unfortunately here the order of the attractor is not maintained
        # Source: https://stackoverflow.com/questions/37295981/python-creating-a-dictionary-with-key-as-a-set-and-value-as-its-count
        #

        :return:
        """
        all_attractors_list = [sorted(self.orbit(i)[1]) for i in range(self.nb_states)]
        attractors_count = collections.Counter(frozenset(x) for x in all_attractors_list)

        return attractors_count


    def average_occupancies_in_orbit(self, orbit, print_steps = None):
        """
        Count occurence of ABCDEF activated in each states
        :param orbit:
        :return: list of percentages like [0.25, 0.5, 0.25, 0.5, 0.5, 0.0]
        """
        total_bits = [0 for _ in range(0, self.nb_bits)]
        percentages = [0.0 for _ in range(0, self.nb_bits)]

        # For every state, convert to binary and increment the occupancy
        for state in orbit:
            bin = self.int_to_binary(state)

            # if the optional parameter is true, print the binary states
            # allow to see more clearely the evolution of the different gene activation
            if print_steps:
                print(bin)
            #Increment here
            for i in range(0, len(bin)):
                total_bits[i] += bin[i]
        # Calculate percentages
        total_elem = len(orbit)
        for i in range(0, self.nb_bits):
            percentages[i] = total_bits[i] / total_elem

        return percentages



    def get_basin_of_attraction(self):
        """

        :return:
        """

        sequence_set = collections.defaultdict(list)

        for i in range(0, self.nb_states):
            orbit = self.orbit(i)
            unique_orbit_string = str(sorted(orbit[1]))
            # We have the "previous steps" and the cyclic attractor -> add the previous steps to the set corresponding to the attractor to have the full basin
            sequence_set[unique_orbit_string].extend(orbit[3])
            # To have the whole basin, we add also the cycle
            sequence_set[unique_orbit_string].extend(orbit[1])

        for e in sequence_set:
            sequence_set[e] = list(set(sequence_set[e]))

        return sequence_set