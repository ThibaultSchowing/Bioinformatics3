from generic_network import GenericNetwork
import random
from random import randint
import matplotlib.pyplot as plt
from randomized_network import RandomizedNetwork
from motif_enrichment import MotifEnrichment


def remove_contained_cliques(res1, res2, res3):
    """

    :param clik3: cliques of 3 nodes
    :param clik4: cliques of 4 nodes
    :param clik5: cliques of 5 nodes
    :return: remove the smaller cliques contained in the big ones as requested
    """
    # If the clique of 4 is already in a clique of 5 -> remove
    for clique5 in res3:
        for clique4 in res2:
            if contains(clique5, clique4):
                res2.remove(clique4)
        # Same with size 3
        for clique3 in res1:
            if contains(clique5, clique3):
                res1.remove(clique3)

    for clique4 in res2:
        for clique3 in res1:
            if contains(clique4, clique3):
                res1.remove(clique3)

def contains(list1, list2):
    """
    http://thispointer.com/python-check-if-a-list-contains-all-the-elements-of-another-list/
    check if list1 contains all elements in list2

    :param list1:
    :param list2:
    :return: boolean value
    """
    result = all(elem in list1 for elem in list2)
    return bool(result)


def evolve(t, network, plot = None):
    """
    Randomly select two nodes and delete the edge if existing or add it otherwise

    :param t: number of time steps
    :param network: network class object
    :return:
    """

    def get_two_random_nodes(add):
        """
        :add: if "add" is true, we want to add an edge so the two nodes must not be connected
        :return: two different random nodes from the network
        """

        # Pick a node with a degree > 1
        node1 = network.get_node(random.sample(list(network.get_nodes()), 1)[0])
        node2 = network.get_node(random.sample(list(network.get_nodes()), 1)[0])

        while not node1.degree() > 1:
            node1 = network.get_node(random.sample(list(network.get_nodes()), 1)[0])

        while not node2.degree() > 1:
            node2 = network.get_node(random.sample(list(network.get_nodes()), 1)[0])

        # If we want to add an edge, the two nodes mustn't be connected. To avoid blockage
        # it is necessary to rechoose both nodes.
        if add:
            while node1.has_edge_to(node2) or node1 == node2:
                node1 = network.get_node(random.sample(list(network.get_nodes()), 1)[0])
                node2 = network.get_node(random.sample(list(network.get_nodes()), 1)[0])
        else:
            # if the node are note connected, take a random neighbour of node1
            while not node1.has_edge_to(node2) or node1 == node2:
                node1_list = node1.get_neighbours()
                node2 = network.get_node(node1_list[randint(0,len(node1_list)-1)])

        return (node1, node2)

    # return cliques values for t = 100
    ret1 = []
    ret2 = []
    ret3 = []

    for _ in range(0, t):
        print("Evolution step: ", _)

        # 1 = Add or 0 = delete edge
        add = bool(random.getrandbits(1))

        # Get to nodes according to the decision to add or remove an edge
        nodes = get_two_random_nodes(add)

        if not add:
            network.remove_link(nodes[0], nodes[1])
        else:
            network.add_edge(nodes[0], nodes[1])

        # For t = 100 - plot each step.
        if t == 100:
            print("Calculating intermediate cliques...")
            res1 = network.find_cliques(3)
            res2 = network.find_cliques(4)
            res3 = network.find_cliques(5)
            remove_contained_cliques(res1, res2, res3)

            # Save the number of cliques of size 3, 4 and 5 after each step
            ret1.append(len(res1))
            ret2.append(len(res2))
            ret3.append(len(res3))

    # return the different clique values for all the 100 steps (empty if t != 100)
    return (ret1, ret2, ret3)


#################################################################################
#  MAIN
#################################################################################


