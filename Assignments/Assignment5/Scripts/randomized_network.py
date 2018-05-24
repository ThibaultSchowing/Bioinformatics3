from node import Node
from generic_network import GenericNetwork
import random
from random import randint
from copy import deepcopy

def intersect(a, b):
    """ return the intersection of two lists """
    return list(set(a) & set(b))

class RandomizedNetwork:
    '''
    Randomize a given network
    '''
    def __init__(self, network):
        '''
        Initialization: deep copy the given network and randomize the copy
        '''
        self.rand_network = deepcopy(network)

        m = len(self.rand_network.edges)

        for _ in range(0, 2*m):

            edges = self.rand_network.edges

            # Break if we found two "good" edges to switch
            while(True):
                edge1 = random.choice(edges)
                edge2 = random.choice(edges)

                if not edge1 == edge2:
                    n1, n2 = list(edge1)[0], list(edge1)[1]
                    n3, n4 = list(edge2)[0], list(edge2)[1]

                    if n1 != n4 and n2 != n3:
                        # check if the link we want to create don't already exist
                        if self.rand_network.nodes[n1].has_edge_to(self.rand_network.nodes[n4]) or self.rand_network.nodes[n2].has_edge_to(self.rand_network.nodes[n3]):
                            continue
                        else:
                            # remove the link n1 - n2 and n3 - n4 and create the links n1 - n4 and n2 - n3

                            # Remove neighbour from node list
                            self.rand_network.nodes[n1].remove_edge(self.rand_network.nodes[n2])
                            self.rand_network.nodes[n2].remove_edge(self.rand_network.nodes[n1])

                            self.rand_network.nodes[n4].remove_edge(self.rand_network.nodes[n3])
                            self.rand_network.nodes[n3].remove_edge(self.rand_network.nodes[n4])

                            # Add the new edge
                            self.rand_network.nodes[n1].add_edge(self.rand_network.nodes[n4])
                            self.rand_network.nodes[n4].add_edge(self.rand_network.nodes[n1])

                            self.rand_network.nodes[n3].add_edge(self.rand_network.nodes[n2])
                            self.rand_network.nodes[n2].add_edge(self.rand_network.nodes[n3])
                            break

    def get_randomized_network(self):
        return self.rand_network