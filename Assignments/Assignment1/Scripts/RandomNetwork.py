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
        random.seed()
                    