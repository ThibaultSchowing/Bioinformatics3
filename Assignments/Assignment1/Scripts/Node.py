#Bioinformatics 3 : Wiebke Schmitt & Thibault Schowing
#Usefull link to begin with classes: http://introtopython.org/classes.html

class Node:
    def __init__(self, identifier):
        """
        Sets node id and initialize empty node list that references its connected nodes
        """
        self.identifier = identifier

        # More about lists in Python 3.5:
        # https://docs.python.org/3.5/tutorial/datastructures.html
        self.neighbours_list = []

    def hasLinkTo(self, node):
        """
        Returns True if this node is connected to node asked for,
        False otherwise
        """
        return node in self.neighbours_list

    def addLinkTo(self, node):
        """
        Adds link from this node to parameter node (only if there is no link connection already),
        does not automatically care for a link from parameter node to this node
        """
        if node not in self.neighbours_list:
            self.neighbours_list.append(node)

    def degree(self):
        """
        Returns degree of this node
        """
        return len(self.neighbours_list)

    def __str__(self):
        """
        Returns id of node as string
        """
        return self.identifier
