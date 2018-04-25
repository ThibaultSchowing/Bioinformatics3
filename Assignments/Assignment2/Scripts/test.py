#!/usr/bin/python
#Bioinformatics 3 : Wiebke Schmitt & Thibault Schowing
from ScaleFreeNetwork import ScaleFreeNetwork
from DegreeDistribution import DegreeDistribution
from RandomNetwork import RandomNetwork
import matplotlib.pyplot as plt
import Tools as Tools


if __name__== "__main__":

    # TASK 2.1 a AND b
    # # Creating two networks and taking the degree distributions
    # small = 1000
    # big = 10000
    # sf_net = ScaleFreeNetwork(small,2)
    # sf_net2 = ScaleFreeNetwork(big,2)
    # # EQUALLY SIZED _ CHECK THAT
    # # TODO this
    # rand_net = RandomNetwork(10000, 100000)
    #
    # sf_degree = DegreeDistribution(sf_net).getNormalizedDistribution()
    # sf_degree2 = DegreeDistribution(sf_net2).getNormalizedDistribution()
    # rand_degree = DegreeDistribution(rand_net).getNormalizedDistribution()
    #
    #
    #
    #
    # # Plot the degree distribution
    # Tools.plotDistributionComparisonLogLog([sf_degree, sf_degree2, rand_degree],[small,big, "rand"], "Degree Distribution Scale-Free network ")


    # TASK 2.1 c

    sf_net_c = ScaleFreeNetwork(1000, 2)
    sf_net_c_degree = DegreeDistribution(sf_net_c).getNormalizedDistribution()

    k = len(sf_net_c_degree) - 1

    gamma_distance = []

    steps = [x * 0.1 for x in range(10, 30)]
    for gamma in steps:
        theoretical_dist = Tools.getScaleFreeDistributionHistogram(gamma, k)
        distance = Tools.simpleKSdist(sf_net_c_degree, theoretical_dist)

        gamma_distance.append((gamma, distance))

    gamma_distance.sort(key=lambda x: x[1], reverse=False)

    # Pretty much always 1
    print("All gamma-distance: ", gamma_distance)
    print("Best gamma: ", gamma_distance[0][0])

    # Optimal theoretical distribution (powerlaw)
    optimal_theoretical = Tools.getScaleFreeDistributionHistogram(gamma_distance[0][0], k)
    Tools.plotDistributionComparisonLogLog([sf_net_c_degree, optimal_theoretical], ['Scale Free Network', 'PowerLaw'],'Compare theory to practice')