if __name__== "__main__":

    print("Assignment 5 - Schmitt Schowing\n\n")

    # (b) - Read Network
    PATH = "../Data/sup53/rat_network.tsv"
    net = GenericNetwork()
    net.read_from_tsv(PATH)

    # # (c) - Count cliques
    # res1 = net.find_cliques(3)
    # res2 = net.find_cliques(4)
    # res3 = net.find_cliques(5)
    #
    # # Total number of cliques
    # print("\n\nNumber of cliques of 3 nodes: ", len(res1))
    # print("Number of cliques of 4 nodes: ", len(res2))
    # print("Number of cliques of 5 nodes: ", len(res3))
    #
    #
    # # # Do not count the cliques of smaller size that are contained in a larger
    # # # clique.
    # # remove_contained_cliques(res1, res2, res3)
    # #
    # #
    # # print("\n\nNumber of cliques of 3 nodes after cleaning: ", len(res1))
    # # print("Number of cliques of 4 nodes after cleaning: ", len(res2))
    # # print("Number of cliques of 5 nodes after cleaning: ", len(res3))
    #
    #
    #
    #
    #
    #
    # # 100 EVOLUTION - reset the network
    #
    # print("\n\n----------------------------------------------------------------"
    #       "\n                       Network Evolution"
    #       "\n----------------------------------------------------------------\n")
    #
    #
    # print("Start evolution 100 time steps.")
    #
    # evo100_net = GenericNetwork()
    # evo100_net.read_from_tsv(PATH)
    # evolution_data_100 = evolve(100, evo100_net)
    #
    # print("Evolution done. Counting cliques.")
    #
    # evo100_res1 = evo100_net.find_cliques(3)
    # evo100_res2 = evo100_net.find_cliques(4)
    # evo100_res3 = evo100_net.find_cliques(5)
    #
    # # remove_contained_cliques(evo100_res1, evo100_res2, evo100_res3)
    #
    # print("\n\nNumber of cliques of 3 nodes after 100 evolutions: ", len(evo100_res1))
    # print("Number of cliques of 4 nodes after 100 evolutions: ", len(evo100_res2))
    # print("Number of cliques of 5 nodes after 100 evolutions: ", len(evo100_res3))
    #
    # print("Plot Evolution Data")
    #
    # plt.plot(evolution_data_100[0], label='Cliques of size 3')
    # plt.plot(evolution_data_100[1], label='Cliques of size 4')
    # plt.plot(evolution_data_100[2], label='Cliques of size 5')
    # plt.xlabel("Evolution")
    # plt.ylabel("Number of cliques")
    # plt.legend()
    # plt.show()
    #
    #
    #
    # # Too damn long !
    # # 1000 EVOLUTION - reset the network
    #
    #
    # print("Reset Network")
    # evo1000_net = GenericNetwork()
    # evo1000_net.read_from_tsv(PATH)
    #
    # print("Start evolution 1000 time steps.")
    # evolution_data_1000 = evolve(1000, evo1000_net)
    #
    # print("Counting cliques for the 1000 time evolved network")
    # evo1000_res1 = evo1000_net.find_cliques(3)
    # evo1000_res2 = evo1000_net.find_cliques(4)
    # evo1000_res3 = evo1000_net.find_cliques(5)
    #
    # # remove_contained_cliques(evo1000_res1, evo1000_res2, evo1000_res3)
    #
    #
    # print("\n\nNumber of cliques of 3 nodes after 1000 evolutions: ", len(evo1000_res1))
    # print("Number of cliques of 4 nodes after 1000 evolutions: ", len(evo1000_res2))
    # print("Number of cliques of 5 nodes after 1000 evolutions: ", len(evo1000_res3))



    # print("\n\n----------------------------------------------------------------"
    #       "\n                       Randomized network"
    #       "\n----------------------------------------------------------------\n")


    # print("Original Network ")
    # rat_net = GenericNetwork()
    # rat_net.read_from_tsv("../Data/sup53/rat_network.tsv")
    #
    # print("nb cliques 3: ", len(rat_net.find_cliques(3)))
    #
    #
    # print("Randomized Network ")
    # randomized_net = RandomizedNetwork(rat_net).get_randomized_network()
    # print("nb cliques rand: ", len(randomized_net.find_cliques(3)))

    #-------------------------------------------------------------------
    #   Motif Enrichment
    #-------------------------------------------------------------------

    rat_net = GenericNetwork()
    rat_net.read_from_tsv("../Data/sup53/rat_network.tsv")
    print("Start Motif Enrichment")
    enrich = MotifEnrichment(100, rat_net)
    print("P-Values: ", enrich.pis)