#Bioinformatics 3 : Wiebke Schmitt & Thibault Schowing
from Node import Node

class AbstractNetwork:
    """Abstract network definition, can not be instantiated"""

    def __init__(self, amount_nodes, amount_links):
        """
        Creates empty nodelist and call createNetwork of the extending class
        """
        self.nodes = {}
        self.__createNetwork__(amount_nodes, amount_links)

    def __createNetwork__(self, amount_nodes, amount_links):
        """
        Method overwritten by subclasses, nothing to do here
        """
        raise NotImplementedError

    def appendNode(self, node):
        """
        Appends node to network
        """
        self.nodes[node.identifier] = node

    def maxDegree(self):
        """
        Returns the maximum degree in this network
        """
        deg_list = []
        for key, value in self.nodes.items():
            deg_list.append(value.degree())

        #print("Debug: deg_list ", deg_list)
        #print("Debug: max degree: ", max(deg_list))
        return max(deg_list)

    def size(self):
        """
        Returns network size (here: number of nodes)
        """
        return len(self.nodes)

    def __str__(self):
        '''
        Any string-representation of the network (something simply is enough)
        '''
        # will contain: {identifier : neighbours} -> dict are printed pretty nicely
        self.networkdict = {}
        for n in self.nodes.values():
            # n is a node -> contains identifier and neighbours
            self.networkdict[n.identifier] = n.neighbours_list
        return str(self.networkdict)



    def getNode(self, identifier):
        """
        Returns node according to key
        """
        return self.nodes[identifier]