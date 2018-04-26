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

        def genProbList():

            # Generate probability range for each nodes

            prob_list = []
            sumkj = self.degreeSum()

            for key, node in self.nodes.items():
                # calculate pi
                # ki = degree of node i
                #print("Debug: node degree: ", node.degree())
                ki = node.degree()
                # Sum kj = sum of all degrees

                prob_list.append(ki / sumkj)
                #print("Debug select neighbours prob list: ", prob_list)

            # now we have a probability list -> select the number_neighbours future neighbours

            #print("DEBUG probability list generated: ", prob_list)
            return prob_list






        random.seed()
        print("Debug: ", amount_nodes, " nodes and ", amount_links, "links.... creating ScaleFree network")

        # Initial m0 nodes connected to each other
        #
        # #QUESTION: is 3 fixed ??? Should it be dynamic ?

        m0 = 3
        # Number of links per node
        number_neighbours = amount_links

        # Contains the degrees of the initial complete network
        degree_list = [2,2,2]

        for i in range(0, m0):
            self.appendNode(Node(i))

        symetricConnection(self.getNode(0), self.getNode(1))
        symetricConnection(self.getNode(1), self.getNode(2))
        symetricConnection(self.getNode(0), self.getNode(2))

        # useless and slow
        # http://didar-physics.blogspot.de/2015/02/barabasialbert-model-generated-code.html
        # https://stackoverflow.com/questions/38008748/python-implementing-a-step-by-step-modified-barabasi-albert-model-for-scale-fr

        # Random failure measure
        random_failure = 0

        # new nodes id (without the 3 initial nodes)
        for new_node_id in range(3, amount_nodes - 3):

            #print("Debug: population: ", population)
            new_node = Node(new_node_id)
            self.appendNode(new_node)

            # Just a sequence of all node ids
            population = list(range(0, self.size()))

            # Generate probability list of existing nodes
            prob_list = genProbList()

            for i in range(amount_links):


                while(True):
                    chosen_neighbour = random.choices(population, weights=prob_list, k = 1)[0]

                    # if it's a new link and it's not a self-connection
                    if not new_node.hasLinkTo(chosen_neighbour) and not chosen_neighbour == new_node.id:

                        symetricConnection(new_node,self.getNode(chosen_neighbour))
                        break

                    # Random failure increment
                    random_failure += 1

            # debug info: print degrees
            self.degrees = []
            for id, node in self.nodes.items():
                self.degrees.append(node.degree())
            #print(self.degrees)



        print("Debug Random failure count: ", random_failure)

