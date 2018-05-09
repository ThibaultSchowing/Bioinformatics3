from random import gauss
import math
import random
import itertools
from generic_network import GenericNetwork


class Layout:
    def __init__(self, file_path):
        """
        :param file_path: path to a white-space-separated file that contains node interactions
        """
        # create a network from the given file
        self.network = GenericNetwork()
        self.network.read_from_tsv(file_path)
        # friction coefficient
        self.alpha = 0.03
        # random force interval
        self.interval = 0.3
        # initial square to distribute nodes
        self.size = 50


    def init_positions(self):
        """
        Initialise or reset the node positions, forces and charge.
        """

        netsize = len(self.network.nodes)

        # Set up the positions and charge
        for key, node in self.network.nodes.items():

            #Pick a coordinate between 0 and 50 (initial square)
            node.pos_x = random.randint(1,self.size + 1)
            node.pos_y = random.randint(1,self.size + 1)
            #print("Random posx: ", node.pos_x, " and posy ", node.pos_y)

            node.charge = node.degree()

        # Calculate the force
        self.calculate_forces()


    def calculate_forces(self):
        """
        Calculate the force on each node during the current iteration.
        """

        # For all pair of nodes...
        for pair in itertools.combinations(self.network.nodes.items(),2):

            node1 = pair[0][1]
            node2 = pair[1][1]

            coulombx = (node1.charge * node2.charge) * ((node1.pos_x - node2.pos_x)/((node1.pos_x - node2.pos_x)**2 + (node1.pos_y - node2.pos_y)**2)**(3/2))
            coulomby = (node1.charge * node2.charge) * ((node1.pos_y - node2.pos_y)/((node1.pos_x - node2.pos_x)**2 + (node1.pos_y - node2.pos_y)**2)**(3/2))
            harmonicx = 0.0
            harmonicy = 0.0

            # If the nodes are connected, we temper the force with the harmonic
            if node1.has_edge_to(node2):
                harmonicx = -(node1.pos_x - node2.pos_x)
                harmonicy = -(node1.pos_y - node2.pos_y)

            # Add the force to node1 .... opposite to node2
            fx = coulombx + harmonicx
            fy = coulomby + harmonicy

            node1.force_x += fx
            node1.force_y += fy

            node2.force_x -= fx
            node2.force_y -= fy


    def add_random_force(self, temperature):
        """
        Add a random force within [- temperature * interval, temperature * interval] to each node.
        (There is nothing to do here for you.)
        :param temperature: temperature in the current iteration
        """
        for node in self.network.nodes.values():
            node.force_x += gauss(0.0, self.interval * temperature)
            node.force_y += gauss(0.0, self.interval * temperature)

    def displace_nodes(self):
        """
        Change the position of each node according to the force applied to it and reset the force on each node.
        """

        for node in self.network.nodes.values():
            node.pos_x = node.pos_x + node.force_x * self.alpha
            node.pos_y = node.pos_y + node.force_y * self.alpha

            # Reset the forces to 0
            node.force_x = 0
            node.force_y = 0


    def calculate_energy(self):
        """
        Calculate the total energy of the network in the current iteration.
        :return: total energy
        """

        energy_total = 0

        for pair in itertools.combinations(self.network.nodes.values(), 2):
            node1 = pair[0]
            node2 = pair[1]

            # Coulomb energy
            Ec = (node1.degree() * node2.degree()) / (math.sqrt(((node1.pos_x - node2.pos_x)**2) + ((node1.pos_y - node2.pos_y)**2)))

            #Harmonic energy
            Eh = 0
            if node1.has_edge_to(node2):
                Eh = ((node1.pos_x - node2.pos_x)**2 + (node1.pos_y - node2.pos_y)**2)/2
            energy_total += Ec + Eh


        return energy_total

    def layout(self, iterations):
        """
        Executes the force directed layout algorithm. (There is nothing to do here for you.)
        :param iterations: number of iterations to perform
        :return: list of total energies
        """
        # initialise or reset the positions and forces
        self.init_positions()
        energies = []

        for _ in range(iterations):
            self.calculate_forces()
            self.displace_nodes()
            energies.append(self.calculate_energy())

        return energies

    def simulated_annealing_layout(self, iterations):
        """
        Executes the force directed layout algorithm with simulated annealing.
        :param iterations: number of iterations to perform
        :return: list of total energies
        """
        self.init_positions()
        energies = []
        temperature = 100000
        for i in range(iterations):
            # TODO: DECREASE THE TEMPERATURE IN EACH ITERATION. YOU CAN BE CREATIVE.
            temperature = 0.2 * temperature
            # there is nothing to do here for you
            self.calculate_forces()
            self.add_random_force(temperature)
            self.displace_nodes()
            energies.append(self.calculate_energy())

        return energies
