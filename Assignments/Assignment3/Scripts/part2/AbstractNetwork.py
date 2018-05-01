from Node import Node
import sys

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
        self.nodes[node.id] = node

    def maxDegree(self):
        """
        Returns the maximum degree in this network
        """
        return max([x.degree() for x in self.nodes.values()])

    def size(self):
        """
        Returns network size
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
            nblist = []
            for elem in n.nodelist:
                nblist.append(elem.id)
            self.networkdict[n.id] = nblist

        niceprint = str(("\n".join("{}\t\t{}".format(k, v) for k, v in self.networkdict.items())) + "\n\n")
        return niceprint

    def getNode(self, identifier):
        """
        Returns node according to key
        """
        if identifier not in self.nodes:
            self.nodes[identifier] = Node(identifier)
            
        return self.nodes[identifier]


    def degreeSum(self):
        '''

        :return: sum of all degrees of the network (a bit unefficient )
        '''
        sum = 0
        for key, node in self.nodes.items():
            sum += node.degree()
        return sum

    def removeLink(self, node1, node2):
        if node1.hasLinkTo(node2) and node2.hasLinkTo(node1):
            node1.removeNode(node2)
            node2.removeNode(node1)
        else:
            print("Cannot remove link between ", str(node1), " and ", str(node2))

    def nbTriangle(self, node1, node2):
        if(not node1.hasLinkTo(node2)):
            return 0
        else:
            # Intersection is part of "set"
            intersect = set(node1.nodelist).intersection(node2.nodelist)
            return len(intersect)

    def edgeClusterCoeff(self, node1, node2):
        if(node1.degree() -1 == 0 or node2.degree()-1 == 0):
            return sys.maxsize
        else:
            return (self.nbTriangle(node1, node2) + 1) / float(min(node1.degree() - 1, node2.degree() - 1))