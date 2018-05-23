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

        m = self.rand_network.nb_edges

        for _ in range(0, 2*m):
            #print("debug loop: ", _)

            # Randomly select 2 nodes with degree > 0
            def choose_random_node():
                return self.rand_network.get_node(random.sample(list(self.rand_network.get_nodes()), 1)[0])

            def choose_two_nodes_condition():
                """
                Chose two nodes
                 - not the same nodes
                 - with more than 0 neighbour
                 -
                :return:
                """

                node01 = choose_random_node()
                node11 = choose_random_node()

                while not node01.degree() > 0 or node01.has_edge_to(node11):
                    node01 = choose_random_node()

                while (not node11.degree() > 0 and node11 != node01) or node11.has_edge_to(node01):
                    node11 = choose_random_node()

                return node01, node11


            # CHOSE TWO RANDOM NODES - not identical, with degree > 1
            node01, node11 = choose_two_nodes_condition()

            # Randomly select a neighbour in the neighbours lists !!!!! not already connected to node 11 !!!!
            # #TODO proof to self link and duplicate link
            # #UPDATE self link ok, as the two nodes are different

            # Below: choose two node in the neighbour list of node01 and node 11
            # the resulting edges should be switched without producing duplicate nodes

            def chose_rand_neighbour(list):
                return self.rand_network.get_node(list[randint(0, len(list) - 1)])

            # chose 02 and 12 a random neighbour of 01 and 11
            # In the next while loop, all random operation a executed again to avoid blockage.

            node02 = chose_rand_neighbour(node01.get_neighbours())
            node12 = chose_rand_neighbour(node11.get_neighbours())

            # chose a random other neighbour !! Might cause blockage if neighbour are all connected to node 01
            while node01.has_edge_to(node12) or node11.has_edge_to(node02):
                node01, node11 = choose_two_nodes_condition()

                node02 = chose_rand_neighbour(node01.get_neighbours())
                node12 = chose_rand_neighbour(node11.get_neighbours())


            # e1 = (node01, node02) -> (node01, node12)
            # e2 = (node11, node12) -> (node 11, node02)

            node01.remove_edge(node02)
            node01.add_edge(node12)

            node11.remove_edge(node12)
            node11.add_edge(node02)



    def get_randomized_network(self):
        return self.rand_network