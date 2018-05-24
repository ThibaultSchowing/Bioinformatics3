from node import Node
from itertools import combinations
import copy


class GenericNetwork:
    def __init__(self):
        # key: node identifier, value: Node-object
        self.nodes = {}
        self.edges = []
        self.nb_edges = 0

    def read_from_tsv(self, file_path):
        """
        Reads white-space-separated files that contain two or more columns. The first two columns contain the
        identifiers of two nodes that have an undirected edge. The two nodes are added to the network.
        :param file_path: path to the file
        """
        # clear the prior content of the network
        self.nodes = {}

        # open the file for reading
        with open(file_path, 'r') as file:
            # iterate over the lines in the file
            for line in file:
                #
                columns = line.split()

                # skip lines that do not have two node identifiers
                if len(columns) < 2:
                    continue

                # We ignore if there is more than one connection
                # create the two nodes and remove potential whitespace such as new-line from their identifiers
                node_1 = Node(columns[0].strip())
                node_2 = Node(columns[1].strip())
                # add the nodes and the edge between them to the network
                self.add_node(node_1)
                self.add_node(node_2)
                self.add_edge(node_1, node_2)

        # set (or reset) the self.edges list with all unique edge.
        self.reset_edges()

    def reset_edges(self):
        # Add the edges avoiding the duplicates (A-B and B-A)
        tmp_edges = []
        visited = []
        for node in self.nodes:
            visited.append(node)
            for neighbour in self.nodes[node].neighbour_nodes:
                if neighbour not in visited:
                    tmp_edges.append({node, neighbour})
        self.edges = tmp_edges

        #print("Nb edges: ", self.nb_edges)
        #print("len edges: ", len(self.edges))

    def get_nodes(self):
        """
        :return: the dict of nodes
        """
        return copy.deepcopy(self.nodes)

    def add_node(self, node):
        """
        Adds the specified node to the network.
        :param node: Node-object
        """
        if node.identifier not in self.nodes.keys():
            self.nodes[node.identifier] = node

    def add_edge(self, node_1, node_2):
        """
        Adds an (undirected) edge between the two specified nodes.
        :param node_1: Node-object
        :param node_2: Node-object
        :raises: KeyError if either node is not in the network
        """
        # raise an error if the nodes are not in the network
        if node_1.identifier not in self.nodes.keys():
            raise KeyError('There is no node in the network with identifier:', node_1)
        if node_2.identifier not in self.nodes.keys():
            raise KeyError('There is no node in the network with identifier:', node_2)

        # add the (undirected) edge
        self.nodes[node_1.identifier].add_edge(node_2)
        self.nodes[node_2.identifier].add_edge(node_1)

        # increment the number of edge of 1
        self.nb_edges += 1
        self.edges.append({str(node_1), str(node_2)})

    def get_node(self, identifier):
        """
        :param identifier: node identifier
        :return: Node-object corresponding to the given node identifier, if the node is in the network
        :raises: KeyError if there is no node with that identifier in the network
        """
        if identifier not in self.nodes.keys():
            raise KeyError('There is no node in the network with identifier:', identifier)
        return self.nodes[identifier]

    def has_edge(self, node_1, node_2):
        """
        :param node_1: Node-object
        :param node_2: Node-object
        :return: True if the two nodes have an (undirected) edge, False otherwise
        :raises: KeyError if either node is not in the network
        """
        # raise an error if the nodes are not in the network
        if node_1.identifier not in self.nodes.keys():
            raise KeyError('There is no node in the network with identifier:', node_1)
        if node_2.identifier not in self.nodes.keys():
            raise KeyError('There is no node in the network with identifier:', node_2)

        return node_1.has_edge_to(node_2) and node_2.has_edge_to(node_1)

    def size(self):
        """
        :return: number of nodes in the network
        """
        return len(self.nodes.keys())

    def nb_edges(self):
        """
        :return: number of edges
        """
        return self.nb_edges

    def max_degree(self):
        """
        :return: highest node degree in the network, 0 if there are no nodes in the network
        """
        return max([node.degree() for node in self.nodes.values()], default=0)

    def __str__(self):
        '''
        Any string-representation of the network (something simply is enough)
        '''
        # will contain: {identifier : neighbours} -> dict are printed pretty nicely
        self.networkdict = {}
        for n in self.nodes.values():
            # n is a node -> contains identifier and neighbours
            nblist = []
            for elem in n.neighbour_nodes:
                nblist.append(elem)
            self.networkdict[n.identifier] = nblist

        niceprint = str(("\n".join("{}\t\t{}".format(k, v) for k, v in self.networkdict.items())) + "\n\n")
        return niceprint

    # remove the link between two nodes and return true or false if link don't exist.
    def remove_edge(self, node1, node2):
        """
        Remove edge between two nodes in the different structures.
        :param node1:
        :param node2:
        :return:
        """

        if isinstance(node1, str):
            node1 = self.nodes[node1]
        if isinstance(node2, str):
            node2 = self.nodes[node2]

        if node1.has_edge_to(node2) and node2.has_edge_to(node1):
            node1.remove_edge(node2)
            node2.remove_edge(node1)
            self.nb_edges -= 1
            self.edges.remove({str(node1), str(node2)})
            return True
        else:
            return False

    @staticmethod
    def remove_contained_cliques(cliques3, cliques4, cliques5):
        """
        Remove the cliques of size n-1 included in the cliques of size n
        :param cliques3:
        :param cliques4:
        :param cliques5:
        :return:
        """
        # Contains all cliques 4 contained in the list of cliques of size 5
        contained_cliques_4 = []
        # For each cliques 4, check if it is part on a clique 5
        for clique4 in cliques4:
            for clique5 in cliques5:
                if clique4.issubset(clique5):
                    if clique4 not in contained_cliques_4:
                        contained_cliques_4.append(clique4)

        # Remove the contained cliques
        for clique in contained_cliques_4:
            cliques4.remove(clique)

        # Now the clique 4 list is emptied of its bad cliques, we can check for the size 3
        contained_cliques_3 = []
        for clique3 in cliques3:
            for clique4 in cliques4:
                if clique3.issubset(clique4):
                    if clique3 not in contained_cliques_3:
                        contained_cliques_3.append(clique3)

        for clique in contained_cliques_3:
            cliques3.remove(clique)

        return cliques3, cliques4, cliques5

    def find_cliques(self):
        """
        # Finds cliques of size 3, 4 and 5
        # second attempt with the set of connections
        # HELP SOURCE: https://medium.com/100-days-of-algorithms/day-64-k-clique-c03fdc565b1e

        :return: the cliques, without the smaller cliques already included in bigger ones
        """
        k = 3
        edges_list = self.edges

        # While there is edges and k <=5
        while edges_list and k <= 5:

            cliques_tmp = []
            for u, v in combinations(edges_list, 2):
                w = u ^ v
                if len(w) == 2:
                    node1 = list(w)[0]
                    node2 = list(w)[1]
                    if self.nodes[node1].has_edge_to(self.nodes[node2]):
                        if (u | v) not in cliques_tmp:
                            cliques_tmp.append(u | v)
            # We need to remove eventual duplicates (set)

            edges_list = list(map(set, cliques_tmp))
            if k == 3:
                cliques3 = edges_list
            elif k == 4:
                cliques4 = edges_list
            elif k == 5:
                cliques5 = edges_list

            k += 1

        return self.remove_contained_cliques(cliques3, cliques4, cliques5)
