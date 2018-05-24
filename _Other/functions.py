from itertools import combinations
import random


def find_cliques(network):
    """
    :param network: is a class that contains nodes and their connections
    :return: cliques of size 3, 4 and 5
    algorithm steps:
    1- for every pair A-B and C-D check whether there are edges between A and C, A and D, B and C and B and D
    2- if there are edges, then it's a clique
    4- For every clique identified, ABCD, check all proteins in the PPI network
    5- For additional protein E:
        if all interactions e-a, e-b, e-c and e-d exists, then ABCDE is a clique with size 5.
    """
    k = 3
    list_of_edges = network.edges
    while list_of_edges and k <= 5:
        # result

        # merge k-cliques into (k+1)-cliques
        cliques_1 = []
        for u, v in combinations(list_of_edges, 2):
            w = u ^ v
            if len(w) == 2:
                node1 = list(w)[0]
                node2 = list(w)[1]
                if network.nodes[node1].has_edge_to(network.nodes[node2]):
                    if (u | v) not in cliques_1:
                        cliques_1.append(u | v)

        # remove duplicates
        list_of_edges = list(map(set, cliques_1))
        if k == 3:
            cliques_3 = list_of_edges
        elif k == 4:
            cliques_4 = list_of_edges
        elif k == 5:
            cliques_5 = list_of_edges

        k += 1
    return  true_cliques(cliques_3, cliques_4, cliques_5)


# removing cliques that are a subset of other cliques
def true_cliques(cliques_3, cliques_4, cliques_5):
    false_cliques_4 = []
    for c4 in cliques_4:
        for c5 in cliques_5:
            if c4.issubset(c5):
                if c4 not in false_cliques_4:
                    false_cliques_4.append(c4)

    for item in false_cliques_4:
        cliques_4.remove(item)

    false_cliques_3 = []
    for c3 in cliques_3:
        for c4 in cliques_4:
            if c3.issubset(c4):
                if c3 not in false_cliques_3:
                    false_cliques_3.append(c3)

    for item in false_cliques_3:
        cliques_3.remove(item)

    return cliques_3, cliques_4, cliques_5


def evolving_net(network, t, step_plot=False):
    new_network = network
    c3_size = []
    c4_size = []
    c5_size = []
    for i in range(t):
        if random.choices([0, 1], [50, 50]) == [0]:  # 0 is for an edge deletion
            edge = list(random.choice(network.edges))
            p1 = list(edge)[0]
            p2 = list(edge)[1]
            new_network.nodes[p1].remove_edge(new_network.nodes[p2])
            new_network.nodes[p2].remove_edge(new_network.nodes[p1])
            network.edges.remove(edge)
        else:  # adding a random edge
            while True:
                node1 = random.choice(list(new_network.nodes.keys()))
                node2 = random.choice(list(new_network.nodes.keys()))
                if node1 != node2:
                    if node2 not in list(new_network.nodes[node1].neighbour_nodes):
                        new_network.nodes[node1].remove_edge(new_network.nodes[node2])
                        new_network.nodes[node2].remove_edge(new_network.nodes[node1])
                        network.edges.append({node1, node2})
                        break

        if step_plot:
            net_cliq3, net_cliq4, net_cliq5 = find_cliques(new_network)
            c3_size.append(len(net_cliq3))
            c4_size.append(len(net_cliq4))
            c5_size.append(len(net_cliq5))

    print("size 3", c3_size)
    print("size 4", c4_size)
    print("size 5", c5_size)


def randomised_net(network):
    for i in range(len(network.edges)*2):
        while True:
            edge1 = list(random.choice(network.edges))
            edge2 = list(random.choice(network.edges))
            if edge1 != edge2:
                p1, p2 = edge1[0], edge1[1]
                p3, p4 = edge2[0], edge2[1]
                # remove connections first
                if network.nodes[p1].has_edge_to(network.nodes[p4]) or \
                        network.nodes[p3].has_edge_to(network.nodes[p2]):
                    print("we are here:")
                    pass
                else:

                    network.nodes[p1].remove_edge(network.nodes[p2])
                    network.nodes[p2].remove_edge(network.nodes[p1])

                    network.nodes[p4].remove_edge(network.nodes[p3])
                    network.nodes[p3].remove_edge(network.nodes[p4])
                    network.edges.remove(edge1)
                    network.edges.remove(edge2)

                    network.nodes[p1].add_edge(network.nodes[p4])
                    network.nodes[p4].add_edge(network.nodes[p1])

                    network.nodes[p3].add_edge(network.nodes[p2])
                    network.nodes[p2].add_edge(network.nodes[p3])
                    network.edges.append({p1, p4})
                    network.edges.append({p2, p3})
                    break
