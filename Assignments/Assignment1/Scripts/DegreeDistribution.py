#Bioinformatics 3 : Wiebke Schmitt & Thibault Schowing
class DegreeDistribution:
    """Calculates a degree distribution for a network"""

    def __init__(self, network):
        """
        Inits DegreeDistribution with a network and calculate its distribution
        """
        self.histogram = [0] * (network.maxDegree() + 1)

        for key, node in network.nodes.items():
            self.histogram[node.degree()] += 1

        print("Debug: histogram list ", self.histogram)

        # Other option:
        # Dict containing {id:degree}
        # self.degrees = {}
        # for node in network.nodes.iteritems():
        # self.degrees[node.identifier] = node.degree()
        # for i in range(0, network.maxDegree() + 1:
        #     self.histogram[i] = self.degrees.values().count(i)

    def getNormalizedDistribution(self):
        '''
        Returns the computed normalized distribution
        '''

        maxvalue = max(self.histogram)
        norm = [float(i) / maxvalue for i in self.histogram]
        print("Debug: normalized histogram ", norm)
        return norm