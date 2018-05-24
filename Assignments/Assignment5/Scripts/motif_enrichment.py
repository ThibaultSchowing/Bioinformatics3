from copy import deepcopy
from randomized_network import RandomizedNetwork

class MotifEnrichment:
    '''
    Randomize a network n time and process p-values
    '''
    def __init__(self, n, network):
        self.original_network = deepcopy(network)

        # cliques_sizes = [3, 4, 5]

        self.pis = []

        # cliques of size 3, 4 and 5 of the original network
        print("Find Cliques for Original Network")
        cliques = self.original_network.find_cliques()
        original_clique3 = len(cliques[0])
        original_clique4 = len(cliques[1])
        original_clique5 = len(cliques[2])

        nr3 = 0
        nr4 = 0
        nr5 = 0

        # N randomized network
        for j in range(0, n):
            print("Create randomized network and find cliques step ", j)
            print("Randomize network...")
            rand_net_tmp = RandomizedNetwork(network).get_randomized_network()
            print("Done !")

            print("Calculate cliques...")
            # NOTE: Because of the random structure, finding cliques takes longer here than in the original rat network.
            rand_cliques3, rand_cliques4, rand_cliques5 = rand_net_tmp.find_cliques()
            print("Done !")

            cj3 = len(rand_cliques3)
            cj4 = len(rand_cliques4)
            cj5 = len(rand_cliques5)

            print("Temporary Cliques: ", cj3, " - ", cj4, " - ", cj5)

            if cj3 >= original_clique3:
                nr3 += 1
            if cj4 >= original_clique4:
                nr4 += 1
            if cj5 >= original_clique5:
                nr5 += 1

        p3 = nr3/n
        p4 = nr4/n
        p5 = nr5/n

        self.pis.append(p3)
        self.pis.append(p4)
        self.pis.append(p5)