#Bioinformatics 3 : Wiebke Schmitt & Thibault Schowing
import random
from Node import Node
from AbstractNetwork import AbstractNetwork
class ScaleFreeNetwork(AbstractNetwork):
    """Scale-free network implementation of AbstractNetwork"""


          
    def __createNetwork__(self, amount_nodes, amount_links):
        """
        Create a network with an amount of n nodes, add m links per iteration step
        for n nodes:
            for m links:
                link node to other nodes
        """

        def symetricConnection(node1, node2):
            node1.addLinkTo(node2)
            node2.addLinkTo(node1)

        random.seed()
        print("Debug: ", amount_nodes, " nodes and ", amount_links, "links.... creating ScaleFree network")

        # Initial m0 nodes connected to each other
        m0 = 3

        # Create Nodes
        for i in range(0, m0):
            self.appendNode(Node(i))

        # Connect Nodes to each other
        for i in range(0,amount_links):
            for j in range(i+1, m0):
                symetricConnection(self.getNode(i), self.getNode(j%3))


        # Method 1
        # In a first attempt we used the code below.


        def genProbList():
            prob_list = []
            sumkj = self.degreeSum()

            for key, node in self.nodes.items():
                ki = node.degree()
                prob_list.append(ki / sumkj)
            return prob_list


        # new nodes id (without the 3 initial nodes)
        for new_node_id in range(3, amount_nodes - 3):

            new_node = Node(new_node_id)
            self.appendNode(new_node)

            population = list(range(0, self.size()))

            # Generate probability list of existing nodes
            prob_list = genProbList()

            for i in range(amount_links):

                while(True):
                    # choose the neighbour according to its probability
                    chosen_neighbour = random.choices(population, weights=prob_list, k = 1)[0]

                    # if it's a new link and it's not a self-connection
                    if not new_node.hasLinkTo(chosen_neighbour) and not chosen_neighbour == new_node.id:

                        symetricConnection(new_node,self.getNode(chosen_neighbour))
                        break


        # Method 2
        # In a second attempt, we used the code below
        # # the initial network contains 3x2 links
        # network_degree = 6

        # # next node ID
        # id = 3
        #
        # while id < amount_nodes:
        #
        #     new_node = Node(id)
        #     self.appendNode(new_node)
        #     remaining_links = amount_links
        #
        #     while remaining_links:
        #         rand_node = random.choice(self.nodes)
        #
        #         if(id != rand_node.id and not rand_node.hasLinkTo(new_node)):
        #
        #             node_prob = rand_node.degree() / network_degree
        #             random_prob = random.random()
        #
        #             if(node_prob > random_prob):
        #                 rand_node.addLinkTo(new_node)
        #                 new_node.addLinkTo(rand_node)

        #                 network_degree += 2
        #                 remaining_links -= 1
        #
        #     id += 1
        #
        # print("Network created. Size: ", len(self.nodes), "    Total Degree: ", network_degree)

