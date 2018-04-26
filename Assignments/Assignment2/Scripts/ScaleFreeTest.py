#!/usr/bin/python
#Bioinformatics 3 : Wiebke Schmitt & Thibault Schowing
from ScaleFreeNetwork import ScaleFreeNetwork
from DegreeDistribution import DegreeDistribution
from RandomNetwork import RandomNetwork
import matplotlib.pyplot as plt
import Tools as Tools


if __name__== "__main__":

    # TASK 2.1 a AND b
    # Creating two networks and taking the degree distributions
    #TODO update number of nodes and run it during ages
    small = 100
    big = 1000
    sf_net = ScaleFreeNetwork(small,2)
    sf_net2 = ScaleFreeNetwork(big,2)

    rand_net = RandomNetwork(10000, 100000)

    sf_degree = DegreeDistribution(sf_net).getNormalizedDistribution()
    sf_degree2 = DegreeDistribution(sf_net2).getNormalizedDistribution()
    rand_degree = DegreeDistribution(rand_net).getNormalizedDistribution()

    # Plot the degree distribution
    Tools.plotDistributionComparisonLogLog([sf_degree, sf_degree2],["10'000 Scale-Free","100'000 Scale-Free"], "Plot_Degree Distribution of ScaleFree networks")

    Tools.plotDistributionComparisonLogLog([sf_degree2, rand_degree], ["100'000 Scale-Free", "Random (10'000 x 100'000"],"Plot_Degree Distribution ScaleFree vs Random Network")

    # TASK 2.1 c

    sf_net_c = ScaleFreeNetwork(1000, 2)
    sf_net_c_degree = DegreeDistribution(sf_net_c).getNormalizedDistribution()

    k = len(sf_net_c_degree)

    gamma_distance = []

    # Foreach gamma, calculate the KS distance
    steps = [x * 0.1 for x in range(10, 30)]
    for gamma in steps:
        theoretical_dist = Tools.getScaleFreeDistributionHistogram(gamma, k)
        distance = Tools.simpleKSdist(theoretical_dist, sf_net_c_degree)
        gamma_distance.append((gamma, distance))

    # Sort the distances-gamma tuples
    gamma_distance.sort(key=lambda x: x[1], reverse=False)

    print("All gamma-distance: ", gamma_distance)
    print("Best gamma: ", gamma_distance[0][0])

    # Optimal theoretical distribution (powerlaw) with the best gamma
    optimal_theoretical = Tools.getScaleFreeDistributionHistogram(gamma_distance[0][0], k)
    Tools.plotDistributionComparisonLogLog([sf_net_c_degree, optimal_theoretical], ['Scale Free Network', 'PowerLaw'],'Plot_Compare theory to practice')
