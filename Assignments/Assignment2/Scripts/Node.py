# Node class, assignment 1
class Node:
    def __init__(self, identifier):
        """
        Sets node id and initialize empty node list that references its connected nodes
        """
        self.id = identifier
        self.nodelist = []
        
    def hasLinkTo(self, node):
        """
        Returns True if this node is connected to node asked for, 
        False otherwise
        """
        return (node in self.nodelist)
        
    def addLinkTo(self, node):
        """
        Adds link from this node to parameter ode (only if there is no link connection already),
        does not automatically care for a link from parameter node to this node
        """
        if (~self.hasLinkTo(node)):
            self.nodelist.append(node)      

    def degree(self):
        """
        Returns degree of this node
        """
        return len(self.nodelist)
        
    def __str__(self):
        """
        Returns id of node as string
        """
        return str(self.id)
    
    def getNodeSet(self):
        return set(self.nodelist)

    def removeNode(self,node):
        self.nodelist.remove(node)

