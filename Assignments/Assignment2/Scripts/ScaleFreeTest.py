#!/usr/bin/python
#Bioinformatics 3 : Wiebke Schmitt & Thibault Schowing
from ScaleFreeNetwork import ScaleFreeNetwork
from DegreeDistribution import DegreeDistribution
from RandomNetwork import RandomNetwork
import time
import matplotlib.pyplot as plt
import Tools as Tools


if __name__== "__main__":

    # TASK 2.1 a AND b
    # Number of nodes and link per node
    SMALL = 10000
    BIG = 100000
    NB_LINK = 2

    # Create first network
    time1 = time.time()
    sf_net = ScaleFreeNetwork(SMALL,NB_LINK)
    time2 = time.time()
    print("Network created -> Time elapsed: ", (time2 - time1)/60, " minutes")

    # Create second network
    time1 = time.time()
    sf_net2 = ScaleFreeNetwork(BIG,NB_LINK)
    time2 = time.time()
    print("Network created -> Time elapsed: ", (time2 - time1)/60, " minutes")

    # Create random network
    rand_net = RandomNetwork(10000, 100000)

    # Network's normalized distributions
    sf_degree = DegreeDistribution(sf_net).getNormalizedDistribution()
    sf_degree2 = DegreeDistribution(sf_net2).getNormalizedDistribution()
    rand_degree = DegreeDistribution(rand_net).getNormalizedDistribution()

    # Plot the degree distributions
    # Small vs Big scale-free network
    legend1 = str(SMALL) + "Scale-Free"
    legend2 = str(BIG) + "Scale-Free"
    Tools.plotDistributionComparisonLogLog([sf_degree, sf_degree2],[legend1,legend2], "Plot_Degree Distribution of ScaleFree networks")

    # Big scale-free vs random network
    Tools.plotDistributionComparisonLogLog([sf_degree2, rand_degree], [legend2, "Random (1'0000 x 10'0000"],"Plot_Degree Distribution ScaleFree vs Random Network")

    # TASK 2.1 c
    # Find lambda - 10'000 nodes - 2 links
    sf_net_c = ScaleFreeNetwork(10000,2)
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
    Tools.plotDistributionComparisonLogLog([sf_net_c_degree, optimal_theoretical], ["Scale Free Network" + str(BIG), 'PowerLaw'],'Plot_Compare theory to practice')
