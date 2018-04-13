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

    def maxDegree(self):
        """
        Returns the maximum degree in this network
        """

    def size(self):
        """
        Returns network size (here: number of nodes)
        """

    def __str__(self):
        '''
        Any string-representation of the network (something simply is enough)
        '''

    def getNode(self, identifier):
        """
        Returns node according to key
        """