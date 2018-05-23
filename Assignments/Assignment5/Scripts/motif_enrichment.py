import random
from random import randint
from copy import deepcopy
from randomized_network import RandomizedNetwork



class MotifEnrichment:
    '''

    '''
    def __init__(self, n, network):
        self.original_network = deepcopy(network)

        cliques_sizes = [3, 4, 5]

        self.pis = []

        for i in cliques_sizes:

            # Number of Cliques of size i in the original network
            ci = len(self.original_network.find_cliques(i))

            # Number of clique of size i in the n randomized network

            nri = 0

            for j in range(0, n):
                # compute cliques of size i for the n randomized network
                rand_net_cliques = RandomizedNetwork(network).get_randomized_network().find_cliques(i)

                if len(rand_net_cliques) >= ci:
                    nri += 1

            # For each clique size i, compute:
            self.pis.append(nri/n)