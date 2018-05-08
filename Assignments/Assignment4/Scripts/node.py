class Node:
    def __init__(self, identifier):
        self.identifier = identifier
        # contains the identifiers of other nodes connected to this node
        self.neighbour_nodes = set()

        # fields for the layout algorithm
        self.pos_x = 0
        self.pos_y = 0
        self.force_x = 0
        self.force_y = 0
        self.charge = 0

    def __eq__(self, node):
        """
        :param node: Node-object
        :return: True if the other node has the same identifier, False otherwise
        """
        return self.identifier == node.identifier

    def __str__(self):
        """
        :return: string representation of the node identifier
        """
        return str(self.identifier)

    def has_edge_to(self, node):
        """
        :param node: Node-object
        :return: True if this node has an edge to the other node, False otherwise
        """
        return node.identifier in self.neighbour_nodes

    def add_edge(self, node):
        """
        Adds an edge to the other node by adding it to the neighbour-nodes.
        :param node: Node-object
        """
        self.neighbour_nodes.add(node.identifier)

    def remove_edge(self, node):
        """
        Removes the edge to the other node, if that edge exists, by removing the other node from the neighbour nodes.
        :param node: Node-object
        """
        self.neighbour_nodes.discard(node.identifier)

    def degree(self):
        """
        :return: the degree of this node (= number of neighbouring nodes)
        """
        return len(self.neighbour_nodes)