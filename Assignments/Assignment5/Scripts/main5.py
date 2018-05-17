from generic_network import GenericNetwork
import random
import pickle


def remove_contained_cliques(res1, res2, res3):
    """

    :param clik3: cliques of 3 nodes
    :param clik4: cliques of 4 nodes
    :param clik5: cliques of 5 nodes
    :return: remove the smaller cliques contained in the big ones
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
    '''
        http://thispointer.com/python-check-if-a-list-contains-all-the-elements-of-another-list/
        check if list1 contains all elements in list2
    '''
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

        # Pick a node with a degree > 0
        node1 = network.get_node(random.sample(list(network.get_nodes()), 1)[0])
        node2 = network.get_node(random.sample(list(network.get_nodes()), 1)[0])

        # If we want to add an edge, the two nodes mustn't be connected.
        if add:
            while node1.has_edge_to(node2) or node1 == node2:
                node2 = network.get_node(random.sample(list(network.get_nodes()), 1)[0])
        else:
            while not node1.has_edge_to(node2) or node1 == node2:
                node2 = network.get_node(random.sample(list(network.get_nodes()), 1)[0])

        return (node1, node2)

    # return cliques values for t = 100
    ret1 = []
    ret2 = []
    ret3 = []

    for _ in range(0, t):

        # Add or delete edge ? random
        add = bool(random.getrandbits(1))

        nodes = get_two_random_nodes(add)

        if not add:
            network.remove_link(nodes[0], nodes[1])
        else:
            network.add_edge(nodes[0], nodes[1])

        # For t = 100 - plot each step.
        if t == 100:
            res1 = network.find_cliques(3)
            res2 = network.find_cliques(4)
            res3 = network.find_cliques(5)
            remove_contained_cliques(res1, res2, res3)
            ret1.append(res1)
            ret2.append(res2)
            ret3.append(res3)

    # return the different clique values for all the 100 steps (empty if t != 100)
    return (ret1, ret2, ret3)





print("Assignment 5 - Schmitt Schowing")

PATH = "../Data/sup51/chicken_network.tsv"
net = GenericNetwork()
net.read_from_tsv(PATH)


res1 = net.find_cliques(3)
res2 = net.find_cliques(4)
res3 = net.find_cliques(5)

# Total number of cliques != requested.
print("\n\nNumber of cliques of 3 nodes: ", len(res1))
print("Number of cliques of 4 nodes: ", len(res2))
print("Number of cliques of 5 nodes: ", len(res3))

remove_contained_cliques(res1, res2, res3)


print("\n\nNumber of cliques of 3 nodes after cleaning: ", len(res1))
print("Number of cliques of 4 nodes after cleaning: ", len(res2))
print("Number of cliques of 5 nodes after cleaning: ", len(res3))


# 100 EVOLUTION - reset the network - too long

# evo100_net = GenericNetwork()
# evo100_net.read_from_tsv(PATH)
# evolution_data = evolve(100, evo100_net)

#saving structure after a long runtime (but here it's too long !)
# afile = open("pikled.txt", 'wb')
# pickle.dump(evolution_data, afile)
# afile.close()

# reload the file later
# file2 = open("pikled.txt", 'rb')
# new_evolution_data = pickle.load(file2)
# file2.close()



print("\n\nNumber of cliques of 3 nodes after 100 evolutions: ", len(evo100_res1))
print("Number of cliques of 4 nodes after 100 evolutions: ", len(evo100_res2))
print("Number of cliques of 5 nodes after 100 evolutions: ", len(evo100_res3))


# Too damn long !
# 1000 EVOLUTION - reset the network
#
# evo1000_net = GenericNetwork()
# evo1000_net.read_from_tsv(PATH)
#
# evolve(1000, evo1000_net)
#
# evo1000_res1 = net.find_cliques(3)
# evo1000_res2 = net.find_cliques(4)
# evo1000_res3 = net.find_cliques(5)
#
# remove_contained_cliques(evo1000_res1, evo1000_res2, evo1000_res3)
#
#
# print("\n\nNumber of cliques of 3 nodes after 1000 evolutions: ", len(evo1000_res1))
# print("Number of cliques of 4 nodes after 1000 evolutions: ", len(evo1000_res2))
# print("Number of cliques of 5 nodes after 1000 evolutions: ", len(evo1000_res3))

