#Bioinformatics 3 : Wiebke Schmitt & Thibault Schowing
from AbstractNetwork import AbstractNetwork
from Node import Node
import random # you will need it :-)

class RandomNetwork(AbstractNetwork):
    """Random network implementation of AbstractNetwork"""

    def __createNetwork__(self, amount_nodes, amount_links): # remaining methods are taken from AbstractNetwork
        """
        Creates a random network
        1. Build a list of n nodes
        2. For i=#links steps, add a connection between for two randomly chosen nodes that are not yet connected
        """

        print("debug: Init RandomNetwork")

        random.seed()

        self.maxLink = ((amount_nodes * (amount_nodes - 1)) / 2)

        if amount_links > self.maxLink:
            # https://docs.python.org/2/library/exceptions.html
            raise ValueError("The requested number of link (amount_links) is too high compared to the number of nodes (amount_nodes).")

        # Probability for an edge between two randomly selected nodes.
        self.probability = amount_links / self.maxLink

        # Average degree
        self.averageDegree = (2 * amount_links)/amount_nodes

        # Creation of the nodes with identifier from 0 to amount_nodes - 1
        # and append them to the network with the AbstractNetwork's function
        for i in range(0, amount_nodes):
            self.appendNode(Node(i))


        # Create "amount_links" random connection between two nodes.
        # Verify if the connection already exists and if it is connecting the node to itself
        # Usefull help: https://stackoverflow.com/questions/22842289/generate-n-unique-random-numbers-within-a-range

        for i in range(0, amount_links):
            self.randNum = random.sample(range(0, amount_nodes), 2)

            self.tmpNode1 = self.nodes[self.randNum[0]]
            self.tmpNode2 = self.nodes[self.randNum[1]]

            # Controls

            if not self.randNum[0] == self.randNum[1] and not self.tmpNode1.hasLinkTo(self.tmpNode2):
                # Not the same and not already connected
                self.symetricConnection(self.tmpNode1, self.tmpNode2)



    def symetricConnection(self, node1, node2):
        node1.addLinkTo(node2)
        node2.addLinkTo(node1)

