from node import Node
import itertools
import copy



class GenericNetwork:
    def __init__(self):
        # key: node identifier, value: Node-object
        self.nodes = {}
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

    ''''
    
    '''
    def get_nodes(self):
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

    # def add_edge_str(self, node1, node2):
    #     """
    #
    #     :param node1:
    #     :param node2:
    #     :return:
    #     """
    #     # raise an error if the nodes are not in the network
    #     if node1 not in self.nodes.keys():
    #         raise KeyError('There is no node in the network with identifier:', node_1)
    #     if node2 not in self.nodes.keys():
    #         raise KeyError('There is no node in the network with identifier:', node_2)
    #
    #     # add the (undirected) edge
    #     self.nodes[node1].add_edge(self.nodes[node2])
    #     self.nodes[node2].add_edge(self.nodes[node1])

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
    def remove_link(self, node1, node2):
        """

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
            return True
        else:
            return False

    # Find all the cliques of k nodes in the network
    # We tried an other recursive manner (Bron-Kerbosch with pivot) but missed time to succeed
    def find_cliques(self, k):

        # main loop (recursive)
        def clique_loop(k, list):

            # Recursivity stop condition
            if k == 1:
                return list
            else:
                tmp_list = []
                for tuple in list:
                    for node1 in self.nodes.keys():
                        if node1 in tuple:
                            break
                        else:
                            for node2 in tuple:
                                hasLink = True

                                if not self.nodes[node1].has_edge_to(self.nodes[node2]):
                                    hasLink = False

                        if hasLink:
                            tmp_list.append(tuple + (node1,))

                return clique_loop(k - 1, tmp_list)

        # Here we call the main loop, the list argument contains a map object
        # nodelist == iterable containing all the nodes keys formatted: (x, )


        # http://www.secnetix.de/olli/Python/lambda_functions.hawk
        nodelist = map(lambda x: (x,), self.nodes.keys())
        lst = clique_loop(k, nodelist)
        ret = sorted(lst)
        ret = [ret for ret, _ in itertools.groupby(ret)]
        return ret
















        #
        # # find cliques of n nodes
        #
        # clique_result.increment()
        # print("Candidates: ", candidates)
        #
        #
        # # Stop condition
        # if not candidates and not excluded:
        #     if len(clique) >= self.SIZE_CLIQUE:
        #         clique_result.save_clique(clique)
        #     return
        #
        #
        # pivot = self.choose_random(candidates) or self.choose_random(excluded)
        # print("Pivot: ", pivot)
        # print("self.NEIGHBOURS[pivot] = ", self.NEIGHBOURS[pivot])
        #
        #
        # for v in list(candidates.difference(self.NEIGHBOURS[pivot])):
        #     new_candidates = candidates.intersection(self.NEIGHBOURS[v])
        #     print("New candidates: ", new_candidates)
        #     new_excluded = excluded.intersection(self.NEIGHBOURS[v])
        #     print("New excluded: ", new_excluded)
        #
        #     # recursion
        #     self.find_cliques(clique + [v], new_candidates, new_excluded, clique_result)
        #     candidates.remove(v)
        #     excluded.add(v)
        #
        #
        #
        #
        #
        #
        #
        #



